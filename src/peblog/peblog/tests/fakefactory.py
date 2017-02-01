import factory
from peblog import models
from peblog.models.user import PasswordHandler
from .base import TEST_DB


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = TEST_DB.session
        force_flush = True
        exclude = ('password',)

    class Params:
        password = 'qwerty'

    username = factory.Faker('user_name')
    fullname = factory.Faker('name')
    email = factory.Faker('email')
    role = 'no roles yet'
    password_hash = factory.LazyAttribute(lambda obj: PasswordHandler.hash(obj.password))
