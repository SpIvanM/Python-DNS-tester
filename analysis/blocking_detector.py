def detect_blocking(query_result: QueryResult,
blocking_ip_ranges: List[BlockingIpRange],
custom_blocking_ips: List[str]) -> QueryResult:
"""
Analyzes a raw QueryResult to determine if the domain was blocked by the resolver.
Updates the status field of the QueryResult based on blocking criteria.
"""
if query_result.status == 'Error':
return query_result # Already an error, no blocking detection needed

# Blocking Condition 1: No IPv4 A record returned (NXDOMAIN, SERVFAIL, or no A records in response).
if not query_result.resolved_ips:
    query_result.status = 'Blocked'
    return query_result

# If resolved_ips is not empty, check remaining blocking conditions.
# Blocking Conditions 2 & 3: All returned IPs are non-routable OR match custom blocking IPs.
all_ips_blocked = True
for ip_str in query_result.resolved_ips:
    if not is_valid_ipv4(ip_str):
        # If an invalid IP somehow makes it here, treat it as non-blocking
        # and let other valid IPs determine the status.
        all_ips_blocked = False
        break

    is_ip_in_blocking_range = is_private_or_non_routable_ipv4(ip_str, blocking_ip_ranges)
    is_ip_in_custom_blocking = ip_str in custom_blocking_ips

    if not (is_ip_in_blocking_range or is_ip_in_custom_blocking):
        # If at least one IP is not in any blocking list/range, then not ALL IPs are blocked.
        all_ips_blocked = False
        break

if all_ips_blocked:
    query_result.status = 'Blocked'
else:
    # If it reached here, resolved_ips was not empty, and at least one IP was found
    # to be public/routable AND not in the custom blocking IPs.
    query_result.status = 'Resolved'

return query_result