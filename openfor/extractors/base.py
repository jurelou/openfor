from abc import ABC, abstractmethod
from typing import Union
from openfor.core import ArtifactType
from pathlib import Path
from openfor.core import exceptions
import docker
import sys
from openfor import settings
from loguru import logger
import subprocess

class BaseExtractor(ABC):
    def __init__(self):
        if not isinstance(self.input_artifact_type, ArtifactType):
            raise exceptions.InvalidExtractor(name=self.name, reason=f"invalid input_artifact_type: {self.input_artifact_type}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name, allowing to recognize an extractor in the settings."""

    @property
    @abstractmethod
    def input_artifact_type(self):
        """List of artifact types processed by this extractor."""

    @abstractmethod
    def run(self, artifact_file_path: Path, output_folder: Path):
        """Parses a given file."""

class SubprocessExtractor(BaseExtractor, ABC):

    def run_subprocess(self, cmds, **kwargs):
        logger.info(f"Running subprocess for {self.name} : {cmds}")
        process: subprocess.CompletedProcess = subprocess.run(
            cmds,
            capture_output=True,
            shell=True,
            **kwargs
        )
        if process.returncode != 0:
            batch: str = process.stderr.decode().strip()
            logger.critical(f'Subprocess error for {self.name}: `{batch}`')
        logger.debug(f'Successfully executed subprocess for {self.name}')
        return process.stdout.decode()

DOCKER_CLIENT = docker.from_env()
_CACHED_BUILDS = {}

class DockerExtractor(BaseExtractor, ABC):
    def __init__(self):
        super().__init__()
        self._image = self._build_image()

    def _build_image(self):
        global _CACHED_BUILDS

        image = f"openfor_{self.name.lower()}"
        if self.name in _CACHED_BUILDS:
            logger.debug(f"Image for {self.name} already builded")
            return _CACHED_BUILDS[self.name]
        

        try:
            DOCKER_CLIENT.images.get(image)
            logger.debug(f"Image for {self.name} already found on the system")
            if not settings.force_docker_rebuild:
                _CACHED_BUILDS[self.name] = image
                return image
        except Exception as err:
            pass

        logger.info(f"Building image for {self.name}")
        subclass_path = sys.modules[self.__module__].__file__ 
        actual_folder = Path(subclass_path).resolve().parent

        _, stdout = DOCKER_CLIENT.images.build(path=str(actual_folder), forcerm=True, nocache=True, tag=image)
        for s in stdout:
                logger.debug(s)
        _CACHED_BUILDS[self.name] = image
        return image
    
    def run_container(self, *args, detach=True, stderr=True, auto_remove=True, **kwargs):
        logger.info(f"Running container {self._image} {args}")
        container = DOCKER_CLIENT.containers.run(
            self._image,
            args,
            detach=detach,
            stderr=stderr,
            auto_remove=auto_remove,
            **kwargs
        )
        for log in container.logs(stdout=True, stderr=True, stream=True, follow=True):
            logger.debug(f"[DOCKER] {log.decode()}")
        

