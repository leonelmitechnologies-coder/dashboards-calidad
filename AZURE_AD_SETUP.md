# 📘 Configuración de Azure AD para Microsoft Graph API

## Guía Completa de Configuración

Esta guía te llevará paso a paso para configurar Azure Active Directory (Azure AD) y habilitar el envío automático de emails desde los dashboards de Control de Calidad.

---

## ✅ Requisitos Previos

- Acceso de administrador a Azure AD
- Tenant de Microsoft 365 / Office 365
- Cuenta de correo corporativa de Microsoft

---

## 📋 Paso 1: Crear App Registration en Azure AD

### 1.1. Acceder al Portal de Azure

1. Navega a [Azure Portal](https://portal.azure.com)
2. Inicia sesión con tu cuenta de administrador
3. En el menú lateral izquierdo, busca y selecciona **Azure Active Directory**

### 1.2. Crear Nueva Aplicación

1. En el menú de Azure AD, ve a **App registrations** (Registros de aplicaciones)
2. Clic en **+ New registration** (+ Nuevo registro)
3. Completa el formulario:

   **Nombre de la aplicación:**
   ```
   Dashboard Quality Control - Email Sender
   ```

   **Tipos de cuenta compatibles:**
   - Selecciona: **Accounts in this organizational directory only (Single tenant)**
   - Esto es: Solo cuentas de tu organización

   **Redirect URI (URI de redireccionamiento):**
   - **Plataforma**: Selecciona `Single-page application (SPA)`
   - **URIs**: Agrega las siguientes URLs (reemplaza `yourdomain.com` con tu dominio real):
     ```
     https://yourdomain.com/dashboard-incoming.html
     https://yourdomain.com/dashboard-outgoing.html
     http://localhost:8000/dashboard-incoming.html (para pruebas locales)
     http://localhost:8000/dashboard-outgoing.html (para pruebas locales)
     ```

4. Clic en **Register** (Registrar)

### 1.3. Guardar IDs Importantes

Después de crear la aplicación, verás la página de **Overview** (Información general).

**🔑 GUARDA ESTOS VALORES (los necesitarás después):**

- **Application (client) ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

> **💡 Tip**: Copia estos IDs a un archivo de texto temporal. Los necesitarás para configurar los dashboards.

---

## 🔐 Paso 2: Configurar Permisos de API

### 2.1. Agregar Permisos de Microsoft Graph

1. En el menú lateral de tu aplicación, ve a **API permissions** (Permisos de API)
2. Clic en **+ Add a permission** (+ Agregar un permiso)
3. Selecciona **Microsoft Graph**
4. Selecciona **Delegated permissions** (Permisos delegados)
5. Busca y selecciona los siguientes permisos:
   - ✅ **User.Read** (ya está agregado por defecto)
   - ✅ **Mail.Send** (búscalo y selecciónalo)
6. Clic en **Add permissions** (Agregar permisos)

### 2.2. Otorgar Consentimiento de Administrador

**⚠️ IMPORTANTE**: Este paso es necesario para que los usuarios puedan usar la aplicación sin tener que aprobar permisos individualmente.

1. En la página de **API permissions**, clic en:
   ```
   ✓ Grant admin consent for [Tu Organización]
   ```
2. Confirma la acción clic en **Yes**
3. Verifica que aparezca una marca verde ✅ en la columna "Status"

**Resultado esperado:**
```
Permission                Type        Status
User.Read                 Delegated   ✅ Granted for [Organización]
Mail.Send                 Delegated   ✅ Granted for [Organización]
```

---

## 🔧 Paso 3: Configurar Autenticación

### 3.1. Configuración de Autenticación SPA

1. En el menú lateral, ve a **Authentication** (Autenticación)
2. Verifica que tus **Redirect URIs** estén listados bajo "Single-page application"
3. En la sección **Implicit grant and hybrid flows**:
   - ✅ Marca **Access tokens (used for implicit flows)**
   - ✅ Marca **ID tokens (used for implicit and hybrid flows)**
4. En **Advanced settings**:
   - **Allow public client flows**: Déjalo en `No`
5. Clic en **Save** (Guardar)

---

## 📝 Paso 4: Actualizar Configuración en los Dashboards

### 4.1. Abrir Archivos de Dashboard

Abre los siguientes archivos con tu editor de código:
- `dashboard-incoming.html`
- `dashboard-outgoing.html`

### 4.2. Actualizar Configuración MSAL

Busca la sección de configuración MSAL (aproximadamente línea 920):

```javascript
const MSAL_CONFIG = {
    auth: {
        clientId: 'YOUR-CLIENT-ID-HERE',  // 👈 REEMPLAZA ESTE VALOR
        authority: 'https://login.microsoftonline.com/YOUR-TENANT-ID-HERE',  // 👈 REEMPLAZA ESTE VALOR
        redirectUri: window.location.origin + window.location.pathname
    },
    // ... resto de la configuración
};
```

**Reemplaza los siguientes valores:**

1. **`YOUR-CLIENT-ID-HERE`** → Pega tu **Application (client) ID**
2. **`YOUR-TENANT-ID-HERE`** → Pega tu **Directory (tenant) ID**

**Ejemplo:**
```javascript
const MSAL_CONFIG = {
    auth: {
        clientId: 'a1b2c3d4-e5f6-7890-abcd-1234567890ab',
        authority: 'https://login.microsoftonline.com/9876fedc-ba09-8765-4321-0fedcba98765',
        redirectUri: window.location.origin + window.location.pathname
    },
    // ...
};
```

### 4.3. (Opcional) Cambiar Email Predeterminado

Si deseas cambiar el destinatario por defecto, busca:

```javascript
const EMAIL_CONFIG = {
    defaultRecipient: 'leonelhdze@gmail.com'  // 👈 Cambia este email
};
```

### 4.4. Guardar Archivos

Guarda ambos archivos después de realizar los cambios.

---

## 🧪 Paso 5: Probar la Configuración

### 5.1. Abrir Dashboard en Navegador

1. Abre tu navegador (Chrome, Edge, o Firefox recomendados)
2. Navega a tu dashboard:
   ```
   https://yourdomain.com/dashboard-incoming.html
   ```

### 5.2. Verificar Autenticación

1. Deberías ver dos badges en la esquina superior derecha:
   - **Badge superior**: "Última actualización"
   - **Badge inferior**: "No autenticado" con botón "🔐 Iniciar Sesión"

2. Clic en **"🔐 Iniciar Sesión"**

3. Se abrirá un popup de Microsoft pidiendo credenciales:
   - Ingresa tu email corporativo
   - Ingresa tu contraseña
   - Si hay autenticación de dos factores, complétala

4. **Pantalla de consentimiento**:
   - Verás: "Dashboard Quality Control - Email Sender wants to..."
   - Permisos solicitados:
     - ✅ Read your profile
     - ✅ Send mail as you
   - Clic en **Accept** (Aceptar)

5. **Login exitoso**:
   - El popup se cerrará
   - Verás un mensaje: "✅ Login exitoso. Ahora puedes enviar emails automáticamente..."
   - El badge cambiará a: "👤 [Tu Nombre]" con botón "🚪 Cerrar Sesión"

### 5.3. Probar Envío de Email

1. Genera el resumen ejecutivo:
   - Navega por el dashboard
   - Aplica filtros si deseas
   - Clic en **"📄 Resumen Ejecutivo"**

2. Compartir por email:
   - En el modal del resumen, clic en **"📧 Compartir por Email"**
   - Verás confirmación: "Se enviará el email a: leonelhdze@gmail.com"
   - Clic en **OK**

3. **Envío automático**:
   - Verás indicador de carga: "📧 Enviando email automáticamente..."
   - Después de unos segundos: "✅ Email enviado exitosamente"

4. **Verificar email recibido**:
   - Abre Outlook o tu cliente de correo
   - Revisa la bandeja de entrada de `leonelhdze@gmail.com`
   - Deberías ver el email con el resumen ejecutivo completamente formateado

---

## 🔍 Solución de Problemas (Troubleshooting)

### Error: "AADSTS50011: Reply URL mismatch"

**Causa**: La URL de redireccionamiento no coincide con las configuradas en Azure AD.

**Solución**:
1. Ve a Azure AD → Tu app → Authentication
2. Verifica que las URLs de redireccionamiento incluyan:
   - `https://yourdomain.com/dashboard-incoming.html` (exacta)
   - `https://yourdomain.com/dashboard-outgoing.html` (exacta)
3. Asegúrate de que sean HTTPS en producción
4. Guarda los cambios y vuelve a intentar

### Error: "Insufficient privileges to complete the operation"

**Causa**: El permiso `Mail.Send` no está otorgado correctamente.

**Solución**:
1. Ve a Azure AD → Tu app → API permissions
2. Verifica que `Mail.Send` esté listado
3. Verifica que tenga marca verde ✅ en "Status"
4. Si no, clic en "Grant admin consent for [Organización]"
5. Espera 5 minutos para que los cambios se propaguen
6. Cierra sesión en el dashboard y vuelve a iniciar sesión

### Error: "Popup blocked" o "popup_window_error"

**Causa**: El navegador está bloqueando popups.

**Solución**:
1. En Chrome/Edge: Busca el ícono de popup bloqueado en la barra de direcciones
2. Clic en el ícono → "Always allow popups from this site"
3. Recarga la página e intenta nuevamente

### Error: "Failed to fetch" o "Network error"

**Causa**: Problemas de conexión o CORS.

**Solución**:
1. Verifica tu conexión a internet
2. Asegúrate de que no haya firewall bloqueando:
   - `https://login.microsoftonline.com`
   - `https://graph.microsoft.com`
3. Intenta en modo incógnito para descartar extensiones del navegador

### El email no llega al destinatario

**Posibles causas y soluciones**:

1. **Email en spam**:
   - Revisa la carpeta de spam/correo no deseado
   - Marca el remitente como seguro

2. **Email incorrecto**:
   - Verifica que `EMAIL_CONFIG.defaultRecipient` tenga el email correcto
   - Guarda el archivo y recarga

3. **Permisos de buzón**:
   - Verifica que el usuario autenticado tenga permiso para enviar emails
   - Algunos tenants restringen el envío de emails

### Token expirado

**Síntoma**: Después de varias horas, el envío de email falla.

**Causa**: Los tokens en sessionStorage expiran.

**Solución**:
- Cierra sesión y vuelve a iniciar sesión
- O simplemente recarga la página e intenta nuevamente (el sistema intentará renovar el token automáticamente)

---

## 🔒 Consideraciones de Seguridad

### ✅ Buenas Prácticas Implementadas

1. **Tokens en sessionStorage**: Los tokens se borran al cerrar el navegador
2. **Sin secretos de cliente**: El `clientId` es público y seguro de exponer
3. **PKCE Flow**: Autenticación segura sin secretos en el código
4. **Permisos mínimos**: Solo `User.Read` y `Mail.Send`
5. **HTTPS requerido**: Azure AD requiere HTTPS en producción

### ⚠️ Recomendaciones Adicionales

1. **Single Tenant**: Mantén la app como "Single tenant" para evitar accesos externos
2. **Revisar logs**: Azure AD → Sign-in logs para monitorear accesos
3. **Auditoría**: Revisa periódicamente quién tiene acceso a la app
4. **Rotación**: Si sospechas compromiso, puedes rotar las claves desde Azure AD

---

## 📊 Verificación Final

Antes de considerar la configuración completa, verifica:

- [ ] App registrada en Azure AD
- [ ] Client ID y Tenant ID guardados
- [ ] Permisos `User.Read` y `Mail.Send` otorgados
- [ ] Consentimiento de administrador concedido (marca verde ✅)
- [ ] Redirect URIs configurados correctamente
- [ ] Configuración MSAL actualizada en ambos dashboards
- [ ] Login funciona correctamente (popup abre y cierra)
- [ ] Badge de autenticación muestra nombre del usuario
- [ ] Email se envía correctamente
- [ ] Email se recibe con formato correcto

---

## 🎓 Conceptos Clave

### ¿Qué es MSAL?

**Microsoft Authentication Library (MSAL)** es la biblioteca oficial de Microsoft para autenticar usuarios y obtener tokens de acceso para llamar a Microsoft Graph API.

### ¿Qué es Microsoft Graph API?

**Microsoft Graph** es la API unificada de Microsoft que permite acceder a datos y servicios de Microsoft 365 (Outlook, Teams, OneDrive, etc.). En este caso, la usamos para enviar emails.

### ¿Qué es el flujo PKCE?

**Proof Key for Code Exchange (PKCE)** es un mecanismo de seguridad para aplicaciones públicas (como SPAs) que no pueden almacenar secretos de forma segura. Permite autenticación OAuth 2.0 sin exponer secretos.

### ¿Por qué necesito "Grant admin consent"?

El consentimiento de administrador permite que todos los usuarios de tu organización usen la app sin tener que aprobar permisos individualmente. Sin esto, cada usuario vería una pantalla de consentimiento en su primer uso.

---

## 📞 Soporte

Si tienes problemas adicionales:

1. **Logs del navegador**: Abre Developer Tools (F12) → Console para ver errores
2. **Logs de Azure AD**: Azure Portal → Azure AD → Sign-in logs
3. **Documentación oficial**: [Microsoft Graph API Docs](https://learn.microsoft.com/en-us/graph/)

---

## 🎉 ¡Listo!

Has completado la configuración de Azure AD para Microsoft Graph API. Ahora tus dashboards pueden enviar emails automáticamente sin intervención manual.

**Beneficios logrados:**
- ✅ Envío 100% automático de emails
- ✅ Sin copy/paste manual
- ✅ Sin abrir Outlook manualmente
- ✅ Formato HTML completo preservado
- ✅ Seguridad empresarial con Azure AD

---

**Última actualización**: Febrero 2026
**Versión**: 1.0
