def is_valid_ipv4(ip_address_str: str) -> bool:
try:
ipaddress.IPv4Address(ip_address_str)
return True
except ipaddress.AddressValueError:
return False

def is_private_or_non_routable_ipv4(ip_address_str: str, blocking_ip_ranges: List[BlockingIpRange]) -> bool:
if not is_valid_ipv4(ip_address_str):
return False

ip_address = ipaddress.IPv4Address(ip_address_str)

# Check against explicit blocking ranges
for block_range in blocking_ip_ranges:
    if ip_address in block_range.network:
        return True

return False