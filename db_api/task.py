from db_api import SqlAlchemyBase
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = Cl(sql.Integer, autoincrement=True, unique=True, nullable=False, primary_key=True)
    name = Cl(sql.String, nullable=False, unique=True)
    description = Cl(sql.Text)
    solutions = orm.relation('Solution', back_populates='task', cascade='all,delete')
    test_cases = orm.relation('TestCase', back_populates='task', cascade='all,delete')

