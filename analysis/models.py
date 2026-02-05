from dataclasses import dataclass
from typing import Optional

@dataclass
class PerformanceStats:
    min_latency_ms: Optional[float]
    max_latency_ms: Optional[float]
    median_latency_ms: Optional[float]
    average_latency_ms: Optional[float]

@dataclass
class BlockingStats:
    blocking_percentage: float
    error_rate: float

@dataclass
class CategorizedBlockingStats:
    category: str
    blocking_percentage: float