import asyncio
import random
import time
from loguru import logger
from typing import List
from pathlib import Path
import time

from openfor import settings

from openfor.core import exceptions
from openfor.core import artifacts
from openfor.utils.loader import load_classes
from openfor.extractors import BaseExtractor
from openfor.utils import filesystem


class AsyncProcessor:
    def __init__(self):
        self._jobs = []
    
    def add_job(self, job):
        self._jobs.append(job)

    async def worker(self, q):
        while True:
            job = await q.get()
            extractor = job['extractor']
            logger.info(f"Running extractor {extractor.name} against {job['file']}")
            try:
                extractor().run(artifact_file_path=job['file'], output_folder=job['output_folder'])
            except Exception as err:
                logger.critical(f"Error while executing {extractor.name}: {err}")
            q.task_done()

    async def process(self):
        q = asyncio.Queue()
        for job in self._jobs:
            q.put_nowait(job)

        workers = []
        for _ in range(settings.parallel_tasks):
            worker = asyncio.create_task(self.worker(q))
            workers.append(worker)

        await q.join()
        logger.info("Tasks all finished, stopping workers.")
        for worker in workers:
            worker.cancel()

class   Engine:
    def __init__(self):
        available_extractors = load_classes(
            root_path='openfor/extractors',
            parent_class=BaseExtractor,
        )
        self._available_extractors = {e.name: e for e in available_extractors}
        self._extractors = []
        self._processor = AsyncProcessor()

    @property
    def extractors(self):
        return self._extractors

    @extractors.setter
    def extractors(self, extractors: List[str]):
        self._extractors = []

        for extractor in extractors:
            if extractor not in self._available_extractors:
                raise exceptions.ExtractorNotFound(extractor)
            self._extractors.append(self._available_extractors[extractor])

    def _add_file(self, f: str, output_folder: Path):
        t = artifacts.get_file_type(f)

        if t == artifacts.ArtifactType.UNKNOWN:
            logger.info(f"Skip unknown artifact {f}")
            return


        """
        if isinstance(t, artifacts.CompressedArtifactType):
            filesystem.uncompress(f, intermediate_output_folder, t)
        """
        intermediate_output_folder = None
        for extractor in self.extractors:
            if t != extractor.input_artifact_type:
                continue

            if not intermediate_output_folder:
                intermediate_output_folder = output_folder / f.stem.replace(" ", "_")
                intermediate_output_folder.mkdir(exist_ok=True)


            output_folder = intermediate_output_folder / extractor.name
            output_folder.mkdir(exist_ok=True)

            self._processor.add_job({
                "file": f,
                "extractor": extractor,
                "output_folder": output_folder
            })


    def run(self, files: List[str], output_folder: str):

        # Create root output folder
        root_output_folder = Path(output_folder)
        if root_output_folder.exists() and not root_output_folder.is_dir():
            raise ValueError(f"Output folder {output_folder} is a file !")
        root_output_folder.mkdir(exist_ok=True)

        timed_output_folder = root_output_folder / str(time.time())
        timed_output_folder.mkdir(exist_ok=True)

        all_files = filesystem.gather_files(files)
        logger.info(f"Found {len(all_files)} files")

        # Add tasks
        for f in all_files:
            self._add_file(f, timed_output_folder)

        # Run asyncio loop
        try:
            asyncio.run(self._processor.process())
        except KeyboardInterrupt:
            print("Caught ^C")

        logger.info("DONE")
