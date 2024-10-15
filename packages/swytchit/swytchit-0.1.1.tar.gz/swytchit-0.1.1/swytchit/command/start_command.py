
from argparse import ArgumentParser
import os
from pathlib import Path
import subprocess
import sys
from swytchit.command import SwytchitCommand

import wizlib

from swytchit.error import SwytchitError

RCFILE = '.swytchitrc'


class StartCommand(SwytchitCommand):
    name = 'start'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('directory')

    def handle_vals(self):
        super().handle_vals()
        if not wizlib.io.isatty():
            raise SwytchitError('Swytchit only works in interactive tty')
        self.dirpath = Path(self.directory).expanduser().resolve()
        if not (self.dirpath.is_dir()):
            raise SwytchitError(
                'Swytchit requires an existing directory as an argument')
        if not (self.dirpath.is_relative_to(Path.home())):
            raise SwytchitError(
                'Swytchit only operates within user home directory')

    @SwytchitCommand.wrap
    def execute(self):
        # Don't actually do this until we can test it
        shell = self.app.config.get('swytchit-shell') or os.getenv('SHELL')
        # os.environ['SWYTCHIT'] = str(Path(self.directory).absolute())
        # subprocess.run(shell)
        rcfiles = []
        for path in [self.dirpath] + [d for d in self.dirpath.parents]:
            if path.is_relative_to(Path.home()):
                if (path / RCFILE).is_file():
                    rcfiles.append(path / RCFILE)
        command = ''.join([f"source {f};" for f in rcfiles]) + f"exec {shell}"
        os.chdir(self.dirpath)
        subprocess.run([shell, '-c', command])
