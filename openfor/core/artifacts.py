from enum import Enum, auto
from pathlib import Path
import magic
from loguru import logger

class ArtifactType(Enum):
    EVTX = auto()
    UNKNOWN = auto()

class CompressedArtifactType(Enum):
    SEVENZIP = auto()

def get_file_type(filepath: Path) -> ArtifactType:
    _magic = magic.Magic(mime=False, uncompress=False)
    m = _magic.from_file(str(filepath))
    logger.debug(f"File {filepath} is: {m}")

    if m.startswith("MS Windows Vista Event Log"):
        return ArtifactType.EVTX
    elif m.startswith("7-zip archive data"):
        return CompressedArtifactType.SEVENZIP
    else:
        return ArtifactType.UNKNOWN
