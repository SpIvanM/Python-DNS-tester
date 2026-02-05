import re
from typing import List
from data.models import DnsResolver


def load_resolvers(file_path: str) -> List[DnsResolver]:
    """
    Loads and validates a list of DoH resolver URLs from a file.
    Each URL should be on a new line. Invalid URLs are ignored.
    """
    resolvers = []
    # Basic URL validation regex - more robust validation would use a proper URL parsing library
    # but for simple DoH URLs, this covers common cases.
    url_regex = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and url_regex.match(url):
                    # Derive a simple name from the URL or use URL itself
                    name = url.split('//')[-1].split('/')[0]
                    resolvers.append(DnsResolver(url=url, name=name))
                elif url:
                    print(f"Warning: Invalid or malformed resolver URL skipped: '{url}'")
    except FileNotFoundError:
        print(f"Error: Resolver list file not found at '{file_path}'. Please create it with DoH URLs.")
    except Exception as e:
        print(f"Error loading resolvers from '{file_path}': {e}")
    return resolvers