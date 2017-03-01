import pytest


@pytest.fixture()
def fakefactory(dbsession):
    # TODO: Make thread-safe
    from . import fakefactory
    fakefactory.db_session_proxy.session = dbsession
    try:
        yield fakefactory
    finally:
        fakefactory.db_session_proxy.session = None
