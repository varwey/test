# -*- coding: utf-8 -*-
import contextlib
import traceback
from flask.globals import current_app
from sqlalchemy.orm import sessionmaker
from nowdo.controls.base import main_db_engine

main_db_session_maker = sessionmaker(bind=main_db_engine)


def get_main_session():
    """
    连接到主数据库的session
    """
    return main_db_session_maker()


@contextlib.contextmanager
def session_cm():
    session = get_main_session()
    try:
        yield session
    except Exception:
        current_app.logger.warn(traceback.format_exc())
        raise
    finally:
        session.close()