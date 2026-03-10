from pathlib import Path


def test_initial_migration_contains_core_tables() -> None:
    migration = Path("alembic/versions/20260310_0001_initial_schema.py").read_text()
    for table in [
        "users",
        "roles",
        "strategies",
        "trades",
        "positions",
        "risk_metrics",
        "margin_metrics",
        "audit_logs",
        "file_import_batches",
        "task_execution_history",
    ]:
        assert f'"{table}"' in migration
