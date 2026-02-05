from typing import Literal, List, Optional
from dataclasses import dataclass
import ipaddress


DomainCategory = Literal['Useful', 'Questionable', 'Useless']
QueryStatus = Literal['Resolved', 'Blocked', 'Error']


@dataclass
class DomainConfig:
    name: str
    category: DomainCategory


@dataclass
class DnsResolver:
    url: str
    name: str


@dataclass
class BlockingIpRange:
    network: ipaddress.IPv4Network
    description: str


@dataclass
class QueryResult:
    domain: str
    resolver_url: str
    resolved_ips: List[str]
    latency_ms: Optional[float]
    status: QueryStatus
    domain_category: DomainCategory


# Inferred dataclasses for statistics, not present in original models.py
@dataclass
class PerformanceStats:
    min_latency_ms: Optional[float]
    max_latency_ms: Optional[float]
    median_latency_ms: Optional[float]
    avg_latency_ms: Optional[float]


@dataclass
class BlockingStats:
    total_queries: int
    resolved_queries: int
    blocked_queries: int
    error_queries: int
    overall_blocked_percentage: float  # Percentage of 'Blocked' out of (Resolved + Blocked)


@dataclass
class CategorizedBlockingStats:
    category: DomainCategory
    total_non_error_in_category: int  # Total (Resolved + Blocked) in this category
    blocked_in_category: int
    percentage_blocked_in_category: float