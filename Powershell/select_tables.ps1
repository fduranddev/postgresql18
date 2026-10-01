# Charger d'abord la DLL de logging
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"

# Chemin vers Npgsql.dll
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

# Chaîne de connexion
$connectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=postgres;"

$conn = New-Object Npgsql.NpgsqlConnection($connectionString)
$conn.Open()

$sql = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_type='BASE TABLE';"
$cmd = New-Object Npgsql.NpgsqlCommand($sql, $conn)
$reader = $cmd.ExecuteReader()
while ($reader.Read()) {
    Write-Host "$($reader["table_schema"]).$($reader["table_name"])"
}
$reader.Close()
