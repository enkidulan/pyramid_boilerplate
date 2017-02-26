import factory
from pyramid.threadlocal import get_current_registry

from websauna.system.user import models as ws_models
from websauna.system.user.interfaces import IPasswordHasher

from enkiblog.tests.fixtures import db_session_proxy


def hash_password(password):
    registry = get_current_registry()
    hasher = registry.getUtility(IPasswordHasher)
    hashed = hasher.hash_password(password)
    return hashed


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ws_models.User
        sqlalchemy_session = db_session_proxy
        force_flush = True
        exclude = ('password',)

    class Params:
        password = 'qwerty'

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    # role = 'no roles yet'
    hashed_password = factory.LazyAttribute(lambda obj: hash_password(obj.password))
