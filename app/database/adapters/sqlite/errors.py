from sqlalchemy.exc import (
    DataError,
    DBAPIError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)


class AdapterError(Exception):
    pass


class AdapterIntegrityError(AdapterError):
    pass


class AdapterOperationalError(AdapterError):
    pass


class AdapterDataError(AdapterError):
    pass


class AdapterProgrammingError(AdapterError):
    pass


class AdapterDatabaseError(AdapterError):
    pass


def to_adapter_error(exc: SQLAlchemyError) -> AdapterError:
    message = str(exc)

    if isinstance(exc, IntegrityError):
        return AdapterIntegrityError(message)
    if isinstance(exc, DataError):
        return AdapterDataError(message)
    if isinstance(exc, OperationalError):
        return AdapterOperationalError(message)
    if isinstance(exc, ProgrammingError):
        return AdapterProgrammingError(message)
    if isinstance(exc, DBAPIError):
        return AdapterDatabaseError(message)

    return AdapterError(message)
