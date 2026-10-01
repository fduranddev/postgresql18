# Charger DLL
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

# Chaîne de connexion vers la base employe
$connectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=employe;"

$conn = New-Object Npgsql.NpgsqlConnection($connectionString)
try {
    $conn.Open()
    
    $sql = "INSERT INTO public.employe( nom_employe, prenom_employe, age_employe, salaire_employe) VALUES ('Battle','Véronique','45','50000.00');"
    $cmd = New-Object Npgsql.NpgsqlCommand($sql, $conn)

    $rows = $cmd.ExecuteNonQuery()
    
    Write-Host "$rows ligne(s) insérée(s)."
}
finally {
    $conn.Close()
}
