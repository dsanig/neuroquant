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
        sa.Column("import_batch_id", sa.String(64), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    ]


def upgrade() -> None:
    op.create_table("users", *audit_columns(), sa.Column("email", sa.String(255), unique=True, nullable=False), sa.Column("full_name", sa.String(255), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False))
    op.create_table("roles", *audit_columns(), sa.Column("name", sa.String(100), unique=True, nullable=False))
    op.create_table("user_roles", *audit_columns(), sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False), sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id"), nullable=False))
    op.create_table("broker_accounts", *audit_columns(), sa.Column("account_number", sa.String(64), unique=True, nullable=False), sa.Column("broker_name", sa.String(100), nullable=False))
    op.create_table("strategies", *audit_columns(), sa.Column("name", sa.String(120), unique=True, nullable=False), sa.Column("description", sa.Text(), nullable=True))
    op.create_table("option_contracts", *audit_columns(), sa.Column("underlying", sa.String(16), nullable=False), sa.Column("expiry", sa.Date(), nullable=False), sa.Column("strike", sa.Float(), nullable=False), sa.Column("option_type", sa.String(4), nullable=False), sa.Column("multiplier", sa.Integer(), nullable=False, server_default="100"))
    op.create_table("positions", *audit_columns(), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=False), sa.Column("broker_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("broker_accounts.id"), nullable=False), sa.Column("option_contract_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("option_contracts.id"), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("avg_price", sa.Float(), nullable=False))
    op.create_table("trades", *audit_columns(), sa.Column("broker_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("broker_accounts.id"), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=False), sa.Column("option_contract_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("option_contracts.id"), nullable=True), sa.Column("external_trade_id", sa.String(128), nullable=False), sa.Column("symbol", sa.String(24), nullable=False), sa.Column("side", sa.String(8), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("price", sa.Float(), nullable=False), sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False), sa.Column("roll_group_id", sa.String(64), nullable=True), sa.UniqueConstraint("broker_account_id", "external_trade_id", name="uq_trade_external"))
    for table in ["daily_snapshots", "greeks_snapshots", "income_events", "risk_metrics", "margin_metrics", "audit_logs", "file_imports", "task_execution_history"]:
        pass
    op.create_table("daily_snapshots", *audit_columns(), sa.Column("snapshot_date", sa.Date(), nullable=False), sa.Column("nav", sa.Numeric(18, 4), nullable=False), sa.Column("pnl_day", sa.Numeric(18, 4), nullable=False))
    op.create_table("greeks_snapshots", *audit_columns(), sa.Column("snapshot_at", sa.DateTime(timezone=True), nullable=False), sa.Column("delta", sa.Float(), nullable=False), sa.Column("gamma", sa.Float(), nullable=False), sa.Column("theta", sa.Float(), nullable=False), sa.Column("vega", sa.Float(), nullable=False))
    op.create_table("income_events", *audit_columns(), sa.Column("event_date", sa.Date(), nullable=False), sa.Column("amount", sa.Numeric(18, 4), nullable=False), sa.Column("event_type", sa.String(32), nullable=False))
    op.create_table("risk_metrics", *audit_columns(), sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False), sa.Column("metric_name", sa.String(64), nullable=False), sa.Column("metric_value", sa.Numeric(20, 6), nullable=False), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("margin_metrics", *audit_columns(), sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategies.id"), nullable=True), sa.Column("notional_exposure", sa.Numeric(20, 4), nullable=False), sa.Column("margin_used", sa.Numeric(20, 4), nullable=False), sa.Column("broker_requirement", sa.Numeric(20, 4), nullable=True), sa.Column("source", sa.String(32), nullable=False))
    op.create_table("audit_logs", *audit_columns(), sa.Column("event_type", sa.String(100), nullable=False), sa.Column("entity_type", sa.String(100), nullable=False), sa.Column("entity_id", sa.String(64), nullable=False), sa.Column("payload", sa.Text(), nullable=False))
    op.create_table("file_imports", *audit_columns(), sa.Column("filename", sa.String(255), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("row_count", sa.Integer(), nullable=False, server_default="0"))
    op.create_table("task_execution_history", *audit_columns(), sa.Column("task_name", sa.String(255), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=False), sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    for table in ["task_execution_history", "file_imports", "audit_logs", "margin_metrics", "risk_metrics", "income_events", "greeks_snapshots", "daily_snapshots", "trades", "positions", "option_contracts", "strategies", "broker_accounts", "user_roles", "roles", "users"]:
        op.drop_table(table)
