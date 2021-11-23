from openfor.extractors import SubprocessExtractor
from openfor.core import ArtifactType
from pathlib import Path

"""
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
"""

class EvtxDump(SubprocessExtractor):
    name = "evtx_dump"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path, output_folder: Path):
        output_file_xml = output_folder.absolute() / f"{artifact_file_path.stem}.xml"
        output_file_json = output_folder.absolute() / f"{artifact_file_path.stem}.json"

        command_xml = f"./vendor/evtx_dump {artifact_file_path.absolute()} --threads 4 --format xml --output {output_file_xml} --no-confirm-overwrite"
        command_json = f"./vendor/evtx_dump {artifact_file_path.absolute()} --threads 4 --format json --output {output_file_json} --no-confirm-overwrite"

        self.run_subprocess(command_xml)
        self.run_subprocess(command_json)
