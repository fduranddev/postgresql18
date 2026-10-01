<#
.SYNOPSIS
  Supervision des sessions PostgreSQL via Npgsql.dll

.DESCRIPTION
  Affiche les sessions actives, les sessions en attente, les requêtes longues,
  les sessions par utilisateur et par base. Compatible PostgreSQL 10+.

  Dépendance : Npgsql.dll
#>

# ------------------------------
# CONFIGURATIONclear
# ------------------------------

# Charger DLL
Add-Type -Path "/mnt/c/Tools/Npgsql/Microsoft.Extensions.Logging.Abstractions.dll"
Add-Type -Path "/mnt/c/Tools/Npgsql/Npgsql.dll"

# Connexion PostgreSQL
$connectionString = "Host=localhost;Port=5436;Username=postgres;Password=admin;Database=dvdrental;"

# Durée max des requêtes (en secondes)
$LongQueryThreshold = 30

# Export CSV ? (true/false)
$ExportCSV = $true
$CSVPath = "/mnt/c/Temp/supervision_pg.csv"

# ------------------------------
# FONCTION : Exécution SQL
# ------------------------------
function Invoke-PgQuery {
    param(
        [string]$Query
    )

    $conn = New-Object Npgsql.NpgsqlConnection($connectionString)

    try {
        $conn.Open()
        $cmd = New-Object Npgsql.NpgsqlCommand($Query, $conn)
        $reader = $cmd.ExecuteReader()

        $table = New-Object System.Data.DataTable
        $table.Load($reader)
        return $table
    }
    catch {
        Write-Host "Erreur SQL : $($_.Exception.Message)"
        return $null
    }
    finally {
        $conn.Close()
    }
}

# ------------------------------
# 1️⃣ nombre total de sessions
# ------------------------------
$queryTotal = "SELECT COUNT(*)::int AS total_sessions FROM pg_stat_activity;"
$totalSessions = Invoke-PgQuery -Query $queryTotal
$total = if ($totalSessions -and $totalSessions.Rows.Count -gt 0) { $totalSessions.Rows[0]["total_sessions"] } else { 0 }

# ------------------------------
# 2️⃣ sessions actives
# ------------------------------
$queryActive = @"
SELECT pid, usename, datname, state, query_start, query
FROM pg_stat_activity
WHERE state = 'active';
"@
$activeSessions = Invoke-PgQuery -Query $queryActive
$activeCount = if ($activeSessions) { $activeSessions.Rows.Count } else { 0 }

# ------------------------------
# 3️⃣ sessions en attente (locks)
# ------------------------------
$queryWaiting = @"
SELECT pid, usename, datname, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE wait_event_type IS NOT NULL;
"@
$waitingSessions = Invoke-PgQuery -Query $queryWaiting
$waitingCount = if ($waitingSessions) { $waitingSessions.Rows.Count } else { 0 }

# ------------------------------
# 4️⃣ sessions par utilisateur
# ------------------------------
$queryByUser = @"
SELECT usename, COUNT(*) AS nb_sessions
FROM pg_stat_activity
GROUP BY usename
ORDER BY nb_sessions DESC;
"@
$sessionsByUser = Invoke-PgQuery -Query $queryByUser

# ------------------------------
# 5️⃣ sessions par base
# ------------------------------
$queryByDb = @"
SELECT datname, COUNT(*) AS nb_sessions
FROM pg_stat_activity
GROUP BY datname
ORDER BY nb_sessions DESC;
"@
$sessionsByDb = Invoke-PgQuery -Query $queryByDb

# ------------------------------
# 6️⃣ requêtes longues
# ------------------------------
$queryLong = @"
SELECT pid, usename, datname, now() - query_start AS duree, query
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '$LongQueryThreshold seconds'
ORDER BY duree DESC;
"@
$longQueries = Invoke-PgQuery -Query $queryLong

# ------------------------------
# AFFICHAGE
# ------------------------------
Write-Host "================================================================="
Write-Host " 🔎 SUPERVISION POSTGRESQL ($(Get-Date))"
Write-Host "================================================================="
Write-Host ""
Write-Host "➡ Total sessions            : $total"
Write-Host "➡ Sessions actives          : $activeCount"
Write-Host "➡ Sessions en attente       : $waitingCount"
Write-Host ""

Write-Host "---- Sessions par utilisateur ----"
if ($sessionsByUser) { $sessionsByUser | Format-Table -AutoSize }

Write-Host "---- Sessions par base ----"
if ($sessionsByDb) { $sessionsByDb | Format-Table -AutoSize }

Write-Host "---- Sessions actives ----"
if ($activeSessions) { $activeSessions | Format-Table -AutoSize }

Write-Host "---- Sessions en attente ----"
if ($waitingSessions) { $waitingSessions | Format-Table -AutoSize }

Write-Host "---- Requêtes longues (> $LongQueryThreshold s) ----"
if ($longQueries) { $longQueries | Format-Table -AutoSize }

# ------------------------------
# EXPORT CSV
# ------------------------------
if ($ExportCSV -eq $true -and $activeSessions) {

    $export = [System.Collections.Generic.List[psobject]]::new()

    foreach ($row in $activeSessions) {
        $export.Add([pscustomobject]@{
            Timestamp = (Get-Date)
            PID       = $row.pid
            User      = $row.usename
            Database  = $row.datname
            State     = $row.state
            QueryStart= $row.query_start
            Query     = $row.query
        })
    }

    $export | Export-Csv -Path $CSVPath -NoTypeInformation -Encoding UTF8

    Write-Host ""
    Write-Host "📁 Export CSV généré : $CSVPath"
}

Write-Host ""
Write-Host "✔ Supervision terminée."
