# Sous WSL2
Import-Module "/mnt/c/Postgresql18/Powershell/PostgreSQLCmdlets/PostgreSQLCmdlets.psd1"

# Connexion à la base
$postgresql = Connect-PostgreSQL -Server "127.0.0.1" -Port 5433 -Database "dvdrental" -User "postgres" -Password "admin"

# Chemin du CSV exporté
$csvFile = "/mnt/c/Postgresql18/Backup/film_20251127_182038.csv"

# Lire le CSV
$data = Import-Csv -Path $csvFile

# Insérer les lignes dans la table
foreach ($row in $data) {
    $columns = $row.PSObject.Properties.Name -join ", "
    $values = $row.PSObject.Properties.Value | ForEach-Object { "'$_'" } -join ", "
    $query = "INSERT INTO public.film ($columns) VALUES ($values);"
    Invoke-PostgreSQL -Connection $postgresql -Query $query
}

Write-Host "Restauration terminée pour la table film"
