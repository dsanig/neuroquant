"""initial schema

Revision ID: 20260310_0001
Revises:
Create Date: 2026-03-10
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260310_0001"
down_revision = None
branch_labels = None
depends_on = None


def audit_columns():
    return [
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("updated_by", sa.String(255), nullable=True),
        sa.Column("source_system", sa.String(100), nullable=True),
        sa.Column("source_file", sa.String(255), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    ]


def upgrade() -> None:
    op.create_table("users", *audit_columns(), sa.Column("email", sa.String(255), unique=True, nullable=False), sa.Column("full_name", sa.String(255), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.create_table("roles", *audit_columns(), sa.Column("name", sa.String(100), unique=True, nullable=False))
    op.create_table("user_roles", *audit_columns(), sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False), sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id"), nullable=False))
    op.create_table("instruments", *audit_columns(), sa.Column("symbol", sa.String(24), unique=True, nullable=False), sa.Column("underlying", sa.String(24), nullable=False), sa.Column("instrument_type", sa.String(32), nullable=False))
    op.create_table("firms", *audit_columns(), sa.Column("name", sa.String(150), unique=True, nullable=False), sa.Column("legal_name", sa.String(255), nullable=True), sa.Column("base_currency", sa.String(3), nullable=False, server_default="USD"), sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.create_table("broker_accounts", *audit_columns(), sa.Column("firm_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("firms.id"), nullable=False), sa.Column("account_number", sa.String(64), unique=True, nullable=False), sa.Column("broker_name", sa.String(100), nullable=False))
    op.create_table("strategies", *audit_columns(), sa.Column("name", sa.String(120), unique=True, nullable=False), sa.Column("description", sa.Text(), nullable=True))
    op.create_table("option_contracts", *audit_columns(), sa.Column("instrument_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("instruments.id"), nullable=True), sa.Column("underlying", sa.String(16), nullable=False), sa.Column("expiry", sa.Date(), nullable=False), sa.Column("strike", sa.Numeric(12, 4), nullable=False), sa.Column("option_type", sa.String(4), nullable=False), sa.Column("multiplier", sa.Integer(), nullable=False, server_default="100"))
    op.create_table("positions", *audit_columns(), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=False), sa.Column("broker_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("broker_accounts.id"), nullable=False), sa.Column("option_contract_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("option_contracts.id"), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("avg_price", sa.Numeric(16, 6), nullable=False), sa.Column("mark_price", sa.Numeric(16, 6), nullable=True), sa.Column("realized_pnl", sa.Numeric(18, 6), nullable=False, server_default="0"))
    op.create_table("trades", *audit_columns(), sa.Column("broker_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("broker_accounts.id"), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=False), sa.Column("option_contract_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("option_contracts.id"), nullable=True), sa.Column("external_trade_id", sa.String(128), nullable=False), sa.Column("symbol", sa.String(24), nullable=False), sa.Column("side", sa.String(8), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("price", sa.Numeric(16, 6), nullable=False), sa.Column("premium", sa.Numeric(16, 6), nullable=True), sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False), sa.Column("roll_group_id", sa.String(64), nullable=True), sa.UniqueConstraint("broker_account_id", "external_trade_id", name="uq_trade_external"))
    op.create_table("greeks_snapshots", *audit_columns(), sa.Column("snapshot_at", sa.DateTime(timezone=True), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("instrument_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("instruments.id"), nullable=True), sa.Column("delta", sa.Numeric(18, 6), nullable=False), sa.Column("gamma", sa.Numeric(18, 6), nullable=False), sa.Column("theta", sa.Numeric(18, 6), nullable=False), sa.Column("vega", sa.Numeric(18, 6), nullable=True), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("risk_metrics", *audit_columns(), sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("instrument_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("instruments.id"), nullable=True), sa.Column("metric_name", sa.String(64), nullable=False), sa.Column("metric_value", sa.Numeric(20, 6), nullable=False), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("margin_metrics", *audit_columns(), sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("notional_exposure", sa.Numeric(20, 4), nullable=False), sa.Column("capital_at_risk", sa.Numeric(20, 4), nullable=False, server_default="0"), sa.Column("margin_used", sa.Numeric(20, 4), nullable=False), sa.Column("broker_requirement", sa.Numeric(20, 4), nullable=True), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("performance_snapshots", *audit_columns(), sa.Column("snapshot_date", sa.Date(), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("nav", sa.Numeric(18, 4), nullable=False), sa.Column("pnl_day", sa.Numeric(18, 4), nullable=False), sa.Column("pnl_mtd", sa.Numeric(18, 4), nullable=True), sa.Column("pnl_ytd", sa.Numeric(18, 4), nullable=True), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("income_events", *audit_columns(), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("event_date", sa.Date(), nullable=False), sa.Column("amount", sa.Numeric(18, 4), nullable=False), sa.Column("event_type", sa.String(32), nullable=False))
    op.create_table("audit_logs", *audit_columns(), sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True), sa.Column("event_type", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(100), nullable=False), sa.Column("entity_id", sa.String(64), nullable=False), sa.Column("payload", sa.JSON(), nullable=False))
    op.create_table("file_import_batches", *audit_columns(), sa.Column("filename", sa.String(255), nullable=False), sa.Column("source_checksum", sa.String(128), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("row_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("imported_count", sa.Integer(), nullable=False, server_default="0"), sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"), sa.UniqueConstraint("source_checksum", name="uq_file_import_checksum"))
    op.create_table("file_import_rows", *audit_columns(), sa.Column("import_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("file_import_batches.id"), nullable=False), sa.Column("row_number", sa.Integer(), nullable=False), sa.Column("raw_payload", sa.JSON(), nullable=False), sa.Column("entity_type", sa.String(64), nullable=True), sa.Column("entity_id", sa.String(64), nullable=True), sa.Column("status", sa.String(32), nullable=False, server_default="pending"), sa.Column("error_message", sa.Text(), nullable=True))
    op.create_table("task_execution_history", *audit_columns(), sa.Column("task_name", sa.String(255), nullable=False), sa.Column("celery_task_id", sa.String(128), nullable=True), sa.Column("status", sa.String(32), nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True), sa.Column("metadata_json", sa.JSON(), nullable=True))


def downgrade() -> None:
    for table in ["task_execution_history", "file_import_rows", "file_import_batches", "audit_logs", "income_events", "performance_snapshots", "margin_metrics", "risk_metrics", "greeks_snapshots", "trades", "positions", "option_contracts", "strategies", "broker_accounts", "firms", "instruments", "user_roles", "roles", "users"]:
        op.drop_table(table)
