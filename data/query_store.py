from typing import List, Dict
from data.models import QueryResult

class QueryStore:
"""
In-memory repository for storing and retrieving QueryResult objects.
"""
def init(self):
self._results: List[QueryResult] = []

def add_result(self, result: QueryResult):
    """Adds a single QueryResult object to the store."""
    self._results.append(result)

def get_results(self,
                resolver_url: Optional[str] = None,
                domain_name: Optional[str] = None,
                status: Optional[QueryStatus] = None,
                domain_category: Optional[DomainCategory] = None) -> List[QueryResult]:
    """
    Retrieves filtered QueryResult objects from the store.
    Filters are applied cumulatively.
    """
    filtered_results = self._results

    if resolver_url:
        filtered_results = [r for r in filtered_results if r.resolver_url == resolver_url]
    if domain_name:
        filtered_results = [r for r in filtered_results if r.domain == domain_name]
    if status:
        filtered_results = [r for r in filtered_results if r.status == status]
    if domain_category:
        filtered_results = [r for r in filtered_results if r.domain_category == domain_category]

    return filtered_results

def get_all_resolvers(self) -> List[str]:
    """Returns a list of all unique resolver URLs present in the store."""
    return sorted(list({r.resolver_url for r in self._results}))

def get_all_domains(self) -> List[str]:
    """Returns a list of all unique domain names present in the store."""
    return sorted(list({r.domain for r in self._results}))