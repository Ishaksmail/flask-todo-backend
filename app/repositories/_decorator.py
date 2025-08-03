from functools import wraps

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            args[0].session.rollback()  # args[0] هو self في métodos
            raise RepositoryError(f"Database operation failed: {str(e)}") from e
        except Exception as e:
            raise RepositoryError(f"Unexpected error: {str(e)}") from e
    return wrapper