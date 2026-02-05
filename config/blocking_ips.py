import ipaddress
from typing import List
from data.models import BlockingIpRange
from utils.ip_utils import is_valid_ipv4


def load_blocking_ip_ranges() -> List[BlockingIpRange]:
    """
    Loads predefined private and non-routable IPv4 ranges.
    """
    ranges = [
        BlockingIpRange(ipaddress.IPv4Network('0.0.0.0/8'), "Non-routable (current network)"),
        BlockingIpRange(ipaddress.IPv4Network('10.0.0.0/8'), "Private-use (Class A)"),
        BlockingIpRange(ipaddress.IPv4Network('100.64.0.0/10'), "Shared Address Space (CGN)"),
        BlockingIpRange(ipaddress.IPv4Network('127.0.0.0/8'), "Loopback"),
        BlockingIpRange(ipaddress.IPv4Network('169.254.0.0/16'), "Link-Local"),
        BlockingIpRange(ipaddress.IPv4Network('172.16.0.0/12'), "Private-use (Class B)"),
        BlockingIpRange(ipaddress.IPv4Network('192.0.0.0/24'), "IETF Protocol Assignments"),
        BlockingIpRange(ipaddress.IPv4Network('192.0.2.0/24'), "TEST-NET-1"),
        BlockingIpRange(ipaddress.IPv4Network('192.88.99.0/24'), "6to4 Relay Anycast"),
        BlockingIpRange(ipaddress.IPv4Network('192.168.0.0/16'), "Private-use (Class C)"),
        BlockingIpRange(ipaddress.IPv4Network('198.18.0.0/15'), "Benchmark and Testing"),
        BlockingIpRange(ipaddress.IPv4Network('198.51.100.0/24'), "TEST-NET-2"),
        BlockingIpRange(ipaddress.IPv4Network('203.0.113.0/24'), "TEST-NET-3"),
        BlockingIpRange(ipaddress.IPv4Network('224.0.0.0/4'), "Multicast"),
        BlockingIpRange(ipaddress.IPv4Network('240.0.0.0/4'), "Reserved for future use"),
        BlockingIpRange(ipaddress.IPv4Network('255.255.255.255/32'), "Broadcast")
    ]
    return ranges


def load_custom_blocking_ips(file_path: str) -> List[str]:
    """
    Loads user-defined specific blocking IPv4 addresses from a file.
    Each IP address should be on a new line. Invalid IPs are ignored.
    """
    custom_ips = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                ip_str = line.strip()
                if ip_str and is_valid_ipv4(ip_str):
                    custom_ips.append(ip_str)
    except FileNotFoundError:
        print(f"Warning: Custom blocking IPs file not found at '{file_path}'. No custom IPs loaded.")
    except Exception as e:
        print(f"Error loading custom blocking IPs from '{file_path}': {e}")
    return custom_ips

