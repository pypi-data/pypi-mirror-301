# pylint: disable=missing-module-docstring
import typing
from .analysis import Analysis
from .common import BundleDict
from .data_file import DataFile

class Analyses:
    """Class Analyses is a container of Analysis objects.
    """

    def __init__(self) -> None:
        self._arr: typing.List[Analysis] = []
        self._iter_index: int = 0

    def __len__(self) -> int:
        return len(self._arr)

    def __iter__(self) -> typing.Generator[Analysis, typing.Any, None]:
        yield from self._arr

    @typing.overload
    def __getitem__(self, k: int) -> Analysis:
        pass

    @typing.overload
    def __getitem__(self, k: slice) -> typing.List[Analysis]:
        pass

    def __getitem__(self, k): # type: ignore
        if isinstance(k, int):
            return self._arr[k]
        return self._arr[k.start:k.stop]

    def add(self, a: Analysis) -> None:
        """Add one Analysis object."""
        self._arr.append(a)

    def get_nb_files(self, cat: str | None = None) -> int:
        """Get the total number of files as paths."""
        return len(self.get_data_files(cat = cat))

    def get_data_files(self, cat: str | None = None) -> typing.List[DataFile]:
        """Get the total number of files as DataFile objects.
        """

        data_files: typing.List[DataFile] = []

        for a in self._arr:
            data_files.extend(a.get_data_files(cat = cat))

        return data_files

    def get_all_categories(self) -> typing.Set[str]:
        """Return all the categories of the analyses."""
        categories = set()
        for a in self._arr:
            categories.update(a.get_all_categories())
        return categories

    @classmethod
    def from_array_of_dicts(cls, arr: typing.Sequence[BundleDict]
                            ) -> typing.Self:
        """Build an Analyses instance."""

        analyses = cls()

        for d in arr:
            analyses.add(Analysis(**d))

        return analyses
