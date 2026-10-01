# Sous Windows
#Import-Module "C:\Postgresql18\Powershell\PostgreSQLCmdlets\PostgreSQLCmdlets.psd1"

# Sous WSL2
Import-Module "/mnt/c/Postgresql18/Powershell/PostgreSQLCmdlets/PostgreSQLCmdlets.psd1"

# Connexion
$postgresql = Connect-PostgreSQL -Server "127.0.0.1" -Port 5433 -Database "dvdrental" -User "postgres" -Password "admin"

# Export de la table "film" en CSV
$filmData = Select-PostgreSQL -Connection $postgresql -Table "public.film"
$filmData | Export-Csv -Path "/mnt/c/Postgresql18/Backup/film_$(Get-Date -Format yyyyMMdd_HHmmss).csv" -NoTypeInformation

Write-Host "Sauvegarde table film terminée"




