from openfor.extractors import DockerExtractor
from openfor.core import ArtifactType
from pathlib import Path

class sdfr:
    pass

class Zircolite(DockerExtractor):
    name = "zircolite"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path, output_folder: Path):
        docker_file_path = f"/tmp/{artifact_file_path.stem}.evtx"
        self.run_container("--evtx", docker_file_path, "--ruleset", "rules/rules_windows_generic.json", "--templateOutput", "/tmp/output/zircolite_output.json", "--template", "templates/exportForSplunk.tmpl", volumes={
            artifact_file_path.absolute(): {"bind": docker_file_path, "mode": "ro"},
            output_folder.absolute(): {"bind": "/tmp/output", "mode": "rw"}
        })