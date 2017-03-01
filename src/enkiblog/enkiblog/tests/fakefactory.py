from collections import namedtuple
import factory
from pyramid.threadlocal import get_current_registry

from websauna.system.user import models as ws_models
from websauna.system.user.interfaces import IPasswordHasher
from websauna.utils.time import now
from websauna.system.user.utils import get_site_creator


class DBSessionProxy:
    session = None

    def __getattr__(self, attr):
        return getattr(self.session, attr)


db_session_proxy = DBSessionProxy()


def hash_password(password):
    # ???: should I pass "registry" trougth proxy as well?
    registry = get_current_registry()
    hasher = registry.getUtility(IPasswordHasher)
    hashed = hasher.hash_password(password)
    return hashed


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = db_session_proxy
        force_flush = True
        abstract = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        excluded = {k: w for k, w in kwargs.items() if k in cls._meta.exclude}
        obj = super()._prepare(create, **kwargs)
        obj._fb_excluded = namedtuple('excluded', excluded)(**excluded)
        return obj

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super()._create(model_class, *args, **kwargs)
        assert user.can_login()
        return user


class UserFactory(BaseFactory):
    class Meta:
        model = ws_models.User
        exclude = ('password',)

    class Params:
        password = factory.Faker('slug')

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    # role = 'no roles yet'
    hashed_password = factory.LazyAttribute(lambda obj: hash_password(obj.password))
    activated_at = factory.LazyAttribute(lambda obj: now())


class AdminFactory(UserFactory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super()._create(model_class, *args, **kwargs)
        site_creator = get_site_creator(get_current_registry())
        site_creator.init_empty_site(db_session_proxy, user)
        return user
