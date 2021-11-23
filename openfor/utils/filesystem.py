from pathlib import Path
from typing import List
import py7zr

from openfor.core import CompressedArtifactType


def gather_files(files: List[str]):
    all_files = []
    for _file in  files:
        f = Path(_file)
        if not f.exists():
            raise ValueError(f"File {f} does not exists")
        if f.is_file():
            all_files.append(f)
        if f.is_dir():
            all_files.extend([f for f in f.rglob('*') if f.is_file()])
    return all_files

def uncompress(filepath: Path, output_folder: Path, compression_type: CompressedArtifactType):
    if compression_type == CompressedArtifactType.SEVENZIP:
        try:
            with py7zr.SevenZipFile(filepath, 'r') as archive:
                archive.extractall(path="/tmp")
        except Exception as err:
            pass
