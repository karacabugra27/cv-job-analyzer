"""create feedback table

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-24

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("page_url", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_feedback_created_at", "feedback", ["created_at"])

    op.execute("ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;")
    op.execute(
        """
        CREATE POLICY feedback_insert_own ON public.feedback
        FOR INSERT TO authenticated
        WITH CHECK (user_id = auth.uid());
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS feedback_insert_own ON public.feedback;")
    op.execute("ALTER TABLE public.feedback DISABLE ROW LEVEL SECURITY;")
    op.drop_index("ix_feedback_created_at", table_name="feedback")
    op.drop_table("feedback")
