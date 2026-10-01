# ------------------------------
# SCRIPT D'UTILISATION DU MODULE PgSupervision
# ------------------------------

# Import du module
Import-Module "/mnt/c/Tools/PgSupervision/PgSupervision.psm1"

# Définir la chaîne de connexion PostgreSQL
$ConnectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=dvdrental;"

# ------------------------------
# 1️⃣ Toutes les sessions
# ------------------------------
Write-Host "---- Toutes les sessions ----"
$sessions = Get-PgSessions -ConnectionString $ConnectionString
$sessions | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 2️⃣ Sessions actives
# ------------------------------
Write-Host "---- Sessions actives ----"
$active = Get-PgActiveSessions -ConnectionString $ConnectionString
$active | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 3️⃣ Sessions en attente
# ------------------------------
Write-Host "---- Sessions en attente ----"
$waiting = Get-PgWaitingSessions -ConnectionString $ConnectionString
$waiting | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 4️⃣ Requêtes longues (> 30s)
# ------------------------------
$ThresholdSeconds = 30
Write-Host "---- Requêtes longues (> $ThresholdSeconds s) ----"
$long = Get-PgLongQueries -ConnectionString $ConnectionString -ThresholdSeconds $ThresholdSeconds
$long | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 5️⃣ Sessions par utilisateur
# ------------------------------
Write-Host "---- Sessions par utilisateur ----"
$queryUser = @"
SELECT usename, COUNT(*) AS nb_sessions
FROM pg_stat_activity
GROUP BY usename
ORDER BY nb_sessions DESC;
"@
$userSessions = Invoke-PgQuery -ConnectionString $ConnectionString -Query $queryUser
$userSessions | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 6️⃣ Sessions par base
# ------------------------------
Write-Host "---- Sessions par base ----"
$queryDb = @"
SELECT datname, COUNT(*) AS nb_sessions
FROM pg_stat_activity
GROUP BY datname
ORDER BY nb_sessions DESC;
"@
$dbSessions = Invoke-PgQuery -ConnectionString $ConnectionString -Query $queryDb
$dbSessions | Format-Table -AutoSize
Write-Host ""

# ------------------------------
# 7️⃣ Export CSV des sessions actives
# ------------------------------
$CsvPath = "/mnt/c/Temp/pg_active_sessions.csv"
Export-PgSessionsCsv -Data $active -Path $CsvPath
Write-Host ""

Write-Host "✔ Supervision terminée. CSV disponible : $CsvPath"
