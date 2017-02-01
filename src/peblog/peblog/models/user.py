import bcrypt
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class PasswordHandler:
    @staticmethod
    def hash(pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        return pwhash.decode('utf8')

    def check(hash, pw):
        expected_hash = hash.encode('utf8')
        return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    fullname = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)

    password_hash = Column(Text)

    def set_password(self, pw):
        self.password_hash = PasswordHandler.make_hash(pw)

    def check_password(self, pw):
        if self.password_hash is None:
            return False
        return PasswordHandler.check(self.password_hash, pw)


Index('users_emails', User.email, unique=True)
Index('users_usersnames', User.username, unique=True)
Index('users_roles', User.role)
