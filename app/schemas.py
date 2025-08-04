from pydantic import BaseModel
from typing import List, Optional
from enum import Enum, IntEnum


class StarRating(IntEnum):
    um = 1
    dois = 2
    tres = 3
    quatro = 4
    cinco = 5


class SubjectsEnum(str, Enum):
    biologia = "biologia"
    quimica = "quimica"
    fisica = "física"
    matematica = "matemática"
    historia = "historia"
    geografia = "geografia"
    sociologia = "sociologia"
    filosofia = "filosofia"
    linguagens = "linguagens"
    literatura = "literatura"


class CreateSubject(BaseModel):
    name: str
    stars: Optional[StarRating] = StarRating.um
    subject_type: SubjectsEnum


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterTodo(BaseModel):
    name: Optional[str] = None
    subject: Optional[List[SubjectsEnum]] = None
    stars: Optional[StarRating] = None


class UpdateSubject(BaseModel):
    name: Optional[str] = None
    stars: Optional[StarRating] = None
    subject_type: Optional[SubjectsEnum] = None


class Subjects(BaseModel):
    id: int
    name: str
    stars: StarRating = StarRating.cinco
    subject_type: SubjectsEnum


class Config:
    from_attributes = True


class ListSubjects(BaseModel):
    subjects: List[Subjects]


class DeleteSubjectResponse(BaseModel):
    detail: str
