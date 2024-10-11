"""
Module: common

This module contains custom types and functions shared by multiple genelastic scripts.
"""
import argparse
import sys
import typing
import logging

import elastic_transport
import elasticsearch

logger = logging.getLogger('genelastic')

AnalysisMetaData: typing.TypeAlias = typing.Dict[str, str | int]
WetProcessesData: typing.TypeAlias = typing.Dict[str, str | int | float]
BioInfoProcessData: typing.TypeAlias = typing.Dict[str, str | typing.List[str]]
BundleDict: typing.TypeAlias = typing.Dict[str, typing.Any]

AnalysisDocument: typing.TypeAlias = typing.Dict[str, str | None | AnalysisMetaData]
MetadataDocument: typing.TypeAlias = typing.Dict[str, int | str | typing.List[typing.Any | None]]
ProcessDocument: typing.TypeAlias = (typing.Dict[str, str] |
                                     WetProcessesData |
                                     BioInfoProcessData)
BulkItems: typing.TypeAlias = typing.List[typing.Dict[str, str |
                                                           MetadataDocument |
                                                           AnalysisDocument |
                                                           ProcessDocument]]
Bucket: typing.TypeAlias = typing.Dict[str, typing.Dict[typing.Any, typing.Any]]


def connect_to_es(host: str, port: int, usr: str, pwd: str) -> elasticsearch.Elasticsearch:
    """Connect to a remote Elasticsearch database."""
    addr = f"https://{host}:{port}"
    logger.info("Trying to connect to Elasticsearch at %s.", addr)

    try:
        es = elasticsearch.Elasticsearch(
            addr,
            # ssl_assert_fingerprint=args.es_cert_fp,
            # ca_certs=args.es_cert,
            verify_certs=False,
            basic_auth=(usr, pwd)
        )
        logger.info(es.info())
    except elastic_transport.TransportError as e:
        logger.error(e.message)
        sys.exit(1)
    return es


def run_composite_aggregation(es: elasticsearch.Elasticsearch,
                              index: str, query: typing.Dict[str, typing.Any]) \
        -> typing.List[Bucket]:
    """
    Executes a composite aggregation on an Elasticsearch index and returns all paginated results.

    :param es: Elasticsearch client instance.
    :param index: Name of the index to query.
    :param query: Aggregation query to run.
    :return: List of aggregation results.
    """
    # Extract the aggregation name from the query dict.
    agg_name = next(iter(query["aggs"]))
    all_buckets: typing.List[Bucket] = []

    try:
        logger.debug("Running composite aggregation query %s on index '%s'.", query, index)
        response = es.search(index=index, body=query)
    except elasticsearch.NotFoundError as e:
        raise SystemExit(f"Error: {e.message} for index '{index}'.") from e

    while True:
        # Extract buckets from the response.
        buckets: typing.List[Bucket] = response['aggregations'][agg_name]['buckets']
        all_buckets.extend(buckets)

        # Check if there are more results to fetch.
        if 'after_key' in response['aggregations'][agg_name]:
            after_key = response['aggregations'][agg_name]['after_key']
            query['aggs'][agg_name]['composite']['after'] = after_key
            try:
                logger.debug("Running query %s on index '%s'.", query, index)
                response = es.search(index=index, body=query)  # Fetch the next page of results.
            except elasticsearch.NotFoundError as e:
                raise SystemExit(f"Error: {e.message} for index '{index}'.") from e
        else:
            break

    return all_buckets


def get_process_ids(es: elasticsearch.Elasticsearch, index: str, proc_field_name: str) \
        -> typing.Set[str]:
    """Return a set of process IDs."""
    process_ids = set()

    query = {
        "size": 0,
        "aggs": {
            "get_proc_ids": {
                "composite": {
                    "sources": {"proc_id": {"terms": {"field": f"{proc_field_name}.keyword"}}},
                    "size": 1000,
                }
            }
        }
    }

    buckets: typing.List[Bucket] = run_composite_aggregation(es, index, query)

    for bucket in buckets:
        process_ids.add(bucket['key']['proc_id'])

    return process_ids


def add_verbose_control_args(parser: argparse.ArgumentParser) -> None:
    """
    Add verbose control arguments to the parser.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_const',
                        const=0, default=1,
                        help='Set verbosity to 0 (quiet mode).')
    parser.add_argument('-v', '--verbose', dest='verbose', action='count',
                        default=1,
                        help=('Verbose level. -v for information, -vv for debug,' +
                              ' -vvv for trace.'))


def add_es_connection_args(parser: argparse.ArgumentParser) -> None:
    """
    Add arguments to the parser needed to gather ElasticSearch server connection parameters.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument('--es-host', dest='es_host', default='localhost',
                        help='Address of Elasticsearch host.')
    parser.add_argument('--es-port', type=int, default=9200, dest='es_port',
                        help='Elasticsearch port.')
    parser.add_argument('--es-usr', dest='es_usr', default='elastic',
                        help='Elasticsearch user.')
    parser.add_argument('--es-pwd', dest='es_pwd', required=True,
                        help='Elasticsearch password.')
    parser.add_argument('--es-cert', dest='es_cert',
                        help='Elasticsearch certificate file.')
    parser.add_argument('--es-cert-fp', dest='es_cert_fp',
                        help='Elasticsearch certificate fingerprint.')
    parser.add_argument('--es-index-prefix', dest='es_index_prefix',
                        help='Add the given prefix to each index created during import.')
