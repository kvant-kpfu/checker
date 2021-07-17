from db_api import SqlAlchemyBase
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm


class TestCase(SqlAlchemyBase):
    __tablename__ = 'test_cases'
    id = Cl(sql.Integer, autoincrement=True, unique=True, nullable=False, primary_key=True)
    input_filename = Cl(sql.String, nullable=False)
    output_filename = Cl(sql.String, nullable=False)
    task_id = Cl(sql.Integer, sql.ForeignKey('tasks.id', ondelete='cascade'), nullable=False)
    task = orm.relation('Task')
