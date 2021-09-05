from functools import wraps
from contextlib import contextmanager

from app.infrastructure import database


@contextmanager
def transaction():
    try:
        yield
        database.AppRepository.db.session.commit()
    except Exception as ex:
        database.AppRepository.db.session.rollback()
        raise ex


def transactional(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        with transaction():
            return func(*args, **kwargs)
    return decorated_function
