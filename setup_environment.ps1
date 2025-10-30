# HAL Environment Setup Script
# This script configures environment variables for the HAL AI Assistant

Write-Host "HAL AI Assistant - Environment Configuration" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Function to prompt for value with default
function Get-ConfigValue {
    param(
        [string]$VariableName,
        [string]$Description,
        [string]$DefaultValue
    )
    
    Write-Host "$Description" -ForegroundColor Yellow
    Write-Host "Current default: $DefaultValue" -ForegroundColor Gray
    $value = Read-Host "Enter value (press Enter to use default)"
    
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $DefaultValue
    }
    return $value
}

# Function to test if path exists
function Test-PathExists {
    param([string]$Path)
    return Test-Path $Path
}

Write-Host "Configuring HAL environment variables..." -ForegroundColor Green
Write-Host ""

# Python Path
$pythonPath = Get-ConfigValue `
    -VariableName "HAL_PYTHON_PATH" `
    -Description "Python executable path" `
    -DefaultValue "C:\Python312\python.exe"

if (-not (Test-PathExists $pythonPath)) {
    Write-Host "WARNING: Python executable not found at: $pythonPath" -ForegroundColor Red
    Write-Host "Please verify the path is correct." -ForegroundColor Red
}

# Script Path
$scriptPath = Get-ConfigValue `
    -VariableName "HAL_SCRIPT_PATH" `
    -Description "AI handler script path" `
    -DefaultValue "C:\QMSYS\HAL\PY\ai_handler.py"

if (-not (Test-PathExists $scriptPath)) {
    Write-Host "WARNING: Script not found at: $scriptPath" -ForegroundColor Red
    Write-Host "Please verify the path is correct." -ForegroundColor Red
}

# Ollama Host
$ollamaHost = Get-ConfigValue `
    -VariableName "OLLAMA_HOST" `
    -Description "Ollama server hostname or IP" `
    -DefaultValue "ubuai.q.lcs.ai"

# Ollama Port
$ollamaPort = Get-ConfigValue `
    -VariableName "OLLAMA_PORT" `
    -Description "Ollama server port" `
    -DefaultValue "11434"

Write-Host ""
Write-Host "Configuration Summary:" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host "HAL_PYTHON_PATH: $pythonPath"
Write-Host "HAL_SCRIPT_PATH: $scriptPath"
Write-Host "OLLAMA_HOST: $ollamaHost"
Write-Host "OLLAMA_PORT: $ollamaPort"
Write-Host ""

# Ask for scope
Write-Host "Select environment variable scope:" -ForegroundColor Yellow
Write-Host "1. User (current user only)"
Write-Host "2. Machine (all users - requires admin)"
Write-Host "3. Process (current session only)"
$scope = Read-Host "Enter choice (1-3)"

switch ($scope) {
    "1" { $envScope = "User" }
    "2" { $envScope = "Machine" }
    "3" { $envScope = "Process" }
    default { 
        Write-Host "Invalid choice. Using User scope." -ForegroundColor Yellow
        $envScope = "User" 
    }
}

Write-Host ""
Write-Host "Setting environment variables with scope: $envScope" -ForegroundColor Green

try {
    if ($envScope -eq "Process") {
        # Set for current session only
        $env:HAL_PYTHON_PATH = $pythonPath
        $env:HAL_SCRIPT_PATH = $scriptPath
        $env:OLLAMA_HOST = $ollamaHost
        $env:OLLAMA_PORT = $ollamaPort
        Write-Host "Environment variables set for current session." -ForegroundColor Green
    } else {
        # Set permanently
        [System.Environment]::SetEnvironmentVariable("HAL_PYTHON_PATH", $pythonPath, $envScope)
        [System.Environment]::SetEnvironmentVariable("HAL_SCRIPT_PATH", $scriptPath, $envScope)
        [System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", $ollamaHost, $envScope)
        [System.Environment]::SetEnvironmentVariable("OLLAMA_PORT", $ollamaPort, $envScope)
        
        # Also set for current session
        $env:HAL_PYTHON_PATH = $pythonPath
        $env:HAL_SCRIPT_PATH = $scriptPath
        $env:OLLAMA_HOST = $ollamaHost
        $env:OLLAMA_PORT = $ollamaPort
        
        Write-Host "Environment variables set permanently ($envScope level)." -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Configuration completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Verification:" -ForegroundColor Cyan
    Write-Host "HAL_PYTHON_PATH = $env:HAL_PYTHON_PATH"
    Write-Host "HAL_SCRIPT_PATH = $env:HAL_SCRIPT_PATH"
    Write-Host "OLLAMA_HOST = $env:OLLAMA_HOST"
    Write-Host "OLLAMA_PORT = $env:OLLAMA_PORT"
    Write-Host ""
    
    if ($envScope -ne "Process") {
        Write-Host "NOTE: You may need to restart OpenQM or your terminal for changes to take effect." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "ERROR: Failed to set environment variables." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($envScope -eq "Machine") {
        Write-Host "TIP: Machine-level variables require administrator privileges." -ForegroundColor Yellow
        Write-Host "Try running PowerShell as Administrator or use User scope instead." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
