from pathlib import Path
from typing import List

def gather_files(files: List[str]):
    all_files = []
    for _file in  files:
        f = Path(_file)
        if not f.exists():
            raise ValueError(f"File {f} does not exists")
        if f.is_file():
            all_files.append(f)
        if f.is_dir():
            all_files.extend([f for f in f.glob('*') if f.is_file()])
    return all_files
