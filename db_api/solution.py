from db_api import SqlAlchemyBase
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm


# TODO: нужен ли нам Solution?
class Solution(SqlAlchemyBase):
    __tablename__ = 'solutions'

    id = Cl(sql.Integer, autoincrement=True, unique=True, nullable=False, primary_key=True)
    filename = Cl(sql.String, nullable=False)
    sender = Cl(sql.String, nullable=False)
    task_id = Cl(sql.Integer, sql.ForeignKey('tasks.id', ondelete='cascade'), nullable=False)
    task = orm.relation('Task')
    comment = Cl(sql.Text)
