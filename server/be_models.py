from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(500))
    email = Column(String(100))
    phone_number = Column(String(20))
    role_id = Column(Integer, ForeignKey('roles.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    status = Column(String(20))

    history = relationship("History", back_populates="user")

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(10), unique=True)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(100), unique=True)

class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    path = Column(String(100))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    version = Column(String(15))
    description = Column(String(500))
    model_type = Column(String(50))
    creat_at = Column(DateTime, default=datetime.utcnow)


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    classification_model_id = Column(Integer)
    localization_model_id = Column(Integer)
    input_img_path = Column(String(100))
    output_img_path = Column(String(100))
    label = Column(String(20))
    classification_accuracy = Column(Float)
    localization_accuracy = Column(Float)
    creat_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="history")