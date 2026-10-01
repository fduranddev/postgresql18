# Charger d'abord la DLL de logging
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"

# Chemin vers Npgsql.dll
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

# Chaîne de connexion
$connectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=postgres;"

# Création de l'objet connexion
$conn = New-Object Npgsql.NpgsqlConnection($connectionString)

try {
    $conn.Open()
    Write-Host "Connexion réussie !"
}
catch {
    Write-Host "Erreur de connexion : $($_.Exception.Message)"
}
finally {
    $conn.Close()
}
