# Charger DLL
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

# Chaîne de connexion vers la base employe
$connectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=employe;"

$conn = New-Object Npgsql.NpgsqlConnection($connectionString)
try {
    $conn.Open()
    
    $sql = "SELECT id_employe, nom_employe, prenom_employe, age_employe, salaire_employe FROM public.employe;"
    $cmd = New-Object Npgsql.NpgsqlCommand($sql, $conn)
    $reader = $cmd.ExecuteReader()
    
    while ($reader.Read()) {
        Write-Host "ID: $($reader['id_employe']) | Nom: $($reader['nom_employe']) | Prénom: $($reader['prenom_employe']) | Age: $($reader['age_employe']) | Salaire: $($reader['salaire_employe'])"
    }
    
    $reader.Close()
}
finally {
    $conn.Close()
}
