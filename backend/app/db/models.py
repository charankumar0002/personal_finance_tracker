from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    kyc = relationship("KYC", back_populates="user", uselist=False)
    investor_profile = relationship("InvestorProfile", back_populates="user", uselist=False)

class KYC(Base):
    __tablename__ = "kyc"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    pan_number = Column(String, nullable=False)
    aadhaar_number = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="pending")  # New field for KYC status
    user = relationship("User", back_populates="kyc")

class InvestorProfile(Base):
    __tablename__ = "investor_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    risk_level = Column(String, nullable=False)
    investment_goals = Column(Text, nullable=False)  # Store as comma-separated string
    investment_experience = Column(String, nullable=False)
    user = relationship("User", back_populates="investor_profile") 