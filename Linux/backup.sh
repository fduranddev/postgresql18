#!/usr/bin/bash

CONTAINER="pg18_a"
BACKUP_DIR="/home/durandf/sauvegardes"
BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"

# Vérifier le dossier hôte
mkdir -p "$BACKUP_DIR"

echo "🔄 Sauvegarde des bases depuis le container PostgreSQL..."
echo "➡ Container: $CONTAINER"
echo "➡ Fichier:   $BACKUP_FILE"

# Exécuter pg_dumpall depuis le container
podman exec $CONTAINER pg_dumpall -U postgres > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Sauvegarde terminée avec succès !"
    echo "📁 Fichier : $BACKUP_FILE"
else
    echo "❌ Échec de la sauvegarde."
fi
