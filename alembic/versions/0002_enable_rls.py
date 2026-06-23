"""enable RLS on public tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-23

"""
from typing import Sequence, Union

from alembic import op


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE public.alembic_version ENABLE ROW LEVEL SECURITY;")

    op.execute("ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;")

    op.execute(
        """
        CREATE POLICY analyses_select_own ON public.analyses
        FOR SELECT TO authenticated
        USING (user_id = auth.uid());
        """
    )
    op.execute(
        """
        CREATE POLICY analyses_insert_own ON public.analyses
        FOR INSERT TO authenticated
        WITH CHECK (user_id = auth.uid());
        """
    )
    op.execute(
        """
        CREATE POLICY analyses_update_own ON public.analyses
        FOR UPDATE TO authenticated
        USING (user_id = auth.uid())
        WITH CHECK (user_id = auth.uid());
        """
    )
    op.execute(
        """
        CREATE POLICY analyses_delete_own ON public.analyses
        FOR DELETE TO authenticated
        USING (user_id = auth.uid());
        """
    )


def downgrade() -> None:
    op.execute("DROP POLICY IF EXISTS analyses_delete_own ON public.analyses;")
    op.execute("DROP POLICY IF EXISTS analyses_update_own ON public.analyses;")
    op.execute("DROP POLICY IF EXISTS analyses_insert_own ON public.analyses;")
    op.execute("DROP POLICY IF EXISTS analyses_select_own ON public.analyses;")
    op.execute("ALTER TABLE public.analyses DISABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE public.alembic_version DISABLE ROW LEVEL SECURITY;")
