import statistics
from typing import List, Dict, Optional
from data.models import QueryResult, DomainCategory
from analysis.models import PerformanceStats, BlockingStats, CategorizedBlockingStats

def calculate_performance_stats(query_results: List[QueryResult]) -> PerformanceStats:
"""
Calculates min, max, median, and average latency for a given set of resolved queries.
Only considers queries with status 'Resolved' and non-null latency.
"""
resolved_latencies = [qr.latency_ms for qr in query_results if qr.status == 'Resolved' and qr.latency_ms is not None]

if not resolved_latencies:
    return PerformanceStats(
        min_latency_ms=None,
        max_latency_ms=None,
        median_latency_ms=None,
        avg_latency_ms=None
    )

return PerformanceStats(
    min_latency_ms=min(resolved_latencies),
    max_latency_ms=max(resolved_latencies),
    median_latency_ms=statistics.median(resolved_latencies),
    avg_latency_ms=statistics.mean(resolved_latencies)
)
def calculate_overall_blocking_percentage(query_results: List[QueryResult]) -> BlockingStats:
"""
Calculates the overall percentage of 'Blocked' queries out of all non-'Error' queries,
and also returns counts for total, resolved, blocked, and error queries.
"""
resolved_count = sum(1 for qr in query_results if qr.status == 'Resolved')
blocked_count = sum(1 for qr in query_results if qr.status == 'Blocked')
error_count = sum(1 for qr in query_results if qr.status == 'Error')

total_non_error = resolved_count + blocked_count
overall_blocked_percentage = 0.0
if total_non_error > 0:
    overall_blocked_percentage = (blocked_count / total_non_error) * 100.0

return BlockingStats(
    total_queries=len(query_results),
    resolved_queries=resolved_count,
    blocked_queries=blocked_count,
    error_queries=error_count,
    overall_blocked_percentage=overall_blocked_percentage
)
def calculate_categorized_blocking_percentages(
query_results: List[QueryResult], categories: List[DomainCategory]
) -> List[CategorizedBlockingStats]:
"""
Calculates the percentage of 'Blocked' queries for each domain category.
"""
categorized_stats: List[CategorizedBlockingStats] = []

# Initialize counts for each category
category_data: Dict[DomainCategory, Dict[str, int]] = {
    category: {"resolved": 0, "blocked": 0, "error": 0}
    for category in categories
}

for qr in query_results:
    if qr.domain_category in category_data:
        if qr.status == 'Resolved':
            category_data[qr.domain_category]["resolved"] += 1
        elif qr.status == 'Blocked':
            category_data[qr.domain_category]["blocked"] += 1
        elif qr.status == 'Error':
            category_data[qr.domain_category]["error"] += 1

for category in categories:
    data = category_data.get(category, {"resolved": 0, "blocked": 0, "error": 0})
    resolved_in_category = data["resolved"]
    blocked_in_category = data["blocked"]
    
    total_non_error_in_category = resolved_in_category + blocked_in_category
    percentage_blocked = 0.0
    if total_non_error_in_category > 0:
        percentage_blocked = (blocked_in_category / total_non_error_in_category) * 100.0
    
    categorized_stats.append(
        CategorizedBlockingStats(
            category=category,
            total_non_error_in_category=total_non_error_in_category,
            blocked_in_category=blocked_in_category,
            percentage_blocked_in_category=percentage_blocked
        )
    )
return categorized_stats
def get_blocked_useful_domains(query_results: List[QueryResult]) -> List[str]:
"""Retrieves a sorted list of unique 'Useful' domains that were 'Blocked'."""
blocked_useful = {qr.domain for qr in query_results if qr.domain_category == 'Useful' and qr.status == 'Blocked'}
return sorted(list(blocked_useful))

def get_blocked_useless_domains(query_results: List[QueryResult]) -> List[str]:
"""Retrieves a sorted list of unique 'Useless' domains that were 'Blocked'."""
blocked_useless = {qr.domain for qr in query_results if qr.domain_category == 'Useless' and qr.status == 'Blocked'}
return sorted(list(blocked_useless))

def get_passed_useless_domains(query_results: List[QueryResult]) -> List[str]:
"""Retrieves a sorted list of unique 'Useless' domains that were 'Resolved'."""
passed_useless = {qr.domain for qr in query_results if qr.domain_category == 'Useless' and qr.status == 'Resolved'}
return sorted(list(passed_useless))