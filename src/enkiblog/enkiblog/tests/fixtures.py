import pytest
from websauna.tests.fixtures import create_test_dbsession
from sqlalchemy.orm.session import Session


class DBSessionProxy:
    session = None

    def __getattr__(self, attr):
        return getattr(self.session, attr)


db_session_proxy = DBSessionProxy()


@pytest.fixture()
def factoryshared_dbsession(request, app) -> Session:
    if db_session_proxy.session is None:
        db_session_proxy.session = create_test_dbsession(
            request, app.initializer.config.registry)
    try:
        yield db_session_proxy
    finally:
        db_session_proxy.session = None
