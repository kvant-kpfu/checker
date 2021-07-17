from typing import Optional, List, Callable, Any

from db_api.task import Task
from db_api.solution import Solution
from db_api.test_case import TestCase
from sqlalchemy.orm import Session
from db_api import SqlAlchemyBase
import os


def create_task(session: Session,
                name: str,
                description: str = None) -> Task:
    """
    Creates Task object and adds it to a session
    :param session: session you want to add object to, Session
    :param name: name of task, string
    :param description: optional, description of task, string
    :return: Task object
    """
    task = Task(name=name, description=description)
    session.add(task)
    return task


def create_solution(session: Session,
                    filename: str,
                    sender: str,
                    task_id: int,
                    comment: Optional[str] = None) -> Solution:
    """
    Creates Solution object and adds it to a session
    :param session: session you want to add object to, Session
    :param filename: name of solution file, string
    :param sender: name of sender, string
    :param task_id: id of task you want to attach solution to, int
    :param comment: optional, comment of teachers, str
    :return: Solution object
    """

    sol = Solution(filename=filename,
                   sender=sender,
                   task_id=task_id,
                   comment=comment)
    session.add(sol)
    return sol


def create_test_case(session: Session,
                     input_filename: str,
                     output_filename: str,
                     task_id: int) -> TestCase:
    """
    Creates TestCase object and adds it to a session
    :param session: session you want to add object to, Session
    :param input_filename: name of test case input file, string
    :param output_filename: name of test case output file, string
    :param task_id: id of task you want to attach test case to, int
    :return: TestCase object
    """

    case = TestCase(input_filename=input_filename,
                    output_filename=output_filename,
                    task_id=task_id)
    session.add(case)
    return case


def create_test_case_by_task_name(session: Session,
                                  input_filename: str,
                                  output_filename: str,
                                  task_name: str) -> TestCase:
    task_id = session.query(Task).filter(Task.name == task_name).first().id
    return create_test_case(session, input_filename, output_filename, task_id)




def get_next_index(session: Session,
                   cls: SqlAlchemyBase) -> int:
    """
    Get next index for cls type object
    :param session: session you want to search with, Session
    :param cls: model class, SqlAlchemyBase
    :return: index, int
    """

    all_obj = session.query(cls).order_by(cls.id).all()
    try:
        return all_obj[-1].id + 1
    except IndexError:
        return 1


def remove(session: Session,
           cls: SqlAlchemyBase,
           id_: int) -> None:
    """
    Remove object from database
    :param session: session you want to delete object from, Session
    :param cls: type of object, SqlAlchemyBAse
    :param id_: id of object, int
    :return:
    """
    obj = session.query(cls).get(id_)
    session.delete(obj)


remove_task = lambda session, id_: remove(session, Task, id_)
remove_solution = lambda session, id_: remove(session, Solution, id_)
remove_test_case = lambda session, id_: remove(session, TestCase, id_)


def get_all(session: Session,
            cls: SqlAlchemyBase):
    """
    Get all objects of cls type from database
    :param session: session you want to get objects from
    :param cls: type of objects you want to get
    :return:
    """

    return session.query(cls).all()
