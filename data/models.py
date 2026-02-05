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