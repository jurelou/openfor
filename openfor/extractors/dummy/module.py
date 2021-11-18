from pathlib import Path

from openfor.extractors import BaseExtractor
from openfor.core import ArtifactType
from openfor import settings

class DummyExtractor(BaseExtractor):
    name = "dummy"
    input_artifact_type = ArtifactType.EVTX

    def run(self, artifact_file_path: Path):
        print("RUNNN", artifact_file_path)