from openfor.extractors import DockerExtractor
from openfor.core import ArtifactType
from pathlib import Path

class sdfr:
    pass

class Zircolite(DockerExtractor):
    name = "zircolite"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path):

        self.run_container("--evtx", "/tmp/input.evtx", "--ruleset", "rules/rules_windows_generic.json", volumes={
            artifact_file_path.absolute(): {"bind": "/tmp/input.evtx", "mode": "ro"}
        })