# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import genelastic
from genelastic.tags import Tags


def test_empty_analysis() -> None:
    a = genelastic.Analysis(Tags(None))
    assert a.get_nb_files() == 0
    assert a.get_nb_files('vcf') == 0


def test_empty_analysis_one_file() -> None:
    a = genelastic.Analysis(Tags(None), files=['a.vcf'])
    assert a.get_nb_files() == 1
    assert a.get_nb_files('vcf') == 1
    assert a.get_nb_files('cov') == 0
