# pylint: disable=missing-module-docstring
import argparse
import logging
import os
import random
import subprocess  # nosec
import sys
from typing import Dict, List, Sequence, Collection

import yaml

from genelastic.common import add_verbose_control_args
from .logger import configure_logging

logger = logging.getLogger('genelastic')


def read_args() -> argparse.Namespace:
    # pylint: disable=R0801
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(description='Genetics data random generator.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    add_verbose_control_args(parser)
    parser.add_argument('-d', '--data-folder', dest='data_folder', required=True,
                        help='Data destination folder.')
    parser.add_argument('--log-file', dest='log_file', help='Path to a log file.')
    parser.add_argument('-n', '--chrom-nb', dest='chrom_nb', type=int, default=5,
                        help='Number of chromosomes to generate.')
    parser.add_argument('-o', '--output-yaml-file', dest='output_file', default='-',
                        help='Output YAML file.')
    parser.add_argument('-s', '--chrom-size', dest='chrom_size', type=int, default=2000,
                        help='Data size (number of nucleotides) for each chromosome.')
    return parser.parse_args()


def gen_cov_files(folder: str, nb_chrom: int, chrom_sz: int, prefix: str) -> List[str]:
    """Generate dummy coverage files. If an error occurs while generating coverage files, exit."""
    files = []
    chrom_end = chrom_sz - 1

    for chrom in range(1, nb_chrom + 1):
        output_path = os.path.join(folder, f"{prefix}_chr{chrom}_cov.tsv")

        # gen-cov will output a coverage file to stdout.
        gen_cov_cmd = ["gen-cov", "-c", str(chrom), "-p", f"0-{chrom_end}", "-d", "5-15",
                       "-r", "0.1"]

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                # Redirect the gen-cov output to a file.
                subprocess.run(gen_cov_cmd, stdout=f, check=True)  # nosec

        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            logger.error(e)
            sys.exit(1)

        files.append(output_path)

    return files


def gen_vcf_files(folder: str, nb_chrom: int, chrom_sz: int, prefix: str) -> List[str]:
    """Generate dummy VCF files. If an error occurs while generating VCFs, exit."""
    files = []
    for chrom in range(1, nb_chrom + 1):
        output_path = os.path.join(folder, f"{prefix}_chr{chrom}.vcf")

        # gen-fasta will output a FASTA to stdout.
        gen_fasta_cmd = ["gen-fasta", "-s", f"chr{chrom}", "-n", str(chrom_sz)]
        # gen-vcf will output a VCF to stdout.
        gen_vcf_cmd = ["gen-vcf", "--snp-rate", "0.02", "--ins-rate", "0.01", "--del-rate", "0.01"]

        try:
            # Pipe the output of gen-fasta to the stdin of gen-vcf.
            with subprocess.Popen(gen_fasta_cmd, stdout=subprocess.PIPE) as gen_fasta_proc:  # nosec
                # Redirect the gen-vcf output to a file.
                with open(output_path, "w", encoding="utf-8") as f:
                    subprocess.run(gen_vcf_cmd,
                                   stdin=gen_fasta_proc.stdout, stdout=f, check=True)  # nosec
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
            logger.error(e)
            sys.exit(1)

        files.append(output_path)

    return files


def gen_name(chars: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', n: int = 4) -> str:
    """Generate a random alphanumerical name."""
    return ''.join(random.sample(list(chars), n))


def gen_data(folder: str, nb_chrom: int, chrom_sz: int) -> (
        Dict)[str, int | Sequence[Collection[str]]]:
    """Generate dummy analysis following the V3 YAML schema."""
    # Set metadata
    sample_name = "HG0003"
    source = "CNRGH"
    barcode = gen_name(n=6)
    wet_process = "novaseqxplus-10b"
    bi_process = "dragen-4123"
    reference_genome = "hg38"
    prefix = f'{sample_name}_{source}_{wet_process}_{bi_process}_{barcode}_{reference_genome}'

    wet_processes = [{
        "proc_id": "novaseqxplus-10b",
        "manufacturer": "illumina",
        "sequencer": "novaseqxplus",
        "generic_kit": "truseq-illumina",
        "fragmentation": 350,
        "reads_size": 300,
        "input_type": "gdna",
        "amplification": "pcr-free",
        "flowcell_type": "10b",
        "sequencing_type": "wgs",
    }]

    bi_processes = [{
        "proc_id": "dragen-4123",
        "name": "dragen",
        "pipeline_version": "4.1.2.3",
        "steps": [
            {"name": "basecalling", "cmd": "bclconvert", "version": "3.9.3.2"},
            {"name": "trimming", "cmd": "dragen"},
            {"name": "mapping", "cmd": "dragmap"},
            {"name": "postmapping", "cmd": "dragen", "version": "4.1.23"},
            {"name": "smallvarcalling", "cmd": "dragen", "version": "4.1.23"},
            {"name": "svcalling", "cmd": "dragen", "version": "4.1.23"},
            {"name": "secondary_qc", "cmd": "dragen", "version": "4.1.23"}
        ],
        "sequencing_type": "wgs"
    }]

    analyses = [{
        'file_prefix': '%S_%F_%W_%B_%A_%R_chr[0-9]+',
        'sample_name': sample_name,
        'source': source,
        'barcode': barcode,
        'wet_process': "novaseqxplus-10b",
        'bi_process': "dragen-4123",
        'reference_genome': reference_genome,
        'flowcell': gen_name(n=8),
        'lanes': [random.randint(1, 10)],  # nosec
        'seq_indices': ['DUAL219', 'DUAL222', 'DUAL225', 'DUAL228', 'DUAL289'],
        'qc_comment': "",
        'data_path': folder,
    }]

    gen_vcf_files(folder, nb_chrom=nb_chrom, chrom_sz=chrom_sz, prefix=prefix)
    gen_cov_files(folder, nb_chrom=nb_chrom, chrom_sz=chrom_sz, prefix=prefix)

    return {
        'version': 3,
        'analyses': analyses,
        'bi_processes': bi_processes,
        'wet_processes': wet_processes
    }


# Write import bundle YAML
def write_yaml(file: str, data: Dict[str, int | Sequence[Collection[str]]]) -> None:
    """Write YAML to stdout or in a file."""
    # Standard output
    if file == '-':
        print('---')
        yaml.dump(data, sys.stdout)

    # File
    else:
        with open(file, 'w', encoding="utf-8") as f:
            print('---', file=f)
            yaml.dump(data, f)


def main() -> None:
    """Entry point of the gen-data script."""
    # Read command line arguments
    args = read_args()

    # Configure logging
    configure_logging(args.verbose, log_file=args.log_file)
    logger.debug("Arguments: %s", args)

    # Generate data
    data = gen_data(args.data_folder, nb_chrom=args.chrom_nb, chrom_sz=args.chrom_size)

    # Write to stdout or file
    write_yaml(args.output_file, data)


if __name__ == '__main__':
    main()
