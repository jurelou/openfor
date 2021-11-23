from openfor.extractors import DockerExtractor, SubprocessExtractor
from openfor.core import ArtifactType
from pathlib import Path
from loguru import logger
"""
class Zircolite(DockerExtractor):
    name = "zircolite"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path, output_folder: Path):
        docker_file_path = f"/tmp/{artifact_file_path.stem}.evtx"
        self.run_container("--evtx", docker_file_path, "--ruleset", "rules/rules_windows_generic.json", "--templateOutput", "/tmp/output/zircolite_output.json", "--template", "templates/exportForSplunk.tmpl", volumes={
            artifact_file_path.absolute(): {"bind": docker_file_path, "mode": "ro"},
            output_folder.absolute(): {"bind": "/tmp/output", "mode": "rw"}
        })
"""

class Zircolite(SubprocessExtractor):
    name = "zircolite"
    input_artifact_type = ArtifactType.EVTX


    def run(self, artifact_file_path: Path, output_folder: Path):
        output_file = output_folder.absolute() / "zircolite_output.json"

        command = f"python ./zircolite.py \
        --evtx {artifact_file_path.absolute()} \
        --fileext={artifact_file_path.suffix[1:]} \
        --ruleset rules/rules_windows_generic.json \
        --templateOutput {output_folder.absolute() / 'data.js'} --template templates/exportForZircoGui.tmpl \
        --templateOutput {output_folder.absolute() / 'splunk.json'} --template templates/exportForSplunk.tmpl"

        out = self.run_subprocess(command, cwd="./vendor/zircolite")
        logger.debug(f"Zircolite output: {out}")
