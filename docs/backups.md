# Postgres Backup and Restore

## Strategy scaffold

- Frequency: at least daily full logical backup + before every schema migration
- Retention: 7 daily, 4 weekly, 6 monthly (adjust for policy)
- Integrity: generate SHA256 checksum for every backup
- Off-host copy: replicate encrypted backup artifacts to secondary storage

## Backup command

```bash
./infra/scripts/backup-db.sh
```

Artifacts are written to `./backups/`:

- `postgres_<db>_<timestamp>.sql.gz`
- `postgres_<db>_<timestamp>.sql.gz.sha256`

## Verify backup integrity

```bash
sha256sum -c backups/postgres_<db>_<timestamp>.sql.gz.sha256
```

## Restore command

```bash
./infra/scripts/restore-db.sh backups/postgres_<db>_<timestamp>.sql.gz
```

Restore behavior:

- 10-second safety delay before execution
- Streams decompressed SQL into `psql` inside `db` container

## Suggested automation (cron example)

Run at 02:30 daily as deployment user:

```cron
30 2 * * * cd /srv/neuroquant && ./infra/scripts/backup-db.sh >> /var/log/neuroquant-backup.log 2>&1
```

## Redis persistence note

Redis is configured with append-only file (`--appendonly yes`) and periodic snapshots (`--save 60 1000`).
This supports broker durability but does not replace Postgres backups.

