$filePath = "config.py"
if(Test-Path -Path $filePath) {
    Write-Host "Config loaded"
} else {
    New-Item -Name "config.py" -ItemType File | Out-Null
    $username = Read-Host -Prompt "Username"
    $password = Read-Host -Prompt "Password"
    Add-Content -Path "config.py" -Value "username = '$username'"
    Add-Content -Path "config.py" -Value "password = '$password'"
}
py controller.py
