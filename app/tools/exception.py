from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from loguru import logger
import re


class XBaseException(HTTPException):
    def __init__(self, status_code: str, detail: int):
        super().__init__(status_code=status_code, detail=detail)


class ExceptionInternalError(XBaseException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=500, detail=detail)


class ExceptionUnauthorized(XBaseException):
    def __init__(self):
        super().__init__(status_code=401, detail="Unauthorized")


class ExceptionForbidden(XBaseException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")


class ExceptionLimitExceeded(XBaseException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Exceeded the maximum number of allowed requests",
        )


class DuplicateKeyError(HTTPException):
    def __init__(self, detail="Duplicate entry error"):
        super().__init__(status_code=400, detail=detail)


def extract_duplicate_field_sqlite(error_message: str) -> str:
    """
    Extracts the column name from SQLite's IntegrityError message.
    """
    # Pattern for SQLite's UNIQUE constraint failure
    match = re.search(r'UNIQUE constraint failed: (\w+\.\w+)', error_message)
    if match:
        return match.group(1).split(".")[1]  # Extract column name

    return None


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except IntegrityError as e:
            logger.exception("Duplicate key error: %s", e)

            # Try to extract column name from SQLite's error message
            error_message = str(e.orig)
            duplicate_field = extract_duplicate_field_sqlite(error_message)

            if duplicate_field:
                raise DuplicateKeyError(
                    detail=f"A record with this {duplicate_field} already exists")
            else:
                raise DuplicateKeyError(
                    detail="A duplicate record already exists") from e
        except SQLAlchemyError as e:
            logger.exception("Database error: %s", e)
            raise ExceptionInternalError(
                detail="A database error occurred") from e
        except Exception as e:
            logger.exception(e)
            raise ExceptionInternalError from e
    return wrapper
