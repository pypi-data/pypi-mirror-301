import pathlib
from . import utils as ut
from abc import ABC, abstractmethod
import copy


class Job(ABC):
    '''
    Abstract class on which all submission/job scripts classes are based.
    '''

    @property
    @abstractmethod
    def EXTENSION() -> str:
        'Default extension for submission/job script file'
        raise NotImplementedError

    @property
    @abstractmethod
    def SUBMIT_COMMAND() -> str:
        'Submission command for this scheduler'
        raise NotImplementedError

    @property
    def file_path(self) -> pathlib.Path:
        return self._file_path

    @file_path.setter
    def file_path(self, value: str | pathlib.Path):
        if isinstance(value, str):
            self._file_path = pathlib.Path(value).resolve()
        elif isinstance(value, pathlib.Path):
            self._file_path = value.resolve()
        else:
            raise TypeError('file_path should be of type str or Path')
        return

    @property
    def file_relpath(self) -> pathlib.Path:
        return self.file_path.relative_to(pathlib.Path.cwd())


class SlurmJob(Job):
    '''
    Class to generate Slurm submission/job scripts\n

    Submission script format is \n

    ...............\n
    SCHEDULER BLOCK\n
    ...............\n
    CONTENT BLOCK
    ...............\n

    Attributes
    ----------
    job_file: str
        Submission script name
    job_name: str
        --job-name value, default is taken from job_file
    account: str
        --account value
    partition: str
        --partition value
    error: str
        --error value
    output: str
        --output value
    mem_per_cpu: str
        --mem-per-cpu value
    cpus_per_task: str
        --cpus-per-task value
    ntasks_per_node: str
        --ntasks-per-node value
    ntasks: str
        --ntasks value
    nodes: str
        --nodes value
    signal: str
        --signal value
    qos: str
        --qos value
    gpus_per_node: str
        --gpus-per-node
    time: str
        --time value
    content_block: str
        Commands to include in jobscript after scheduler block
    '''

    #: Submission/job script file extension
    EXTENSION: str = '.slm'

    #: Submission command for this scheduler
    SUBMIT_COMMAND: str = 'sbatch'

    __slots__ = [
        'job_name',
        'account',
        'partition',
        'error',
        'output',
        'mem_per_cpu',
        'cpus_per_task',
        'ntasks',
        'ntasks_per_node',
        'nodes',
        'signal',
        'qos',
        'gpus_per_node',
        'time',
        'content_block',
        'mail_user',
        'mail_type',
    ]

    def __init__(self, file: str | pathlib.Path, **kwargs) -> None:

        # Get set file path with setter
        self.file_path = file

        # Slurm flag defaults
        self.job_name = copy.copy(self.file_path.stem)
        self.account = ''
        self.partition = ''
        self.error = ''
        self.output = ''
        self.mem_per_cpu = ''
        self.cpus_per_task = ''
        self.ntasks = ''
        self.ntasks_per_node = ''
        self.nodes = ''
        self.signal = ''
        self.qos = ''
        self.gpus_per_node = ''
        self.time = ''
        self.mail_user = ''
        self.mail_type = ''
        self.interpreter_directive = '#!/bin/bash -l'

        self.content_block = ''

        # User values
        for key, value in kwargs.items():
            setattr(self, key, value)

        return

    def write_script(self, verbose: bool = True):
        '''
        Writes submission script to file

        Parameters
        ----------
        verbose: bool, default True
            If True, jobscript location is written to screen
        '''

        with open(self.file_path, 'w') as f:
            f.write('{} \n\n'.format(self.interpreter_directive))
            for attr in self.__slots__:
                if attr not in ['content_block'] and len(str(getattr(self, attr))): # noqa
                    f.write(
                        '#SBATCH --{}={}\n'.format(
                            attr.replace('_', '-'),
                            getattr(self, attr)
                        )
                    )
            f.write('\n')
            f.write(self.content_block)

        if verbose:
            ut.cprint(f'Jobscript written to {self.file_relpath}', 'blue')

        return
