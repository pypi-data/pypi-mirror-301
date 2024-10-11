"""
This module defines the DataFile class, which handles the representation,
management, and extraction of metadata for a data file within a data bundle.

It includes functionality to construct DataFile instances from paths and
optional filename patterns, retrieve file paths and metadata, and support
for extracting metadata from filenames using specified patterns.
"""

import logging
import os
import pathlib
import typing
from .filename_pattern import FilenamePattern
from .common import AnalysisMetaData

logger = logging.getLogger('genelastic')


class DataFile:
    """Class for handling a data file and its metadata."""

    # Initializer
    def __init__(self, path: str, bundle_path: str | None = None,
                 metadata: typing.Optional[AnalysisMetaData] = None) -> None:
        self._path = path
        self._bundle_path = bundle_path  # The bundle YAML file in which this
        # file was listed.
        self._metadata = {} if metadata is None else metadata

    def __repr__(self) -> str:
        return (f"File {self._path}, from bundle {self._bundle_path}"
                + f", with metadata {self._metadata}")

    # Get path
    @property
    def path(self) -> str:
        """Retrieve the data file path."""
        return self._path

    def exists(self) -> bool:
        """Tests if the associated file exists on disk."""
        return os.path.isfile(self._path)

    # Get bundle path
    @property
    def bundle_path(self) -> str | None:
        """Retrieve the path to the associated data bundle file."""
        return self._bundle_path

    # Get metadata
    @property
    def metadata(self) -> AnalysisMetaData:
        """Retrieve a copy of the metadata associated with the data file."""
        return self._metadata.copy()

    # Factory
    @classmethod
    def make_from_bundle(
            cls,
            path: str,
            bundle_path: str | None,
            pattern: typing.Optional[FilenamePattern] = None) -> 'DataFile':
        """Construct a DataFile instance from a bundle path, file path,
        and optional filename pattern."""
        # Make absolute path
        if not os.path.isabs(path) and not bundle_path is None:
            path = os.path.join(os.path.dirname(bundle_path), path)

        # Extract filename metadata
        metadata = None
        if pattern is not None:
            metadata = pattern.extract_metadata(os.path.basename(path))

        if metadata:
            if "ext" not in metadata:
                metadata["ext"] = pathlib.Path(path).suffixes[0][1:]

            if "cov_depth" in metadata:
                metadata["cov_depth"] = int(metadata["cov_depth"])

        return cls(path, bundle_path, metadata)
