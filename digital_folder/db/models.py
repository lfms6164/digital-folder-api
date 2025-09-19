import enum
import uuid

from sqlalchemy import Column, ForeignKey, String, Table, Text, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from digital_folder.db.db import Base

project_tag_relations = Table(
    "project_tag_relations",
    Base.metadata,
    Column(
        "project_id",
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Auth(Base):
    __tablename__ = "auth"

    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=True)
    introduction = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

    tags = relationship(
        "Tag",
        secondary=project_tag_relations,
        back_populates="projects",
        passive_deletes=True,
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=False)
    group_id = Column(
        "group_id", UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False
    )

    projects = relationship(
        "Project",
        secondary=project_tag_relations,
        back_populates="tags",
        passive_deletes=True,
    )
    group = relationship("Group", back_populates="tags")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    tags = relationship("Tag", back_populates="group")


class TicketState(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    state = Column(Enum(TicketState), nullable=False, default=TicketState.OPEN)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
