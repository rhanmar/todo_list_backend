from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    color = Column(String)
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_checked = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")
