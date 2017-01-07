from uuid import uuid4

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from websauna.system.model.meta import Base
from websauna.system.model.columns import UTCDateTime
from websauna.system.model.json import NestedMutationDict
from websauna.utils.time import now


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    slug = Column(String(256), nullable=False, unique=True)

    title = Column(String(256), default=None)
    description = Column(String(256), default=None)
    body = Column(String(256), default=None)

    published_at = Column(UTCDateTime, default=None)
    created_at = Column(UTCDateTime, default=now)
    updated_at = Column(UTCDateTime, default=None)

    author = Column(String(256), default=None)

    comments = Column(String(256), default=None)
    tags = Column(String(256), default=None)

    state = Column(NestedMutationDict.as_mutable(JSONB), default=dict)
    data = Column(NestedMutationDict.as_mutable(JSONB), default=dict)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    slug = Column(String(256), nullable=False, unique=True)

    title = Column(String(256))
    description = Column(String(256), default=None)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    post = Column(String(256), default=None)
    body = Column(String(256), default=None)

    published_at = Column(UTCDateTime, default=None)
    created_at = Column(UTCDateTime, default=now)
    updated_at = Column(UTCDateTime, default=None)

    author = Column(String(256), default=None)
    state = Column(NestedMutationDict.as_mutable(JSONB), default=dict)


class Link(Base):
    __tablename__ = "links"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    slug = Column(String(256), nullable=False, unique=True)

    title = Column(String(256))
    description = Column(String(256), default=None)
    link = Column(String(256), default=None)


class Media(Base):
    __tablename__ = "media"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    slug = Column(String(256), nullable=False, unique=True)

    title = Column(String(256))
    mtype = Column(String(256))
    description = Column(String(256), default=None)
    media = Column(String(256), default=None)
    link = Column(String(256), default=None)
