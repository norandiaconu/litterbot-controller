$filePath = "$PSScriptRoot\config.py"
if ($args[0] -eq 'd') {
    Remove-Item $filePath
    Write-Host "Config Deleted"
}
if(-Not(Test-Path -Path $filePath)) {
    Write-Host "Creating new config"
    New-Item -Name "config.py" -Path $PSScriptRoot -ItemType File | Out-Null
    $username = Read-Host -Prompt "Username"
    $password = Read-Host -Prompt "Password"
    Add-Content -Path $filePath -Value "username = '$username'"
    Add-Content -Path $filePath -Value "password = '$password'"
}
py "$PSScriptRoot\controller.py" $args[0]
