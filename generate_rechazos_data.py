import requests
import pandas as pd
import json
from io import BytesIO
from datetime import datetime
from collections import defaultdict

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
import os

SHARE_URL   = os.environ.get("NEXTCLOUD_SHARE_URL")   # link público /s/TOKEN
OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "rechazos_data.json")

# Fallback a credenciales directas (uso local)
if not SHARE_URL:
    try:
        from config_rechazos import NEXTCLOUD_URL, USERNAME, APP_PASSWORD, FILE_PATH
        OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "rechazos_data.json")
    except ImportError:
        NEXTCLOUD_URL = os.environ.get("NEXTCLOUD_URL")
        USERNAME      = os.environ.get("NEXTCLOUD_USERNAME")
        APP_PASSWORD  = os.environ.get("NEXTCLOUD_APP_PASSWORD")
        FILE_PATH     = os.environ.get("NEXTCLOUD_FILE_PATH")
        if not all([NEXTCLOUD_URL, USERNAME, APP_PASSWORD, FILE_PATH]):
            raise SystemExit(
                "ERROR: Define NEXTCLOUD_SHARE_URL o las credenciales directas:\n"
                "  NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_APP_PASSWORD, NEXTCLOUD_FILE_PATH"
            )
# ──────────────────────────────────────────────────────────────────────────────


def _get_ocs_direct_url():
    """Obtiene un URL de descarga temporal sin restricción de IP via OCS API."""
    import xml.etree.ElementTree as ET

    # File ID puede venir de variable de entorno (GitHub secret) o se descubre via PROPFIND local
    file_id = os.environ.get("NEXTCLOUD_FILE_ID")

    if not file_id:
        # Fallback: PROPFIND en la raíz para buscar el archivo (funciona localmente)
        import urllib.parse
        propfind_body = (
            '<?xml version="1.0"?>'
            '<d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">'
            "<d:prop><oc:fileid/></d:prop></d:propfind>"
        )
        nc_user = USERNAME.split("@")[0]
        root_url = f"{NEXTCLOUD_URL}/remote.php/dav/files/{nc_user}/"
        r = requests.request(
            "PROPFIND", root_url,
            auth=(USERNAME, APP_PASSWORD),
            headers={"Depth": "1", "Content-Type": "application/xml"},
            data=propfind_body, timeout=30,
        )
        if r.status_code not in (200, 207):
            raise SystemExit(f"PROPFIND en raíz falló con HTTP {r.status_code}")
        xml_root = ET.fromstring(r.text)
        filename = FILE_PATH.lstrip("/")
        filename_encoded = urllib.parse.quote(filename)
        for response in xml_root.findall("{DAV:}response"):
            href = response.findtext("{DAV:}href") or ""
            if filename in urllib.parse.unquote(href) or filename_encoded in href:
                file_id = response.findtext(".//{http://owncloud.org/ns}fileid")
                break
        if not file_id:
            raise SystemExit(f"No se encontró '{filename}' en la raíz de Nextcloud.")

    print(f"File ID: {file_id}")

    ocs_url = f"{NEXTCLOUD_URL}/ocs/v2.php/apps/dav/api/v1/direct"
    r2 = requests.post(
        ocs_url,
        auth=(USERNAME, APP_PASSWORD),
        headers={"OCS-APIREQUEST": "true", "Content-Type": "application/json"},
        json={"fileId": int(file_id)},
        timeout=30,
    )
    root2 = ET.fromstring(r2.text)
    direct_url = root2.findtext(".//{http://www.w3.org/ns/dav}url") or root2.findtext(".//url")
    if not direct_url:
        raise SystemExit(f"OCS no devolvió URL directo. Respuesta: {r2.text[:200]}")
    print(f"URL directo obtenido (expira en ~60s)")
    return direct_url


def fetch_excel():
    if SHARE_URL:
        # Link público de Nextcloud: /s/TOKEN/download
        url = SHARE_URL.rstrip("/") + "/download"
        print(f"Descargando via link público: {url}")
        r = requests.get(url, timeout=60)
    else:
        # Obtener URL directo temporal via OCS API (sin restricción de IP)
        direct_url = _get_ocs_direct_url()
        print(f"Descargando via URL directo OCS...")
        r = requests.get(direct_url, timeout=120)

    if r.status_code == 401:
        raise SystemExit("ERROR 401: Credenciales incorrectas.")
    if r.status_code == 404:
        raise SystemExit(f"ERROR 404: Archivo no encontrado.")
    if "text/html" in r.headers.get("Content-Type", ""):
        raise SystemExit(f"ERROR: Respuesta HTML inesperada ({len(r.content)} bytes). Posible página de login.")
    r.raise_for_status()
    print(f"Archivo recibido: {len(r.content):,} bytes")
    return BytesIO(r.content)


def _safe_int(val):
    try:
        s = str(val).strip()
        if s in ("", "nan", "None", "NaN"):
            return 0
        return int(float(s))
    except Exception:
        return 0


def _clean(val):
    s = str(val).strip() if val is not None else ""
    return "" if s in ("nan", "None", "NaT") else s


