source .env
export PGPASSWORD=$DB_PASSWORD

psql -h $DB_HOST -U $DB_USERNAME -p $DB_PORT -d $DB_NAME -f schema.sql
psql -h $DB_HOST -U $DB_USERNAME -p $DB_PORT -d $DB_NAME -f seed_db.sql