# Charger DLL
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

$config = Get-Content "config.json" | ConvertFrom-Json

$connectionString = "Host=$($config.Host);Port=$($config.Port);Username=$($config.User);Password=$($config.Password);Database=$($config.Database);"

$conn = New-Object Npgsql.NpgsqlConnection($connectionString)
$conn.Open()

Write-Host "Connexion OK via JSON config !"

$conn.Close()
