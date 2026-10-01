#!/bin/bash
DATA_DIR="/var/lib/pgsql/18/data"

# Initialiser la base si nécessaire
if [ ! -f "$DATA_DIR/PG_VERSION" ]; then
    /usr/pgsql-18/bin/initdb -D "$DATA_DIR"
fi

# Configurer PostgreSQL pour écouter toutes les interfaces
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" $DATA_DIR/postgresql.conf
sed -i "s/#port = 5432/port = 5432/g" $DATA_DIR/postgresql.conf

# Autoriser toutes les connexions TCP
echo "host all all 0.0.0.0/0 trust" >> $DATA_DIR/pg_hba.conf

# Démarrer PostgreSQL au premier plan (PID 1)
exec /usr/pgsql-18/bin/postgres -D "$DATA_DIR"