def process_excel(file_obj):
    print("Leyendo hojas del Excel...")
    xl = pd.read_excel(file_obj, sheet_name=None, dtype=str)

    semanas = []
    all_rows = []

    for sheet_name, df in xl.items():
        if df.empty:
            continue

        # Elimina filas completamente vacías
        df.dropna(how="all", inplace=True)
        df.columns = [str(c).strip() for c in df.columns]

        # Detecta columnas por nombre (flexible)
        col = {}
        for c in df.columns:
            cl = c.lower()
            if "tienda" in cl or "store" in cl:
                col.setdefault("tienda", c)
            elif "orden" in cl or "order" in cl or "pedido" in cl:
                col.setdefault("orden", c)
            elif "sku" in cl or "upc" in cl or "asin" in cl:
                col.setdefault("sku", c)
            elif "qty" in cl or "cant" in cl or "cantidad" in cl or "unit" in cl:
                col.setdefault("qty", c)
            elif "comentario" in cl or "comment" in cl or "nota" in cl:
                col.setdefault("comentario", c)
            elif "razon" in cl or "razón" in cl or "reason" in cl or "motivo" in cl:
                col.setdefault("razon", c)

        # Palabras que indican fin de datos reales (tabla resumen al final de la hoja)
        STOP_IN_SKU    = {"total"}
        STOP_IN_TIENDA = {"sku", "qty", "top", "total"}

        rows = []
        for _, row in df.iterrows():
            tienda = _clean(row.get(col.get("tienda", "__x__"), ""))
            sku    = _clean(row.get(col.get("sku",    "__x__"), ""))
            orden  = _clean(row.get(col.get("orden",  "__x__"), ""))
            qty    = _safe_int(row.get(col.get("qty", "__x__"), 0))
            coment = _clean(row.get(col.get("comentario", "__x__"), ""))
            razon  = _clean(row.get(col.get("razon",  "__x__"), ""))

            # Detectar fila "Total" o encabezado de tabla resumen → fin de datos
            if sku.lower() in STOP_IN_SKU or tienda.lower() in STOP_IN_TIENDA:
                break

            if not sku and not orden:
                continue

            entry = {
                "semana":      sheet_name,
                "tienda":      tienda,
                "orden":       orden,
                "sku":         sku,
                "qty":         qty,
                "comentario":  coment,
                "razon":       razon,
            }
            rows.append(entry)
            all_rows.append(entry)

        semanas.append({
            "nombre":    sheet_name,
            "rechazos":  len(rows),
            "qty_total": sum(r["qty"] for r in rows),
            "datos":     rows,
        })
        print(f"  {sheet_name:30s}  {len(rows):>4} rechazos  |  QTY {sum(r['qty'] for r in rows):>6,}")

    return semanas, all_rows


def build_json(semanas, all_rows):
    tienda_stats = defaultdict(lambda: {"rechazos": 0, "qty": 0})
    sku_stats    = defaultdict(lambda: {"rechazos": 0, "qty": 0})
    razon_stats  = defaultdict(int)

    for r in all_rows:
        if r["tienda"]:
            tienda_stats[r["tienda"]]["rechazos"] += 1
            tienda_stats[r["tienda"]]["qty"]      += r["qty"]
        if r["sku"]:
            sku_stats[r["sku"]]["rechazos"] += 1
            sku_stats[r["sku"]]["qty"]      += r["qty"]
        if r["razon"]:
            razon_stats[r["razon"]] += 1

    top_tiendas = sorted(tienda_stats.items(), key=lambda x: x[1]["rechazos"], reverse=True)[:20]
    top_skus    = sorted(sku_stats.items(),    key=lambda x: x[1]["rechazos"], reverse=True)[:20]

    return {
        "generado_en":   datetime.now().isoformat(),
        "archivo":       FILE_PATH.lstrip("/"),
        "resumen": {
            "total_rechazos":    len(all_rows),
            "total_qty":         sum(r["qty"] for r in all_rows),
            "tiendas_unicas":    len(tienda_stats),
            "skus_unicos":       len(sku_stats),
            "semanas_procesadas": len(semanas),
        },
        "tendencia_semanal": [
            {"semana": s["nombre"], "rechazos": s["rechazos"], "qty": s["qty_total"]}
            for s in semanas
        ],
        "top_tiendas": [
            {"tienda": t, "rechazos": v["rechazos"], "qty": v["qty"]}
            for t, v in top_tiendas
        ],
        "top_skus": [
            {"sku": s, "rechazos": v["rechazos"], "qty": v["qty"]}
            for s, v in top_skus
        ],
        "razones": [
            {"razon": r, "count": c}
            for r, c in sorted(razon_stats.items(), key=lambda x: x[1], reverse=True)
        ],
        "detalle": all_rows,
    }


def main():
    file_obj        = fetch_excel()
    semanas, rows   = process_excel(file_obj)
    data            = build_json(semanas, rows)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    r = data["resumen"]
    print(f"\nOK: {OUTPUT_JSON} generado")
    print(f"  Semanas procesadas : {r['semanas_procesadas']}")
    print(f"  Total rechazos     : {r['total_rechazos']:,}")
    print(f"  Total QTY rechazada: {r['total_qty']:,}")
    print(f"  Tiendas unicas     : {r['tiendas_unicas']}")
    print(f"  SKUs unicos        : {r['skus_unicos']}")


if __name__ == "__main__":
    main()
