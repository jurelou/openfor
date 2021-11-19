from openfor.extractors import DockerExtractor
from openfor.core import ArtifactType
from pathlib import Path

class sdfr:
    pass

class EvtxDump(DockerExtractor):
    name = "evtx_dump"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path, output_folder: Path):

        docker_input_file_path = f"/tmp/{artifact_file_path.stem}.evtx"
        docker_output_file_path = f"/tmp/output/{artifact_file_path.stem}.evtx"

        self.run_container(docker_input_file_path, "--no-confirm-overwrite", "--threads", "4", "--format", "xml", "--output", docker_output_file_path, volumes={
            artifact_file_path.absolute(): {"bind": docker_input_file_path, "mode": "ro"},
            output_folder.absolute(): {"bind": "/tmp/output", "mode": "rw"}
        })