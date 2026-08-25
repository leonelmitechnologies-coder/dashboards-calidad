# Registra una tarea en Windows Task Scheduler que actualiza los datos
# del dashboard cada 6 horas, de lunes a viernes.
# Ejecutar una sola vez como Administrador.

$TaskName   = "DashboardCalidad-ActualizarRechazos"
$ScriptPath = "C:\Proyectos Claude\dashboards-calidad\actualizar_datos.bat"
$LogPath    = "C:\Proyectos Claude\dashboards-calidad\logs\tarea.log"

# Verifica que el bat exista
if (-not (Test-Path $ScriptPath)) {
    Write-Error "No se encontro: $ScriptPath"
    exit 1
}

# Crea carpeta de logs si no existe
$LogDir = Split-Path $LogPath
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }

# Accion: correr el bat y redirigir salida al log
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$ScriptPath`" >> `"$LogPath`" 2>&1"

# Disparadores: 8am, 2pm y 8pm de lunes a viernes
$Triggers = @(
    New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "08:00",
    New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "14:00",
    New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "20:00"
)

# Configuracion: correr aunque el usuario no este logueado, no detener si tarda
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Registrar (o actualizar si ya existe)
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Triggers `
    -Settings $Settings `
    -RunLevel Highest `
    -Description "Actualiza rechazos_data.json desde Nextcloud y hace push a GitHub" | Out-Null

Write-Host "Tarea registrada: $TaskName"
Write-Host "Se ejecutara a las 8:00am, 2:00pm y 8:00pm de lunes a viernes."
Write-Host ""
Write-Host "Para lanzarla ahora mismo:"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
