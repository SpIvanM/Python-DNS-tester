from typing import Optional
import argparse
from dataclasses import dataclass
from config.settings import DEFAULT_OUTPUT_FILE, DEFAULT_CONCURRENCY_LIMIT, DEFAULT_TIMEOUT_SECONDS


@dataclass
class ParsedArguments:
    domain_list_path: Optional[str]
    resolver_list_path: str
    output_file: str
    concurrency_limit: int
    timeout_seconds: float
    custom_blocking_ips_path: Optional[str]


def parse_arguments() -> ParsedArguments:
    """
    Parses command-line arguments for script configuration.
    """
    parser = argparse.ArgumentParser(
        description="DNS Analyzer: Evaluate DoH resolvers against categorized domains."
    )

    parser.add_argument(
        "--domains",
        dest="domain_list_path",
        type=str,
        default=None,
        help="Path to a text file containing additional domain names (one per line). "
             "If not provided, a hardcoded list expanded to 100 domains is used."
    )
    parser.add_argument(
        "--resolvers",
        dest="resolver_list_path",
        type=str,
        required=True,
        help="Path to a text file containing DoH resolver URLs (one per line)."
    )
    parser.add_argument(
        "--output",
        dest="output_file",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Path for the output Excel report. Default: '{DEFAULT_OUTPUT_FILE}'"
    )
    parser.add_argument(
        "--concurrency",
        dest="concurrency_limit",
        type=int,
        default=DEFAULT_CONCURRENCY_LIMIT,
        help=f"Maximum number of concurrent DoH queries. Default: {DEFAULT_CONCURRENCY_LIMIT}"
    )
    parser.add_argument(
        "--timeout",
        dest="timeout_seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Timeout in seconds for each individual DoH query. Default: {DEFAULT_TIMEOUT_SECONDS}s"
    )
    parser.add_argument(
        "--custom-blocking-ips",
        dest="custom_blocking_ips_path",
        type=str,
        default=None,
        help="Path to a text file containing user-defined specific blocking IPv4 addresses (one per line)."
    )

    args = parser.parse_args()

    return ParsedArguments(
        domain_list_path=args.domain_list_path,
        resolver_list_path=args.resolver_list_path,
        output_file=args.output_file,
        concurrency_limit=args.concurrency_limit,
        timeout_seconds=args.timeout_seconds,
        custom_blocking_ips_path=args.custom_blocking_ips_path
    )