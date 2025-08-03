from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String(255), nullable=False, unique=True) 
    is_primary = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False) 
    deleted_at = Column(DateTime, nullable=True) 
    verified_at = Column(DateTime, nullable=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
class VerifiedEmailToken(Base):
    __tablename__ = "verified_email_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(500), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 
    used_at = Column(DateTime, nullable=True)
   
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    
class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens" 
    
    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(500), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(200), nullable=False) 
    is_deleted = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    due_at = Column(DateTime, nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  
    description = Column(String(500), nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    tasks = relationship("Task", back_populates="group",lazy="dynamic",cascade="all, delete-orphan",order_by="Task.created_at")