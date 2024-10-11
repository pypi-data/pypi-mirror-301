# pylint: disable=missing-module-docstring
import argparse
import logging
import typing

import elasticsearch
import urllib3

from .logger import configure_logging
from .common import (add_es_connection_args, connect_to_es, add_verbose_control_args, Bucket,
                     run_composite_aggregation, get_process_ids)

logger = logging.getLogger('genelastic')
logging.getLogger('elastic_transport').setLevel(logging.WARNING)  # Disable excessive logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(description='ElasticSearch database info.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     allow_abbrev=False)
    add_verbose_control_args(parser)
    add_es_connection_args(parser)
    parser.add_argument("-y", "--list-bundles", action="store_true",
                        help="List all imported YAML bundles.")
    parser.add_argument("-f", "--list-data-files", action="store_true",
                        help="List all imported data files.")
    parser.add_argument("-w", "--list-wet-processes", action="store_true",
                        help="List all imported wet processes.")
    parser.add_argument("-b", "--list-bi-processes", action="store_true",
                        help="List all imported bio info processes.")
    parser.add_argument("-Y", "--list-data-files-per-bundle", action="store_true",
                        help="For each imported YAML bundle, "
                             "display some info and list its data files.")
    return parser.parse_args()


def list_bundles(es: elasticsearch.Elasticsearch, index: str) -> None:
    """List all imported YAML bundles."""

    query = {
        "size": 0,
        "aggs": {
            "get_bundle_paths": {
                "composite": {
                    "sources": {"bundle_path": {"terms": {"field": "bundle_path.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, index, query)

    print("Imported YAML files")
    print("===================")

    if len(buckets) == 0:
        print("Empty response.", end="\n")
        return

    for bucket in buckets:
        bundle_path = bucket['key']['bundle_path']
        print(f'- {bundle_path}')
    print()


def list_data_files(es: elasticsearch.Elasticsearch, index: str) -> None:
    """List all imported data files."""

    query = {
        "size": 0,
        "aggs": {
            "get_paths": {
                "composite": {
                    "sources": {"path": {"terms": {"field": "path.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, index, query)

    print("Imported data files")
    print("===================")

    if len(buckets) == 0:
        print("Empty response.", end="\n")
        return

    for bucket in buckets:
        bundle_path = bucket['key']['path']
        print(f'- {bundle_path}')
    print()


def list_processes(es: elasticsearch.Elasticsearch, index: str) -> None:
    """List all processes."""
    process_ids = get_process_ids(es, index, "proc_id")

    if len(process_ids) == 0:
        print("Empty response.", end="\n")
        return

    for process_id in process_ids:
        print(f'- {process_id}')
    print()


def list_wet_processes(es: elasticsearch.Elasticsearch, index: str) -> None:
    """List all wet processes."""
    print("Imported wet processes")
    print("======================")
    list_processes(es, index)


def list_bi_processes(es: elasticsearch.Elasticsearch, index: str) -> None:
    """List all bio info processes."""
    print("Imported bi processes")
    print("=====================")
    list_processes(es, index)


def search_doc_by_field_value(es: elasticsearch.Elasticsearch,
                              index: str, field: str, value: str) -> (
        typing.Dict[str, typing.Any] | None):
    """Search a document by a value for a certain field."""
    logger.info("Searching for field '%s' with value '%s' inside index '%s'.",
                field, value, index)
    search_query = {
        "query": {
            "term": {
                f"{field}.keyword": value,
            }
        }
    }

    response = es.search(index=index, body=search_query)

    try:
        return response['hits']['hits'][0]['_source']  # type: ignore
    except KeyError:
        return None


def list_data_files_per_bundle(es: elasticsearch.Elasticsearch, index: str) -> None:
    """For each imported YAML bundle, display some info and list its data files."""
    query = {
        "size": 0,
        "aggs": {
            "data_files": {
                "composite": {
                    "sources": [
                        {
                            "bundle_path": {
                                "terms": {
                                    "field": "bundle_path.keyword"
                                }
                            }
                        }
                    ],
                    "size": 100
                },
                "aggs": {
                    "docs": {
                        "top_hits": {
                            "size": 100
                        }
                    }
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, index, query)

    print("Data files per YAML bundle")
    print("==========================")

    if len(buckets) == 0:
        print("Empty response.", end="\n")
        return

    for bucket in buckets:

        documents = bucket["docs"]["hits"]["hits"]
        if len(documents) == 0:
            continue

        print(f"- Bundle Path: {bucket['key']['bundle_path']}")
        print(f"    -> Wet process: {documents[0]['_source']['metadata']['wet_process']}")
        print(f"    -> Bio info process: {documents[0]['_source']['metadata']['bi_process']}")
        print("    -> Data files:")

        for doc in documents:
            print(f"        - Index: {doc['_source']['file_index']}")
            print(f"          Path: {doc['_source']['path']}")

    print()


def main() -> None:
    """Entry point of the info script."""
    args = read_args()

    configure_logging(args.verbose)
    logger.debug("Arguments: %s", args)
    es = connect_to_es(host=args.es_host, port=args.es_port, usr=args.es_usr, pwd=args.es_pwd)

    analysis_index = f"{args.es_index_prefix}-analyses"
    wet_processes_index = f"{args.es_index_prefix}-wet_processes"
    bi_processes_index = f"{args.es_index_prefix}-bi_processes"

    list_call_count = 0

    if args.list_bundles:
        list_bundles(es, analysis_index)
        list_call_count += 1

    if args.list_data_files:
        list_data_files(es, analysis_index)
        list_call_count += 1

    if args.list_wet_processes:
        list_wet_processes(es, wet_processes_index)
        list_call_count += 1

    if args.list_bi_processes:
        list_bi_processes(es, bi_processes_index)
        list_call_count += 1

    if args.list_data_files_per_bundle:
        list_data_files_per_bundle(es, analysis_index)
        list_call_count += 1

    if list_call_count == 0:
        logger.debug("No list option specified, listing everything.")
        list_bundles(es, analysis_index)
        list_data_files(es, analysis_index)
        list_wet_processes(es, wet_processes_index)
        list_bi_processes(es, bi_processes_index)
        list_data_files_per_bundle(es, analysis_index)


if __name__ == '__main__':
    main()
