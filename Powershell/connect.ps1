# Sous Windows
#Import-Module "C:\Postgresql18\Powershell\PostgreSQLCmdlets\PostgreSQLCmdlets.psd1"

# Sous WSL2
Import-Module "/mnt/c/Postgresql18/Powershell/PostgreSQLCmdlets/PostgreSQLCmdlets.psd1"

$server = "127.0.0.1"
$port = "5433"
$database = "dvdrental"
$user = "postgres"
$password = "admin"

$postgresql = Connect-PostgreSQL `
    -Server $server `
    -Port $port `
    -Database $database `
    -User $user `
    -Password $password

 
  $postgresql
# Vérification
Write-Host "Connexion réussie !" 

Write-Host " Version de Postgresql"
Invoke-PostgreSQL -Connection $postgresql -Query "SELECT version();"

Write-Host "Film: Agent Truman"

$film = Select-PostgreSQL -Connection $postgresql -Table "public.film" -Where "title = 'Agent Truman'"
$film | Format-Table

$film1 = Invoke-PostgreSQL -Connection $postgresql -Query 'SELECT title, description FROM public.film WHERE film_id=6;'
$film1 | Format-Table
