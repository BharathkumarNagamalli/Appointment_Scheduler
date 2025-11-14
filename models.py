# models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    id: Optional[int]
    name: str

@dataclass
class Appointment:
    id: Optional[int]
    patient_id: int
    date: str
    start: str
    end: str
