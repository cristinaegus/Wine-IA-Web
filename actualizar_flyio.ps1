# Script para actualizar la configuración de Fly.io con el modelo Groq correcto

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ACTUALIZAR CONFIGURACIÓN FLY.IO - GROQ" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. Verificar que flyctl esté instalado
Write-Host "`n[1/4] Verificando Fly.io CLI..." -ForegroundColor Yellow
$flyctlVersion = flyctl version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Fly.io CLI no está instalado" -ForegroundColor Red
    Write-Host "   Instalar con: iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Fly.io CLI instalado: $flyctlVersion" -ForegroundColor Green

# 2. Verificar que estés autenticado
Write-Host "`n[2/4] Verificando autenticación..." -ForegroundColor Yellow
$authCheck = flyctl auth whoami 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: No estás autenticado en Fly.io" -ForegroundColor Red
    Write-Host "   Ejecutar: flyctl auth login" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Autenticado como: $authCheck" -ForegroundColor Green

# 3. Actualizar secretos (API Key)
Write-Host "`n[3/4] Actualizando secretos en Fly.io..." -ForegroundColor Yellow

# Leer API key del archivo .env
$envFile = ".env"
if (Test-Path $envFile) {
    $groqApiKey = (Get-Content $envFile | Select-String "GROQ_API_KEY").ToString().Split("=")[1].Trim()
    
    if ($groqApiKey) {
        Write-Host "✓ API Key encontrada en .env" -ForegroundColor Green
        
        $confirm = Read-Host "¿Actualizar GROQ_API_KEY en Fly.io? (S/N)"
        if ($confirm -eq "S" -or $confirm -eq "s") {
            flyctl secrets set "GROQ_API_KEY=$groqApiKey"
            Write-Host "✓ GROQ_API_KEY actualizada en Fly.io" -ForegroundColor Green
        } else {
            Write-Host "⚠️  GROQ_API_KEY no actualizada" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  No se encontró GROQ_API_KEY en .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "   Configurar manualmente: flyctl secrets set GROQ_API_KEY=tu_api_key" -ForegroundColor Yellow
}

# 4. Desplegar aplicación
Write-Host "`n[4/4] Desplegando aplicación actualizada..." -ForegroundColor Yellow

$confirm = Read-Host "¿Desplegar la aplicación ahora? (S/N)"
if ($confirm -eq "S" -or $confirm -eq "s") {
    Write-Host "`nIniciando despliegue..." -ForegroundColor Cyan
    flyctl deploy
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ DESPLIEGUE COMPLETADO" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host "Cambios aplicados:" -ForegroundColor White
        Write-Host "  • Modelo actualizado: llama-3.3-70b-versatile" -ForegroundColor White
        Write-Host "  • API Key configurada en secretos" -ForegroundColor White
        Write-Host "  • Aplicación desplegada" -ForegroundColor White
        Write-Host "================================================" -ForegroundColor Cyan
        Write-Host "`nAccede a tu aplicación en:" -ForegroundColor Yellow
        flyctl status | Select-String "Hostname"
    } else {
        Write-Host "`n❌ ERROR EN EL DESPLIEGUE" -ForegroundColor Red
        Write-Host "Revisar logs con: flyctl logs" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n⚠️  Despliegue cancelado" -ForegroundColor Yellow
    Write-Host "   Desplegar manualmente: flyctl deploy" -ForegroundColor Yellow
}

Write-Host "`n================================================" -ForegroundColor Cyan
