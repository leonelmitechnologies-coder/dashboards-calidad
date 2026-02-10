# 📧 Configuración de EmailJS para Envío Automático de Emails

## Guía Rápida de Configuración (5 minutos)

EmailJS es un servicio que permite enviar emails directamente desde JavaScript sin backend. Es la forma más simple de implementar envío automático de emails.

---

## ✅ Requisitos Previos

- Cuenta de Gmail (o cualquier email)
- Navegador web
- 5 minutos de tu tiempo

---

## 🚀 Paso 1: Crear Cuenta en EmailJS

### 1.1. Registrarse

1. Ve a [EmailJS.com](https://www.emailjs.com)
2. Clic en **"Sign Up"** (esquina superior derecha)
3. Opciones de registro:
   - **Recomendado**: "Sign up with Google" (1 clic)
   - O: Registrar con email y contraseña
4. Si usas Google, autoriza el acceso
5. ¡Listo! Ya tienes cuenta

**Plan gratuito incluye:**
- ✅ 200 emails por mes
- ✅ Soporte HTML
- ✅ Sin tarjeta de crédito
- ✅ Suficiente para uso normal

---

## 📮 Paso 2: Conectar tu Email (Add Email Service)

### 2.1. Agregar Servicio de Email

1. En el dashboard de EmailJS, ve a **"Email Services"** (menú lateral izquierdo)
2. Clic en **"Add New Service"** (botón azul)
3. Selecciona tu proveedor de email:
   - **Gmail** (recomendado)
   - Outlook
   - Yahoo
   - O cualquier otro

### 2.2. Conectar Gmail

1. Después de seleccionar Gmail, clic en **"Connect Account"**
2. Se abrirá popup de Google
3. Selecciona tu cuenta de Gmail
4. Autoriza EmailJS para enviar emails en tu nombre:
   - Verás: "EmailJS wants to send email on your behalf"
   - Clic en **"Allow"**
5. **Nombre del servicio**: Puedes dejarlo como "Gmail" o cambiar a "Dashboard_Gmail"
6. Clic en **"Create Service"**

### 2.3. Guardar Service ID

**🔑 IMPORTANTE**: Verás tu **Service ID** (ejemplo: `service_abc123`)

**Cópialo y guárdalo** - lo necesitarás después.

---

## 📝 Paso 3: Crear Template de Email

### 3.1. Ir a Email Templates

1. En el menú lateral, clic en **"Email Templates"**
2. Clic en **"Create New Template"** (botón azul)

### 3.2. Configurar Template

**Template Name**: `Dashboard_Quality_Report`

**En la sección "Content":**

**Subject:**
```
{{subject}}
```

**Body (HTML):**
```
{{{html_content}}}
```

**⚠️ IMPORTANTE**: Usa **3 llaves** `{{{` en vez de 2 para HTML. Esto preserva el formato HTML completo.

### 3.3. Configurar Settings

**From Name:**
```
Dashboard Control de Calidad
```

**From Email:** (se auto-completa con tu Gmail)

**To Email:**
```
{{to_email}}
```

**Reply To:**
```
{{reply_to}}
```
(opcional, puede ser tu email)

### 3.4. Guardar Template

1. Clic en **"Save"** (botón azul arriba a la derecha)
2. **Copia el Template ID** que aparece (ejemplo: `template_xyz789`)

---

## 🔑 Paso 4: Obtener Public Key

1. En el menú lateral, clic en **"Account"** (parte superior)
2. Ve a la sección **"General"**
3. Encontrarás **"Public Key"** (ejemplo: `AbC123XyZ`)
4. **Cópialo y guárdalo**

---

## 📝 Paso 5: Configurar Dashboards

### 5.1. Valores que Necesitas

Deberías tener estos 3 valores:

```
Service ID:  service_xxxxxxx
Template ID: template_yyyyyyy
Public Key:  zzzzzzzzzzzzzzz
```

### 5.2. Actualizar dashboard-incoming.html

Abre el archivo y busca (aproximadamente línea 920):

```javascript
const EMAILJS_CONFIG = {
    serviceId: 'YOUR-SERVICE-ID',      // 👈 PEGA TU SERVICE ID
    templateId: 'YOUR-TEMPLATE-ID',    // 👈 PEGA TU TEMPLATE ID
    publicKey: 'YOUR-PUBLIC-KEY'       // 👈 PEGA TU PUBLIC KEY
};

const EMAIL_CONFIG = {
    defaultRecipient: 'leonelhdze@gmail.com',  // 👈 Email destinatario
    replyTo: 'tu-email@gmail.com'              // 👈 Tu email (para respuestas)
};
```

**Reemplaza:**
- `YOUR-SERVICE-ID` → Tu Service ID de EmailJS
- `YOUR-TEMPLATE-ID` → Tu Template ID de EmailJS
- `YOUR-PUBLIC-KEY` → Tu Public Key de EmailJS
- `leonelhdze@gmail.com` → Email destinatario por defecto
- `tu-email@gmail.com` → Tu email (para reply-to)

**Ejemplo:**
```javascript
const EMAILJS_CONFIG = {
    serviceId: 'service_abc123',
    templateId: 'template_xyz789',
    publicKey: 'AbC123XyZ'
};

const EMAIL_CONFIG = {
    defaultRecipient: 'leonelhdze@gmail.com',
    replyTo: 'dashboard@miempresa.com'
};
```

### 5.3. Actualizar dashboard-outgoing.html

Repite el mismo proceso en `dashboard-outgoing.html` con los mismos valores.

---

## 🧪 Paso 6: Probar

### 6.1. Iniciar Servidor Local

**Python:**
```bash
cd C:\Proyectos_IA\web_Calidad\dash
python -m http.server 8000
```

**Node.js:**
```bash
npx serve -l 8000
```

### 6.2. Abrir Dashboard

```
http://localhost:8000/dashboard-incoming.html
```

### 6.3. Enviar Email de Prueba

1. Clic en **"📄 Resumen Ejecutivo"**
2. Clic en **"📧 Compartir por Email"**
3. Confirmar destinatario
4. **¡Email se envía automáticamente!** ⚡
5. Verás: "✅ Email enviado exitosamente vía EmailJS"

### 6.4. Verificar Email

1. Abre Gmail
2. Revisa inbox de `leonelhdze@gmail.com`
3. Deberías ver el email con formato HTML completo

---

## 🔍 Solución de Problemas (Troubleshooting)

### Error: "Failed to send email"

**Causa 1**: Credenciales incorrectas

**Solución**:
- Verifica que Service ID, Template ID y Public Key sean correctos
- Verifica que no haya espacios extra al copiar/pegar
- Revisa en EmailJS dashboard que el servicio esté activo

**Causa 2**: Límite de emails excedido

**Solución**:
- Plan gratuito: 200 emails/mes
- Revisa tu cuota en EmailJS dashboard → Account → Usage
- Si necesitas más, considera upgrade a plan pagado ($9/mes para 1000 emails)

### Error: "Service is not available"

**Causa**: Servicio de Gmail no conectado correctamente

**Solución**:
1. Ve a EmailJS dashboard → Email Services
2. Verifica que tu servicio de Gmail tenga estado "Active" (verde)
3. Si está inactivo, clic en "Reconnect" y vuelve a autorizar

### Error: "Template not found"

**Causa**: Template ID incorrecto

**Solución**:
1. Ve a EmailJS dashboard → Email Templates
2. Verifica el Template ID correcto
3. Copia y pega nuevamente en el dashboard

### Email llega sin formato

**Causa**: Template usa `{{html_content}}` en vez de `{{{html_content}}}`

**Solución**:
1. Ve a EmailJS dashboard → Email Templates → Tu template
2. En el Body, asegúrate de usar **3 llaves**: `{{{html_content}}}`
3. Save y vuelve a intentar

### Email no llega

**Posibles causas y soluciones**:

1. **Email en spam**:
   - Revisa carpeta de spam
   - Marca como "No es spam"

2. **Email destinatario incorrecto**:
   - Verifica `EMAIL_CONFIG.defaultRecipient` en el código

3. **Servicio de Gmail desconectado**:
   - Ve a EmailJS → Email Services
   - Reconecta el servicio de Gmail

---

## 📊 Monitoreo de Emails

### Ver Emails Enviados

1. Ve a EmailJS dashboard
2. Clic en **"History"** (menú lateral)
3. Verás lista de emails enviados:
   - ✅ Exitosos (verde)
   - ❌ Fallidos (rojo)
4. Clic en cada email para ver detalles

### Verificar Cuota

1. EmailJS dashboard → **"Account"**
2. Ve a sección **"Usage"**
3. Verás:
   - Emails enviados este mes
   - Emails restantes
   - Fecha de reset

---

## 💰 Planes de EmailJS

### Plan Gratuito (Actual)
- 200 emails/mes
- 2 servicios de email
- 1 template
- Soporte básico
- **Perfecto para uso del dashboard**

### Plan Pagado ($9/mes)
- 1,000 emails/mes
- 3 servicios de email
- 10 templates
- Soporte prioritario
- **Solo si necesitas más volumen**

---

## 🎯 Ventajas de EmailJS vs Gmail API

| Característica | EmailJS ✅ | Gmail API |
|----------------|------------|-----------|
| Setup time | 5 minutos | 30-60 minutos |
| Complejidad | Muy simple | Complejo (OAuth) |
| Requiere autenticación | No | Sí (popup login) |
| HTML support | ✅ Sí | ✅ Sí |
| Gratis | ✅ 200/mes | ✅ Ilimitado |
| Backend necesario | ❌ No | ❌ No |
| User experience | Click → Send | Login → Click → Send |

---

## 🔒 Consideraciones de Seguridad

### ✅ Seguro

- **Public Key es público**: Es seguro exponerlo en el código
- **No hay contraseñas**: OAuth manejado por EmailJS
- **Rate limiting**: EmailJS previene spam
- **Email verificado**: Solo puedes enviar desde emails que conectaste

### ⚠️ Limitaciones

- **Recipient hardcoded**: El destinatario está fijado en el código (esto es OK para dashboards internos)
- **Límite de envíos**: 200/mes en plan gratuito

### 🛡️ Recomendaciones

1. **No expongas credenciales privadas**: Solo usa Public Key (está diseñado para ser público)
2. **Monitorea uso**: Revisa el History en EmailJS para detectar uso anormal
3. **Usa email corporativo**: Conecta tu email corporativo en EmailJS si es posible

---

## 📚 Recursos Adicionales

- [EmailJS Documentation](https://www.emailjs.com/docs/)
- [EmailJS Templates Guide](https://www.emailjs.com/docs/user-guide/creating-email-template/)
- [EmailJS FAQ](https://www.emailjs.com/docs/faq/)
- [EmailJS Support](https://www.emailjs.com/support/)

---

## ✅ Checklist Final

Antes de considerar la configuración completa:

- [ ] Cuenta creada en EmailJS
- [ ] Servicio de Gmail conectado
- [ ] Service ID copiado
- [ ] Template de email creado con `{{{html_content}}}`
- [ ] Template ID copiado
- [ ] Public Key copiado
- [ ] Configuración actualizada en dashboard-incoming.html
- [ ] Configuración actualizada en dashboard-outgoing.html
- [ ] Servidor local iniciado
- [ ] Email de prueba enviado exitosamente
- [ ] Email recibido con formato correcto

---

## 🎉 ¡Listo!

Ahora tienes envío 100% automático de emails con EmailJS:

**Flujo de Usuario:**
```
Usuario → Clic "📄 Resumen Ejecutivo"
       → Clic "📧 Compartir por Email"
       → Confirmar
       → ✅ Email enviado automáticamente (2 clics)
```

**Sin:**
- ❌ OAuth complicado
- ❌ Login popup
- ❌ Google Cloud Console
- ❌ Copy/paste
- ❌ Abrir Outlook

**Con:**
- ✅ Setup de 5 minutos
- ✅ 100% automático
- ✅ HTML completo preservado
- ✅ Gratis (200 emails/mes)

---

**Última actualización**: Febrero 2026
**Versión**: 1.0
**Proveedor**: EmailJS (www.emailjs.com)
