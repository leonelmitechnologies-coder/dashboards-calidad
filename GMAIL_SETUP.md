# 📧 Configuración de Gmail API para Envío Automático de Emails

## Guía Completa de Configuración

Esta guía te llevará paso a paso para configurar Google Cloud y Gmail API para habilitar el envío 100% automático de emails desde los dashboards de Control de Calidad.

---

## ✅ Requisitos Previos

- Cuenta de Google/Gmail
- Acceso a Google Cloud Console
- Navegador web (Chrome, Edge, o Firefox recomendados)

---

## 📋 Paso 1: Crear Proyecto en Google Cloud

### 1.1. Acceder a Google Cloud Console

1. Navega a [Google Cloud Console](https://console.cloud.google.com)
2. Inicia sesión con tu cuenta de Google
3. En la barra superior, clic en el selector de proyectos (al lado del logo de Google Cloud)

### 1.2. Crear Nuevo Proyecto

1. Clic en **"NEW PROJECT"** (Nuevo Proyecto)
2. Completa el formulario:

   **Nombre del proyecto:**
   ```
   Dashboard Quality Control Gmail
   ```

   **Organization:** (Dejar por defecto)

   **Location:** (Dejar por defecto o seleccionar tu organización)

3. Clic en **"CREATE"** (Crear)
4. Espera 10-15 segundos mientras se crea el proyecto
5. Verás una notificación cuando esté listo

---

## 🔌 Paso 2: Habilitar Gmail API

### 2.1. Activar la API

1. Asegúrate de que tu nuevo proyecto esté seleccionado (verifica en la barra superior)
2. En el menú de navegación (☰), ve a **"APIs & Services"** → **"Library"**
3. En el buscador, escribe: `Gmail API`
4. Clic en **"Gmail API"** (debe aparecer con el logo de Gmail)
5. Clic en el botón azul **"ENABLE"** (Habilitar)
6. Espera a que se habilite (5-10 segundos)

### 2.2. Verificar Activación

Deberías ver:
- ✅ Status: "API enabled"
- 📊 Dashboard de métricas (aún sin datos)

---

## 🔐 Paso 3: Configurar OAuth Consent Screen

### 3.1. Pantalla de Consentimiento

1. En el menú lateral, ve a **"APIs & Services"** → **"OAuth consent screen"**
2. Selecciona tipo de usuario:
   - **External** (Externo) - Para uso personal o con cualquier cuenta Google
   - Clic en **"CREATE"** (Crear)

### 3.2. Configurar App Information

**Paso 1: App information**

Completa los siguientes campos obligatorios:

- **App name:** `Dashboard Quality Control - Email Sender`
- **User support email:** Tu email de Google
- **App logo:** (Opcional - puedes dejarlo en blanco)
- **App domain:** (Opcional - dejar en blanco para pruebas)
- **Authorized domains:** (Opcional - dejar en blanco para pruebas)
- **Developer contact information:** Tu email de Google

Clic en **"SAVE AND CONTINUE"** (Guardar y continuar)

**Paso 2: Scopes**

1. Clic en **"ADD OR REMOVE SCOPES"** (Agregar o quitar permisos)
2. En el buscador, filtra por: `gmail`
3. Selecciona los siguientes scopes:
   - ✅ `.../auth/gmail.send` - Send email on your behalf
   - ✅ `.../auth/userinfo.email` - See your primary Google Account email address
   - ✅ `.../auth/userinfo.profile` - See your personal info
4. Clic en **"UPDATE"** (Actualizar)
5. Clic en **"SAVE AND CONTINUE"** (Guardar y continuar)

**Paso 3: Test users (Solo para External - Modo Testing)**

1. Clic en **"+ ADD USERS"** (Agregar usuarios)
2. Agrega tu email de Gmail (el que usarás para enviar emails)
3. Agrega otros emails si necesitas (máximo 100 en modo testing)
4. Clic en **"ADD"** (Agregar)
5. Clic en **"SAVE AND CONTINUE"** (Guardar y continuar)

**Paso 4: Summary**

Revisa la configuración y clic en **"BACK TO DASHBOARD"** (Volver al panel)

---

## 🔑 Paso 4: Crear OAuth 2.0 Client ID

### 4.1. Crear Credenciales

1. En el menú lateral, ve a **"APIs & Services"** → **"Credentials"**
2. Clic en **"+ CREATE CREDENTIALS"** (Crear credenciales)
3. Selecciona **"OAuth client ID"**

### 4.2. Configurar Client ID

**Application type:** Selecciona `Web application`

**Name:** `Dashboard Quality Control Web Client`

**Authorized JavaScript origins:**

Agrega las siguientes URIs (clic en "+ ADD URI" para cada una):

```
http://localhost:8000
http://localhost:5500
http://127.0.0.1:8000
http://127.0.0.1:5500
https://tudominio.com  (reemplaza con tu dominio real en producción)
```

**Authorized redirect URIs:**

Agrega las siguientes URIs:

```
http://localhost:8000/dashboard-incoming.html
http://localhost:8000/dashboard-outgoing.html
http://localhost:5500/dashboard-incoming.html
http://localhost:5500/dashboard-outgoing.html
http://127.0.0.1:8000/dashboard-incoming.html
http://127.0.0.1:8000/dashboard-outgoing.html
https://tudominio.com/dashboard-incoming.html  (si aplica)
https://tudominio.com/dashboard-outgoing.html  (si aplica)
```

Clic en **"CREATE"** (Crear)

### 4.3. Guardar Client ID

Verás un popup con tus credenciales:

**🔑 GUARDA ESTOS VALORES (los necesitarás después):**

- **Client ID**: `XXXXXX-XXXXXXXXXX.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-XXXXXXXXXXXX` (no se usa en web apps, pero guárdalo por si acaso)

⚠️ **IMPORTANTE:** Copia el **Client ID** a un archivo de texto. Lo necesitarás en el siguiente paso.

Clic en **"OK"**

---

## 📝 Paso 5: Actualizar Configuración en los Dashboards

### 5.1. Abrir Archivos de Dashboard

Abre los siguientes archivos con tu editor de código:
- `dashboard-incoming.html`
- `dashboard-outgoing.html`

### 5.2. Actualizar Gmail API Configuration

Busca la sección de configuración de Gmail API (aproximadamente línea 920):

```javascript
const GMAIL_CONFIG = {
    clientId: 'YOUR-CLIENT-ID-HERE.apps.googleusercontent.com',  // 👈 REEMPLAZA ESTE VALOR
    apiKey: '',  // No necesario para OAuth 2.0
    discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest'],
    scopes: 'https://www.googleapis.com/auth/gmail.send'
};
```

**Reemplaza el siguiente valor:**

**`YOUR-CLIENT-ID-HERE.apps.googleusercontent.com`** → Pega tu **Client ID** de Google Cloud

**Ejemplo:**
```javascript
const GMAIL_CONFIG = {
    clientId: '123456789-abc123xyz.apps.googleusercontent.com',
    apiKey: '',
    discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest'],
    scopes: 'https://www.googleapis.com/auth/gmail.send'
};
```

### 5.3. (Opcional) Cambiar Email Predeterminado

Si deseas cambiar el destinatario por defecto, busca:

```javascript
const EMAIL_CONFIG = {
    defaultRecipient: 'leonelhdze@gmail.com'  // 👈 Cambia este email
};
```

### 5.4. Guardar Archivos

Guarda ambos archivos después de realizar los cambios.

---

## 🧪 Paso 6: Probar la Configuración

### 6.1. Iniciar Servidor Local

Para probar, necesitas servir los archivos HTML desde un servidor local:

**Opción 1: Python (si tienes Python instalado)**
```bash
cd C:\Proyectos_IA\web_Calidad\dash
python -m http.server 8000
```

**Opción 2: Node.js (si tienes Node instalado)**
```bash
cd C:\Proyectos_IA\web_Calidad\dash
npx serve -l 8000
```

**Opción 3: VS Code Live Server**
- Instala extensión "Live Server"
- Clic derecho en dashboard-incoming.html → "Open with Live Server"

### 6.2. Abrir Dashboard en Navegador

1. Abre tu navegador
2. Navega a:
   ```
   http://localhost:8000/dashboard-incoming.html
   ```

### 6.3. Verificar Autenticación

1. Deberías ver dos badges en la esquina superior derecha:
   - **Badge superior**: "Última actualización"
   - **Badge inferior**: "No autenticado" con botón "🔐 Iniciar Sesión con Gmail"

2. Clic en **"🔐 Iniciar Sesión con Gmail"**

3. Se abrirá un popup de Google pidiendo:
   - **Elegir cuenta**: Selecciona tu cuenta de Gmail
   - **Pantalla de advertencia** (si está en modo Testing):
     ```
     Google hasn't verified this app
     ```
     - Clic en **"Advanced"** (Avanzado)
     - Clic en **"Go to Dashboard Quality Control - Email Sender (unsafe)"**
     - Esto es normal en modo testing - es tu propia app

   - **Pantalla de permisos**:
     ```
     Dashboard Quality Control - Email Sender wants to:
     ✓ Send email on your behalf
     ✓ See your primary email address
     ```
     - Clic en **"Allow"** (Permitir)

4. **Login exitoso**:
   - El popup se cerrará
   - Verás un mensaje: "✅ Autenticado exitosamente con Gmail"
   - El badge cambiará a: "👤 [Tu Email]" con botón "🚪 Cerrar Sesión"

### 6.4. Probar Envío de Email

1. Genera el resumen ejecutivo:
   - Navega por el dashboard
   - Aplica filtros si deseas
   - Clic en **"📄 Resumen Ejecutivo"**

2. Compartir por email:
   - En el modal del resumen, clic en **"📧 Compartir por Email"**
   - Verás confirmación: "Se enviará el email a: leonelhdze@gmail.com"
   - Clic en **OK**

3. **Envío automático**:
   - Verás indicador de carga: "📧 Enviando email vía Gmail..."
   - Después de 2-3 segundos: "✅ Email enviado exitosamente vía Gmail API"

4. **Verificar email recibido**:
   - Abre Gmail en otra pestaña
   - Revisa la bandeja de entrada de `leonelhdze@gmail.com`
   - Deberías ver el email con el resumen ejecutivo completamente formateado

---

## 🔍 Solución de Problemas (Troubleshooting)

### Error: "Origin mismatch" o "redirect_uri_mismatch"

**Causa**: La URL desde donde abres el dashboard no coincide con las configuradas en Google Cloud.

**Solución**:
1. Ve a Google Cloud Console → Credentials → Tu OAuth Client ID
2. Verifica que las **Authorized JavaScript origins** incluyan:
   - `http://localhost:8000` (exacta)
   - El puerto que estés usando
3. Verifica que las **Authorized redirect URIs** incluyan:
   - `http://localhost:8000/dashboard-incoming.html` (exacta)
4. Guarda los cambios
5. Espera 5 minutos para que los cambios se propaguen
6. Recarga la página del dashboard

### Error: "Access blocked: This app's request is invalid"

**Causa**: El OAuth Consent Screen no está configurado correctamente.

**Solución**:
1. Ve a Google Cloud Console → OAuth consent screen
2. Verifica que el estado sea "Testing" o "Published"
3. Verifica que tu email esté en **Test users**
4. Verifica que los **Scopes** incluyan `gmail.send`

### Error: "Popup blocked" o "popup_window_error"

**Causa**: El navegador está bloqueando popups.

**Solución**:
1. En Chrome/Edge: Busca el ícono de popup bloqueado en la barra de direcciones
2. Clic en el ícono → "Always allow popups from this site"
3. Recarga la página e intenta nuevamente

### Error: "Failed to fetch" o "CORS error"

**Causa**: No estás sirviendo el archivo desde un servidor HTTP.

**Solución**:
1. NO abras el archivo directamente (file:///)
2. Usa un servidor local (Python, Node, o Live Server)
3. Accede vía `http://localhost:8000/dashboard-incoming.html`

### El email no llega al destinatario

**Posibles causas y soluciones**:

1. **Email en spam**:
   - Revisa la carpeta de spam/correo no deseado
   - Marca el remitente como seguro

2. **Email incorrecto**:
   - Verifica que `EMAIL_CONFIG.defaultRecipient` tenga el email correcto
   - Guarda el archivo y recarga

3. **Cuenta no verificada**:
   - Ve a Gmail y verifica que tu cuenta esté activa
   - Intenta enviar un email manual primero

### Token expirado

**Síntoma**: Después de varias horas, el envío de email falla.

**Causa**: Los tokens en sessionStorage expiran.

**Solución**:
- Cierra sesión y vuelve a iniciar sesión
- O simplemente recarga la página (el sistema intentará renovar el token automáticamente)

---

## 🔒 Consideraciones de Seguridad

### ✅ Buenas Prácticas Implementadas

1. **Tokens en sessionStorage**: Los tokens se borran al cerrar el navegador
2. **OAuth 2.0**: Autenticación segura sin contraseñas en el código
3. **Permisos mínimos**: Solo `gmail.send` (enviar emails)
4. **Client ID público**: Es seguro exponer el Client ID en el código
5. **Sin Client Secret**: Las aplicaciones web no usan Client Secret

### ⚠️ Recomendaciones Adicionales

1. **Modo Testing vs Production**:
   - En modo Testing, solo los test users pueden usar la app
   - Para producción, necesitas verificar la app con Google (proceso de revisión)

2. **Limitar usuarios**:
   - En modo Testing, máximo 100 test users
   - Agrega solo emails que realmente necesiten acceso

3. **Monitoreo**:
   - Revisa el dashboard de Google Cloud para monitorear uso de la API
   - Gmail API tiene cuotas: 1 billón de quotas units por día (suficiente para miles de emails)

---

## 📊 Verificación Final

Antes de considerar la configuración completa, verifica:

- [ ] Proyecto creado en Google Cloud Console
- [ ] Gmail API habilitada
- [ ] OAuth Consent Screen configurado
- [ ] Test users agregados (incluyendo tu email)
- [ ] OAuth Client ID creado
- [ ] Authorized JavaScript origins configurados
- [ ] Authorized redirect URIs configurados
- [ ] Client ID copiado y pegado en dashboards
- [ ] Servidor local iniciado
- [ ] Login funciona correctamente (popup abre y cierra)
- [ ] Badge de autenticación muestra email del usuario
- [ ] Email se envía correctamente
- [ ] Email se recibe con formato correcto

---

## 🎓 Conceptos Clave

### ¿Qué es Gmail API?

**Gmail API** es la API oficial de Google que permite a las aplicaciones interactuar con Gmail de forma programática. Permite leer, enviar, modificar y organizar mensajes.

### ¿Qué es OAuth 2.0?

**OAuth 2.0** es un protocolo de autorización que permite a las aplicaciones acceder a recursos (como Gmail) sin compartir contraseñas. El usuario otorga permisos específicos de forma segura.

### ¿Por qué "unsafe" en modo Testing?

Google muestra advertencia "unsafe" porque la app no ha pasado por el proceso de verificación de Google. Es normal para apps en desarrollo o uso personal. Tu app ES segura - solo tú controlas el código.

### ¿Cuál es la diferencia con Microsoft Graph API?

- **Gmail API**: Para cuentas de Google/Gmail (personales o Google Workspace)
- **Microsoft Graph API**: Para cuentas de Microsoft/Outlook (Microsoft 365/Azure AD)

Ambas funcionan de forma similar con OAuth 2.0, pero son ecosistemas diferentes.

---

## 📞 Soporte

Si tienes problemas adicionales:

1. **Logs del navegador**: Abre Developer Tools (F12) → Console para ver errores
2. **Logs de Google Cloud**: Console → APIs & Services → Dashboard
3. **Documentación oficial**: [Gmail API Docs](https://developers.google.com/gmail/api)
4. **Quotas**: [Gmail API Quotas](https://developers.google.com/gmail/api/reference/quota)

---

## 🎉 ¡Listo!

Has completado la configuración de Gmail API. Ahora tus dashboards pueden enviar emails automáticamente vía Gmail sin intervención manual.

**Beneficios logrados:**
- ✅ Envío 100% automático de emails
- ✅ Sin copy/paste manual
- ✅ Sin abrir Gmail manualmente
- ✅ Formato HTML completo preservado
- ✅ Funciona con cualquier cuenta de Gmail
- ✅ Gratis (dentro de las cuotas de Gmail API)

---

**Última actualización**: Febrero 2026
**Versión**: 1.0
**Compatible con**: Gmail API v1, Google Cloud Platform
