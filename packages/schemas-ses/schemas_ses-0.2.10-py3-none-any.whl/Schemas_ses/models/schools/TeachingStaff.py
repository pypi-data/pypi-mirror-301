
from typing_extensions import Literal, Optional
from datetime import date

from Schemas_ses.enumeration.enums import StudiesLevel
from Schemas_ses.models.model import AnnexeModel
from Schemas_ses.type.types import Year, Sexe


class HighestDegree(AnnexeModel):
    academic: Literal["CEP", "BEPC", "BAC", "LICENCE", "MASTER"]
    professional: Literal["CEAP", "CAP"]


class Seniority(AnnexeModel):
    public: int
    department: int
    school: int


class NumberOfVisit(AnnexeModel):
    inspector: int
    director: int
    cp: int


class Personnel(AnnexeModel):
    matricule: str
    name: str
    surname: str
    sexe: Sexe
    birth_year: Year
    highest_degree: HighestDegree
    grade: str
    statut: Literal["ACPDE", "ACE", "AME", "Communautaire", "Fonctionnaire de l'état", "Privé", "Autre"]
    fonction: Literal["Directeur", "Adjoint", "Enseignant"]
    real_indice: int
    teached_subjects: list[StudiesLevel]
    seniority: Seniority
    last_formation_date: date
    number_of_visit: NumberOfVisit
    up_participation: int


class TeachingStaff(AnnexeModel):
    personnel: Optional[list[Personnel]]
