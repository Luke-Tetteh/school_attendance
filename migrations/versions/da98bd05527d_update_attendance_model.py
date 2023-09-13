"""Update Attendance model

Revision ID: da98bd05527d
Revises: dc57954821adc6
Create Date: 2023-06-02 08:43:01.938324

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'da98bd05527d'
down_revision = 'dc57954821adc6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        if_not_exists=True
)

    op.create_table('students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        if_not_exists=True

    )
    op.create_table('attendance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),  # Adding 'date' column of type Date
        sa.Column('is_present', sa.Boolean(), nullable=False),
        sa.Column('attendance_score', sa.Float(), nullable=True),  # Adding 'attendance_score' column of type Float with nullable option
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True
)
    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True
    )

    op.create_table('marks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True
    )
    op.create_table('enrollment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id']),
        sa.PrimaryKeyConstraint('id'),
        if_not_exists=True
    )



def downgrade():
    op.drop_table('student_course')
    op.drop_table('marks')
    op.drop_table('marks')
    op.drop_table('courses')
    op.drop_table('attendance')
    op.drop_table('students')
    op.drop_table('users')

    # ### end Alembic commands ###
