import asyncio
import random
import time
from loguru import logger
from typing import List
from pathlib import Path

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
        logger.debug(f"Added job {job}")

    async def worker(self, q):
        while True:
            job = await q.get()
            extractor = job['extractor']
            logger.info(f"Running extractor {extractor.name} against {job['file']}")
            try:
                extractor().run(artifact_file_path=job['file'])
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
        self._extractors = available_extractors
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

    def run(self, files: List[str]):
        all_files = filesystem.gather_files(files)
        logger.info(f"Found {len(all_files)} files")

        for f in all_files:
            t = artifacts.get_file_type(f)
            if t == artifacts.ArtifactType.UNKNOWN:
                logger.info(f"Skip file {f}")
                continue

            for extractor in self.extractors:
                if t == extractor.input_artifact_type:
                    self._processor.add_job({"file": f, "extractor": extractor, "output_folder": })

        try:
            asyncio.run(self._processor.process())
        except KeyboardInterrupt:
            print("Caught ^C")
        logger.info("DONE")
            
