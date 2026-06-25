from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class PatientRecord(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    age = Column(Integer)
    stage = Column(String)
    severity = Column(String)
    confidence = Column(Float)
    ai_explanation = Column(Text)