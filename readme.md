# DNS Analyzer Script

## Project Overview

The DNS Analyzer script is a Python-based tool designed to evaluate the performance and blocking capabilities of various DNS over HTTPS (DoH) resolvers against a categorized list of domain names. The primary goal is to help users identify fast and balanced DNS resolvers that align with their desired level of content filtering.

It performs concurrent DoH queries, measures query latencies, and determines if domains are blocked based on criteria such as NXDOMAIN responses, resolution to non-routable IPs, or known blocking IPs. The results are compiled into a comprehensive Excel report, providing both a high-level overview and detailed per-resolver statistics, including:

*   **DNS Matrix:** A visual representation of which DNS resolver blocks which domain.
*   **Performance Statistics:** Minimum, maximum, median, and average query latencies for resolved domains.
*   **Error Rate:** Percentage of queries resulting in technical errors.
*   **Overall Blocking Statistics:** Percentage of domains blocked by each resolver.
*   **Categorized Blocking:** Blocking percentages for 'Useful', 'Questionable', and 'Useless' domain categories.
*   **Detailed Lists:** Specific lists of 'Useful' domains that were blocked, 'Useless' domains that were blocked, and 'Useless' domains that were allowed (resolved).

This tool empowers users to make informed decisions when selecting a DoH resolver, balancing speed with content filtering needs.

## Deployment Instructions

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Save the Script:** Save the provided Python code as `dns_analyzer_script.py` in your desired directory.

2.  **Create Configuration Files:**
    *   **`resolvers.txt` (Required):** Create a plain text file named `resolvers.txt` in the same directory as the script. Each line in this file should contain a valid DoH resolver URL.
        Example `resolvers.txt`:
        ```
        https://1.1.1.1/dns-query
        https://dns.google/dns-query
        https://cloudflare-dns.com/dns-query
        https://doh.opendns.com/dns-query
        https://dns.adguard.com/dns-query
        ```
    *   **`domains.txt` (Optional):** If you wish to provide additional domains beyond the built-in list, create a plain text file named `domains.txt`. Each line should contain one domain name.
        Example `domains.txt`:
        ```
        example.com
        testdomain.org
        anotherdomain.net
        ```
    *   **`custom_blocking_ips.txt` (Optional):** If you want to include specific IP addresses as blocking indicators, create a plain text file named `custom_blocking_ips.txt`. Each line should contain one IPv4 address.
        Example `custom_blocking_ips.txt`:
        ```
        1.2.3.4
        8.8.4.4
        ```

3.  **Install Dependencies:** Open your terminal or command prompt, navigate to the directory where you saved `dns_analyzer_script.py`, and run the following command to install the required Python packages:

    ```bash
    pip install httpx openpyxl
    ```

### Usage

Run the script from your terminal using Python.

```bash
python dns_analyzer_script.py --resolvers resolvers.txt [OPTIONS]
Command-Line Arguments
--resolvers <path/to/resolvers.txt> (Required): Path to the text file containing DoH resolver URLs.
--domains <path/to/domains.txt> (Optional): Path to a text file containing additional domain names (one per line). If not provided, a hardcoded list expanded to 100 domains is used.
--output <filename.xlsx> (Optional): Path for the output Excel report. Defaults to dns_analysis_report.xlsx.
--concurrency <number> (Optional): Maximum number of concurrent DoH queries. Defaults to 20.
--timeout <seconds> (Optional): Timeout in seconds for each individual DoH query. Defaults to 5.0 seconds.
--custom-blocking-ips <path/to/custom_blocking_ips.txt> (Optional): Path to a text file containing user-defined specific blocking IPv4 addresses (one per line).
Example Commands
Basic run with default settings (using resolvers.txt):

python dns_analyzer_script.py --resolvers resolvers.txt
Run with custom domain list and output file:

python dns_analyzer_script.py --resolvers resolvers.txt --domains my_domains.txt --output custom_report.xlsx
Run with increased concurrency and custom blocking IPs:

python dns_analyzer_script.py --resolvers resolvers.txt --concurrency 50 --custom-blocking-ips my_block_ips.txt
After execution, an Excel file (e.g., dns_analysis_report.xlsx) will be generated in the same directory, containing the comprehensive analysis.

system_objective_fulfilled