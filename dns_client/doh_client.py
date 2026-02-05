import asyncio
import time
import httpx
from typing import List, Optional, Tuple, Dict, Any
from data.models import QueryResult, DnsResolver, DomainCategory, QueryStatus
from utils.ip_utils import is_valid_ipv4


class DohClient:
    """
    Asynchronous DNS-over-HTTPS (DoH) client for querying DNS records.
    """
    def __init__(self):
        # httpx.AsyncClient should be reused for connection pooling and efficiency.
        # It handles session management internally.
        self._client = httpx.AsyncClient()

    async def query(self,
                    domain_name: str,
                    resolver: DnsResolver,
                    timeout_seconds: float,
                    semaphore: asyncio.Semaphore,
                    domain_category: DomainCategory) -> QueryResult:
        """
        Executes an asynchronous DNS-over-HTTPS (DoH) query for a given domain
        using a specified resolver, measuring latency.
        """
        resolved_ips: List[str] = []
        latency_ms: Optional[float] = None
        status: QueryStatus = 'Error'  # Default to Error, refine later

        # RFC 8484 specifies GET method with 'dns' query parameter for the DNS message
        # and 'ct' query parameter for content type (application/dns-message or application/dns-json)
        # We'll use application/dns-json and query A records.
        doh_url = f"{resolver.url}?name={domain_name}&type=A"

        start_time = time.perf_counter()
        async with semaphore:
            try:
                response = await self._client.get(
                    doh_url,
                    headers={"Accept": "application/dns-json"},
                    timeout=timeout_seconds
                )
                response.raise_for_status()  # Raise an exception for 4xx/5xx responses
                latency_ms = (time.perf_counter() - start_time) * 1000

                response_json = response.json()
                parsed_ips, is_nxdomain, is_servfail = self._parse_doh_response(response_json)
                resolved_ips = parsed_ips

                status = 'Resolved'  # Temporarily set to resolved; blocking_detector will refine it

            except httpx.TimeoutException:
                status = 'Error'
            except httpx.RequestError:  # Covers connection errors, DNS lookup failures before DoH, etc.
                status = 'Error'
            except httpx.HTTPStatusError:  # Covers 4xx/5xx HTTP responses
                status = 'Error'
            except Exception:  # Catch any other unexpected errors during JSON parsing, etc.
                status = 'Error'

        return QueryResult(
            domain=domain_name,
            resolver_url=resolver.url,
            resolved_ips=resolved_ips,
            latency_ms=latency_ms,
            status=status,
            domain_category=domain_category
        )

    def _parse_doh_response(self, response_json: Dict[str, Any]) -> Tuple[List[str], bool, bool]:
        """
        Parses the JSON response from a DoH query (RFC 8484 format)
        to extract IPv4 A records and detect NXDOMAIN/SERVFAIL.
        """
        ips: List[str] = []
        is_nxdomain = False
        is_servfail = False

        status_code = response_json.get('Status')
        if status_code == 3:  # NXDOMAIN
            is_nxdomain = True
        elif status_code == 2:  # SERVFAIL
            is_servfail = True

        # Answers section contains the RRs
        answers = response_json.get('Answer', [])
        for record in answers:
            if record.get('type') == 1:  # Type 1 is A record (IPv4)
                ip = record.get('data')
                if ip and is_valid_ipv4(ip):
                    ips.append(ip)

        return ips, is_nxdomain, is_servfail

    async def close(self):
        """Closes the underlying httpx.AsyncClient session."""
        await self._client.aclose()