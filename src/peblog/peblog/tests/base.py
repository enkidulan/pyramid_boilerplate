import unittest
import transaction
from pyramid import testing

DEFAULT_SETTINGS = {
    'sqlalchemy.url': 'sqlite:///:memory:',
}


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class TestSessionManager:
    def __init__(self, config):
        self.settings = config.get_settings()
        self.config = config
        self.config.include('peblog.models')
        from peblog.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )
        self.engine = get_engine(self.settings)
        session_factory = get_session_factory(self.engine)
        self.session = get_tm_session(session_factory, transaction.manager)


class TestConfigManager:
    def __init__(self, settings=None):
        self.config = testing.setUp(settings=DEFAULT_SETTINGS if settings is None else settings)


# TODO: redo with ZCA
TESTS_CONFIG = TestConfigManager()
TEST_DB = TestSessionManager(TESTS_CONFIG.config)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db = TEST_DB
        from peblog.models.meta import Base
        Base.metadata.create_all(self.db.engine)

    # def init_database(self):

    def tearDown(self):
        from peblog.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.db.engine)
