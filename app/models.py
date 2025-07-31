from sqlalchemy.orm import Mapped, mapped_column, registry
from enum import Enum, IntEnum

table_registry = registry()


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


@table_registry.mapped_as_dataclass
class Subject:
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    stars: Mapped[StarRating]
    subject_type: Mapped[SubjectsEnum]
