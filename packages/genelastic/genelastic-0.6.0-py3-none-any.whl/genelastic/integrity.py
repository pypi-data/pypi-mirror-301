# pylint: disable=missing-module-docstring
import argparse
import logging
import typing

import elasticsearch
import urllib3
from elasticsearch import NotFoundError

from .common import (add_verbose_control_args, add_es_connection_args,
                     connect_to_es, get_process_ids, Bucket, run_composite_aggregation)
from .logger import configure_logging


logger = logging.getLogger('genelastic')
logging.getLogger('elastic_transport').setLevel(logging.WARNING)  # Disable excessive logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DBIntegrityError(Exception):
    """Represents an integrity error,
    raised when the database content does not match the expected data schema.
    """

def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(description='Utility to check the integrity '
                                                 'of the genelastic ElasticSearch database.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     allow_abbrev=False)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)
    return parser.parse_args()


def ensure_unique(es: elasticsearch.Elasticsearch, index: str, field: str) -> None:
    """
    Ensure that all values of a field in an index are all unique.

    :param es: Elasticsearch database instance.
    :param index: Name of the index.
    :param field: Field name to check for value uniqueness.
    :raises DBIntegrityError: Some values of the given field are duplicated in the index.
    """

    logger.info("Ensuring that the field '%s' in the index '%s' only contains unique values...",
                field, index)
    query = {
        "size": 0,
        "aggs": {
            "duplicate_proc_ids": {
                "terms": {
                    "field": f"{field}.keyword",
                    "size": 10000,
                    "min_doc_count": 2
                }
            }
        }
    }
    buckets: typing.List[Bucket] = run_composite_aggregation(es, index, query)
    duplicated_processes: typing.Set[str] = set(map(lambda bucket: str(bucket["key"]), buckets))

    if len(duplicated_processes) > 0:
        raise DBIntegrityError(f"Found non-unique value for field {field} in index '{index}': "
                               f"{", ".join(duplicated_processes)}.")

    logger.info("All values of field '%s' in index '%s' are unique.",
                field, index)


def check_for_undefined_file_indices(es: elasticsearch.Elasticsearch, analyses_index: str) -> None:
    """
    Check for potentially undefined files indices in the analyses index.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :raises DBIntegrityError: Some files indices are used in the analyses index but
        are undefined.
    """
    logger.info("Checking for references to undefined file indices in the index '%s'...",
                analyses_index)

    undefined_indices = set()

    query = {
        "size": 0,
        "aggs": {
            "get_file_indices": {
                "composite": {
                    "sources": {"file_index": {"terms": {"field": "file_index.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, analyses_index, query)

    for bucket in buckets:
        file_index = bucket['key']['file_index']

        try:
            es.indices.get(index=file_index)
            logger.debug("File index %s used in index '%s' is defined.",
                         file_index, analyses_index)
        except NotFoundError:
            logger.debug("File index %s used in '%s' is undefined.",
                         file_index, analyses_index)
            undefined_indices.add(file_index)

    if len(undefined_indices) > 0:
        raise DBIntegrityError(f"Found the following undefined file indices defined "
                               f"in the index '{analyses_index}': "
                               f"{", ".join(undefined_indices)}")

    logger.info("All defined file indices are referenced.")


def get_undefined_processes(es: elasticsearch.Elasticsearch, analyses_index: str,
                            process_index: str, field: str) -> typing.Set[str]:
    """
    Return a set of undefined processes IDs in an index.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param process_index: Name of the index to check for undefined processes.
    :param field: Field name used to retrieve the process ID.
    :returns: A set of undefined processes IDs.
    """
    query = {
        "size": 0,
        "aggs": {
            "get_analyses_processes": {
                "composite": {
                    "sources": { "process": {"terms": {"field": f"{field}.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, analyses_index, query)

    used_processes = set(map(lambda bucket: bucket["key"]["process"], buckets))
    logger.debug("Used values for field '%s' in index '%s': %s",
                 field, analyses_index, used_processes)

    defined_processes = get_process_ids(es, process_index, "proc_id")
    logger.debug("Defined values in index '%s': %s", process_index, defined_processes)

    return used_processes.difference(defined_processes)


def check_for_undefined_wet_processes(es: elasticsearch.Elasticsearch,
                                      analyses_index: str, wet_process_index: str) -> None:
    """
    Check that each wet process used in the analyses index is defined.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param wet_process_index: Name of the index where wet processes are stored.
    :raises DBIntegrityError: Some wet processes used in the analyses index are undefined.
    """
    logger.info("Checking for undefined wet processes used in index '%s'...", analyses_index)
    undefined_wet_processes = get_undefined_processes(es, analyses_index, wet_process_index,
                                                      "metadata.wet_process")

    if len(undefined_wet_processes) > 0:
        raise DBIntegrityError(f"Index '{analyses_index}' uses the following "
                               f"undefined wet processes: {", ".join(undefined_wet_processes)}.")

    logger.info("All wet processes used in index '%s' are defined.", wet_process_index)


def check_for_undefined_bi_processes(es: elasticsearch.Elasticsearch,
                                     analyses_index: str, bi_process_index: str) -> None:
    """
    Check that each bio info process used in the analyses index is defined.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param bi_process_index: Name of the index where bio info processes are stored.
    :raises DBIntegrityError: Some bio info processes used in the analyses index are undefined.
    """
    logger.info("Checking for undefined bio info processes used in index '%s'...", analyses_index)
    undefined_bi_processes = get_undefined_processes(es, analyses_index, bi_process_index,
                                                     "metadata.bi_process")

    if len(undefined_bi_processes) > 0:
        raise DBIntegrityError(f"Index '{analyses_index}' uses the following "
                               f"undefined bio info processes: "
                               f"{", ".join(undefined_bi_processes)}.")

    logger.info("All bio info processes used in index '%s' are defined.", bi_process_index)


def check_for_unused_file_indices(es: elasticsearch.Elasticsearch,
                                  analyses_index: str, index_prefix: str) -> int:
    """
    Check that each of the file indices are used in at least one analysis.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param index_prefix: Prefix given to all the indices of the ElasticSearch database.
    :returns: 1 if some file indices exists but are unused in the analyses index,
        and 0 otherwise.
    """
    json_indices = es.cat.indices(index=f"{index_prefix}-file-*", format="json").body
    found_file_indices = set(map(lambda x: x["index"], json_indices))

    query = {
        "size": 0,
        "aggs": {
            "get_file_indices": {
                "composite": {
                    "sources": {"file_index": {"terms": {"field": "file_index.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, analyses_index, query)

    used_files_indices = set(map(lambda bucket: bucket['key']['file_index'], buckets))
    unused_files_indices = found_file_indices.difference(used_files_indices)

    if len(unused_files_indices) > 0:
        logger.warning("Found the following unused files indices: %s",
                       ", ".join(unused_files_indices))
        return 1

    logger.info("All files indices are used.")
    return 0


def check_for_unused_wet_processes(es: elasticsearch.Elasticsearch, analyses_index: str,
                                   wet_proc_index: str) -> int:
    """
    Check for defined wet processes that are not used in the analyses index.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param wet_proc_index: Name of the index where wet processes are stored.
    :returns: 1 if some wet process are defined but unused in the analyses index,
        and 0 otherwise.
    """
    logger.info("Checking for unused wet processes in the index '%s'...", wet_proc_index)

    defined_wet_procs = get_process_ids(es, wet_proc_index, "proc_id")
    logger.debug("Found the following defined wet processes: %s", defined_wet_procs)

    used_wet_procs = get_process_ids(es, analyses_index, "metadata.wet_process")
    logger.debug("Following processes are used in the index '%s': %s",
                 analyses_index, used_wet_procs)

    unused_wet_procs = defined_wet_procs - used_wet_procs
    if len(unused_wet_procs) > 0:
        logger.warning("Found unused wet processes: %s", unused_wet_procs)
        return 1

    logger.info("No unused wet processes found.")
    return 0


def check_for_unused_bi_processes(es: elasticsearch.Elasticsearch, analyses_index: str,
                                  bi_proc_index: str) -> int:
    """
    Check for defined bio info processes that are not used in the analyses index.

    :param es: Elasticsearch database instance.
    :param analyses_index: Name of the index where analyses are stored.
    :param bi_proc_index: Name of the index where bio info processes are stored.
    :returns: 1 if some wet process are defined but unused in the analyses index,
        and 0 otherwise.
    """
    logger.info("Checking for unused bio info processes in the index '%s'...", bi_proc_index)

    defined_bi_procs = get_process_ids(es, bi_proc_index, "proc_id")
    logger.debug("Found the following defined bio info processes: %s", defined_bi_procs)

    used_bi_procs = get_process_ids(es, analyses_index, "metadata.bi_process")
    logger.debug("Following processes are used in the index '%s': %s",
                 analyses_index, used_bi_procs)

    unused_bi_procs = defined_bi_procs - used_bi_procs
    if len(unused_bi_procs) > 0:
        logger.warning("Found unused bio info processes: %s", unused_bi_procs)
        return 1

    logger.info("No unused bio info processes found.")
    return 0


def main() -> None:
    """Entry point of the integrity script."""
    args = read_args()

    configure_logging(args.verbose)
    logger.debug("Arguments: %s", args)

    analyses_index = f"{args.es_index_prefix}-analyses"
    wet_processes_index = f"{args.es_index_prefix}-wet_processes"
    bi_processes_index = f"{args.es_index_prefix}-bi_processes"

    es = connect_to_es(host=args.es_host, port=args.es_port, usr=args.es_usr, pwd=args.es_pwd)

    # Fatal errors
    try:
        ensure_unique(es, wet_processes_index, "proc_id")
        ensure_unique(es, bi_processes_index, "proc_id")
        check_for_undefined_file_indices(es, analyses_index)
        check_for_undefined_wet_processes(es, analyses_index, wet_processes_index)
        check_for_undefined_bi_processes(es, analyses_index, bi_processes_index)
    except DBIntegrityError as e:
        raise SystemExit(e) from e

    # Warnings
    check_for_unused_wet_processes(es, analyses_index, wet_processes_index)
    check_for_unused_bi_processes(es, analyses_index, bi_processes_index)
    check_for_unused_file_indices(es, analyses_index, args.es_index_prefix)


if __name__ == '__main__':
    main()
