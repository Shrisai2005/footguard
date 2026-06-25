from pydantic import BaseModel

class PatientCreate(BaseModel):
    patient_name: str
    age: int
    stage: str
    severity: str
    confidence: float
    ai_explanation: str

class PatientResponse(PatientCreate):
    id: int

    class Config:
        orm_mode = True