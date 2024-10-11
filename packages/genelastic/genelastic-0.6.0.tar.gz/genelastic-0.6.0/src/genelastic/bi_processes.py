# pylint: disable=missing-module-docstring
import logging
import typing

from .bi_process import BioInfoProcess
from .common import BundleDict

logger = logging.getLogger('genelastic')


class BioInfoProcesses:
    """Class BioInfoProcesses is a container of BioInfoProcess objects."""

    def __init__(self) -> None:
        self._dict: typing.Dict[str, BioInfoProcess] = {}

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, key: str) -> BioInfoProcess:
        return self._dict[key]

    def add(self, process: BioInfoProcess) -> None:
        """Add one BioInfoProcess object.
        If a BioInfoProcess object with the same ID already exists in the container,
        the program exits.
        """
        if process.id in self._dict:
            raise ValueError(f"A bi process with the id '{process.id}' is already present.")

        # Add one WetProcess object.
        self._dict[process.id] = process

    def get_process_ids(self) -> typing.Set[str]:
        """Get a list of the bio processes IDs."""
        return set(self._dict.keys())

    @classmethod
    def from_array_of_dicts(cls, arr: typing.Sequence[BundleDict]
                            ) -> typing.Self:
        """Build a BioInfoProcesses instance."""

        bi_processes = cls()

        for d in arr:
            bi_processes.add(BioInfoProcess(**d))

        return bi_processes
