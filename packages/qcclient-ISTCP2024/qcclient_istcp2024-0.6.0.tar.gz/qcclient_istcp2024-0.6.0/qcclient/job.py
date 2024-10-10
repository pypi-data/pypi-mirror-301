import logging
import os
import time
import uuid
from contextlib import contextmanager
from pathlib import PosixPath
from tempfile import TemporaryDirectory
from typing import (Any, Callable, Dict, Generator, List, Optional, Tuple, TypeVar)

from . import QCClient, QCConfig

logger = logging.getLogger(__name__)

def generate_id(prefix=None, include_time=True, uuid_len=4):
    if prefix is None:
        prefix = ""
    else:
        prefix = f"{prefix}_"
    if include_time:
        return f"{prefix}{time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:uuid_len]}"
    else:
        return f"{prefix}{uuid.uuid4().hex[:uuid_len]}"

@contextmanager
def temporary_cd(directory_path: Optional[str] = None) -> Generator[None, None, None]:
    if isinstance(directory_path, PosixPath):
        directory_path = directory_path.as_posix()

    if directory_path is not None and len(directory_path) == 0:
        yield
        return

    old_directory = os.getcwd()
    try:
        if directory_path is None:
            with TemporaryDirectory() as new_directory:
                os.chdir(new_directory)
                yield
        else:
            os.makedirs(directory_path, exist_ok=True)
            os.chdir(directory_path)
            yield
    finally:
        os.chdir(old_directory)


class QCJob:
    def __init__(self,
                 input_dir: str,
                 output_dir: str = None,
                 config: QCConfig = None,
                 qcclient: QCClient = None,
                 name: str = 'qcdebug',
                 molecules: list = None,
                 timeout: int = 10):
        self.name = name
        self.input_dir = input_dir
        if not molecules or len(molecules) == 0:
            self.molecules = None
            logger.debug("No molecules provided")
        else:
            for molecule in molecules:
                if molecule is None or molecule.strip() == '':
                    molecules.remove(molecule)
            if len(molecules) == 0:
                self.molecules = None
            else:
                self.molecules = molecules
            logger.debug(f"molecules: {molecules}")
        if config is None:
            self.config = QCConfig(qc_job_type='sp')
        else:
            self.config = config

        self.label = generate_id(name)
        self.job_id = 0
        self.client = qcclient
        if qcclient is None:
            self.client = QCClient(is_submitter=True)
        self._push_input()

        if output_dir is None:
            self.output_dir = os.path.join(self.client.tos_prefix, 'jobs', self.label, "output")
            logger.info(f"Output dir will be assigned to {self.output_dir}")
        else:
            assert output_dir.startswith('tos:'), "Only TOS output is supported"
            self.output_dir = output_dir

    def _push_input(self):
        '''If the input folder is not TOS/S3, upload the entire folder first'''
        remote_dir = self.client.push_input(self.input_dir, self.label)
        self.input_dir = remote_dir

    def _do_submit(self, check=True):
        job_data = {
            "job_type": self.config.qc_job_type,
            "config": self.config,
            "name": self.label,
            "input_url": self.input_dir,
            "result_url": self.output_dir,
            "molecules_list": self.molecules,
        }
        resp = self.client.submit(job_data, check=check)
        logger.info(f"Submitted, {self.label}")
        self.job_id = resp['data']['id']

    def submit(self, check=True):
        self._do_submit(check=check)

    def pull_output(self, local_dir=None):
        if local_dir is None:
            local_dir = self.label
        self.client.pull_output(
            self.job_id,
            local_dir=local_dir)
