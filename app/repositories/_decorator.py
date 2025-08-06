from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

class RepositoryError(Exception):
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            args[0].session.rollback()
            raise RepositoryError(f"Database operation failed: {str(e)}") from e
        except KeyError as e:
            raise RepositoryError(f"Missing field: {str(e)}") from e
        except ValueError as e:
            raise RepositoryError(str(e)) from e
        except PermissionError as e:
            raise RepositoryError(str(e)) from e
        except Exception as e:
            raise RepositoryError(f"Unexpected error: {str(e)}") from e
    return wrapper
