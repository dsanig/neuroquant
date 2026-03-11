"""import pipeline foundation

Revision ID: 20260310_0002
Revises: 20260310_0001
Create Date: 2026-03-10
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260310_0002"
down_revision = "20260310_0001"
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
    op.create_table(
        "import_batch",
        *audit_columns(),
        sa.Column("intake_channel", sa.String(32), nullable=False),
        sa.Column("source_system_name", sa.String(120), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("parser_name", sa.String(120), nullable=True),
        sa.Column("parser_version", sa.String(32), nullable=True),
        sa.Column("row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("imported_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_table(
        "import_file",
        *audit_columns(),
        sa.Column("import_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("import_batch.id"), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("storage_uri", sa.String(500), nullable=False),
        sa.Column("encrypted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("checksum_sha256", sa.String(64), nullable=False, unique=True),
        sa.Column("byte_size", sa.Integer(), nullable=False),
        sa.Column("mime_type", sa.String(120), nullable=True),
        sa.Column("format_hint", sa.String(64), nullable=True),
        sa.Column("detected_format", sa.String(64), nullable=True),
    )
    op.create_table(
        "import_error",
        *audit_columns(),
        sa.Column("import_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("import_batch.id"), nullable=False),
        sa.Column("import_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("import_file.id"), nullable=True),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
    )
    op.create_table(
        "import_row_error",
        *audit_columns(),
        sa.Column("import_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("import_batch.id"), nullable=False),
        sa.Column("import_file_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("import_file.id"), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("source_row", sa.JSON(), nullable=False),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("parser_version", sa.String(32), nullable=False),
    )
    op.create_table(
        "source_mapping_metadata",
        *audit_columns(),
        sa.Column("source_system_name", sa.String(120), nullable=False),
        sa.Column("mapping_version", sa.String(32), nullable=False),
        sa.Column("object_type", sa.String(64), nullable=False),
        sa.Column("mapping_schema", sa.JSON(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )


def downgrade() -> None:
    for table in ["source_mapping_metadata", "import_row_error", "import_error", "import_file", "import_batch"]:
        op.drop_table(table)
