from enum import Enum, auto
from pathlib import Path
import magic
from loguru import logger

class ArtifactType(Enum):
    EVTX = auto()
    UNKNOWN = auto()

def get_file_type(filepath: Path) -> ArtifactType:
    _magic = magic.Magic(mime=False, uncompress=False)
    m = _magic.from_file(str(filepath))
    logger.debug(f"File {filepath} is: {m}")
    if m.startswith("MS Windows Vista Event Log"):
        return ArtifactType.EVTX
    else:
        return ArtifactType.UNKNOWN
