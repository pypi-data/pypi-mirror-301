# pylint: disable=missing-module-docstring
import copy
import glob
import logging
import os
import re
import typing
from pathlib import Path

from .common import AnalysisMetaData
from .constants import ALLOWED_CATEGORIES
from .data_file import DataFile
from .filename_pattern import FilenamePattern
from .tags import Tags

logger = logging.getLogger('genelastic')


class Analysis:
    """Class Analysis that represents an analysis."""

    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 tags: Tags,
                 root_dir: str = '.',
                 bundle_file: str | None = None,
                 file_prefix: str | None = None,
                 files: typing.Sequence[str] | None = None,
                 data_path: str | None = None,
                 **metadata: str | int) -> None:
        self._bundle_file = bundle_file
        self._file_prefix = file_prefix
        self._files = files
        self._data_path = Analysis._resolve_data_path(root_dir, data_path)
        self._tags = tags
        self._metadata: AnalysisMetaData = metadata
        self._categories: typing.Set[str] = set()

    @property
    def metadata(self) -> AnalysisMetaData:
        """Get metadata."""
        return copy.deepcopy(self._metadata)

    @property
    def bundle_file(self) -> str | None:
        """Get the bundle file."""
        return self._bundle_file

    @property
    def filename_regex(self) -> str:
        """
        Resolve placeholders in a file prefix using metadata
        and unresolved placeholders are converted to regex groups
        """

        x: str = r"^.+\.(?P<ext>vcf|cov)(\.gz)?$"

        # Use existing generic prefix
        if self._file_prefix:
            x = self._file_prefix
            # Replace %* tags
            for tag_name, tag_attrs in self._tags.items:
                field = tag_attrs["field"]
                regex = tag_attrs["regex"]

                # Build field regex
                field_regex = (f"(?P<{field}>{self._metadata.get(field)})"
                               if field in self._metadata else
                               f"(?P<{field}>{regex})")
                # Replace tag with field regex
                x = x.replace(tag_name, field_regex)

            # Check for tags that were not replaced.
            groups = re.findall(self._tags.search_regex, x)
            for match in groups:
                logger.warning("String '%s' in key 'file_prefix' looks like an undefined tag. "
                               "If this string is not a tag, you can ignore this warning.",
                               match)

            # Add missing start and end markers
            if not x.startswith("^"):
                x = "^" + x
            if not x.endswith("$"):
                x += (r"\.(?P<ext>" + '|'.join(ALLOWED_CATEGORIES)
                      + r")(\.gz)?$")
            logger.debug("File regex for %s: %s", self._bundle_file, x)

        return x

    def get_nb_files(self, cat: str | None = None) -> int:
        """Returns the total number of files.
        """
        return len(self.get_file_paths(cat=cat))

    def get_data_files(self, cat: str | None = None) -> typing.List[DataFile]:
        """Returns the list of matched files as DataFile objects.
        """

        files = self.get_file_paths(cat=cat)
        filename_pattern = FilenamePattern(self.filename_regex)

        data_files: typing.List[DataFile] = []

        for f in files:
            try:
                data_files.append(DataFile.make_from_bundle(
                    path=f, bundle_path=self._bundle_file,
                    pattern=filename_pattern))
            except (IOError, ValueError) as e:
                logger.error("Error processing file %s: %s", f, str(e))

        return data_files

    def get_file_paths(self, cat: str | None = None) -> typing.Sequence[str]:
        """Returns the list of matched files.
        """
        files, _, _ = self._do_get_file_paths(cat=cat)
        return files

    def get_unmatched_file_paths(self, cat: str | None = None
                                 ) -> typing.Sequence[str]:
        """Returns the list of unmatched files.
        """
        _, files, _ = self._do_get_file_paths(cat=cat)
        return files

    def get_all_categories(self) -> typing.Set[str]:
        """Returns all categories of the analysis."""
        _, _, categories = self._do_get_file_paths()
        return categories

    @staticmethod
    def _resolve_data_path(root_dir: str, data_path: str | None) -> str:
        resolved_data_path = '' if data_path is None else data_path

        if not os.path.isabs(resolved_data_path):
            resolved_data_path = os.path.abspath(os.path.join(root_dir, resolved_data_path))

        return resolved_data_path

    def _get_files_with_allowed_categories(self) -> typing.Dict[str, str]:
        # Create a dict to store allowed files. Keys are the filepaths,
        # and values are their corresponding category.
        allowed_files: typing.Dict[str, str] = {}
        # If files are listed explicitly in the YAML in the 'files' attribute, process them.
        if self._files is not None:
            abs_filepaths = [Path(self._data_path) / f for f in self._files]
            # Try to retrieve files matching allowed categories by checking their first suffix.
            for file in abs_filepaths:
                cat = file.suffixes[0][1:]
                # Add each matching file and its category to the dict.
                if cat in ALLOWED_CATEGORIES:
                    allowed_files[str(file)] = cat
        # Else, look for files on disk using the YAML 'data_path' attribute.
        else:
            # Try to retrieve files matching allowed categories using glob.
            for cat in ALLOWED_CATEGORIES:
                glob_res = []
                glob_res.extend(glob.glob(os.path.join(self._data_path, f"*.{cat}")))
                glob_res.extend(glob.glob(os.path.join(self._data_path, f"*.{cat}.gz")))

                # Add each globed file and its category to the dict.
                for g_file in glob_res:
                    allowed_files[g_file] = cat

        return allowed_files

    def _do_get_file_paths(self, cat: str | None = None) \
            -> tuple[typing.Sequence[str], typing.Sequence[str], typing.Set[str]]:

        # Raise an error if the category given as a parameter is not part of the allowed categories.
        if cat is not None and cat not in ALLOWED_CATEGORIES:
            raise ValueError(f"Unknown category {cat}.")

        # Obtain a dict of all files matching the allowed categories.
        allowed_files = self._get_files_with_allowed_categories()

        if cat is None:
            # No category was given as a parameter, so we match all categories.
            files_to_match = allowed_files
        else:
            # A category was given as a parameter, so we match only this specific category.
            files_to_match = dict((k, v) for (k, v) in allowed_files.items() if v == cat)

        filename_pattern = FilenamePattern(self.filename_regex)
        matching_files: typing.List[str] = []
        non_matching_files: typing.List[str] = []
        categories = set()

        # We filter files by ensuring that they match the filename pattern defined in the analysis.
        for file, category in sorted(files_to_match.items()):
            if filename_pattern.matches_pattern(os.path.basename(file)):
                matching_files.append(file)
                logger.info("MATCHED file %s.", file)
                # Add the file category to the categories set.
                categories.add(category)
            else:
                logger.warning("UNMATCHED file %s.", file)
                non_matching_files.append(file)
        return matching_files, non_matching_files, categories
