async def run_analysis(args: ParsedArguments):
"""
Main orchestration function that sets up, executes, analyzes, and reports DNS queries.
"""
print("DNS Analyzer: Starting analysis...")

# 1. Load configurations
blocking_ip_ranges = load_blocking_ip_ranges()
custom_blocking_ips = []
if args.custom_blocking_ips_path:
    custom_blocking_ips = load_custom_blocking_ips(args.custom_blocking_ips_path)

# Initial domains from requirements (will be expanded by load_domains)
initial_domains_from_req = [
    {"name": "rutube", "category": "Useful"}, # Original prompt did not include .ru
    {"name": "vkvideo", "category": "Useful"}, # Original prompt did not include .ru
    {"name": "photosight", "category": "Questionable"}, # Original prompt did not include .ru
    {"name": "rutracker.org", "category": "Questionable"},
    {"name": "pinterest", "category": "Questionable"}, # Original prompt did not include .com
    {"name": "безопасный поиск гугл", "category": "Useful"}, # To be handled by domain_loader (mapping to google.com/safesearch)
    {"name": "безопасный поиск яндекс", "category": "Useful"}, # To be handled by domain_loader (mapping to yandex.ru/safesearch)
    {"name": "безопасный поиск ютуб", "category": "Useful"}, # To be handled by domain_loader (mapping to youtube.com/safesearch)
    {"name": "xxx.com", "category": "Useless"},
    {"name": "порнхаб", "category": "Useless"}, # To be handled by domain_loader (mapping to pornhub.com)
    {"name": "tiktok", "category": "Useless"}, # Original prompt did not include .com
    # Additional domains from context are already present in load_domains' explicit_domains
]

domain_configs: List[DomainConfig] = load_domains(
    initial_domains_raw=initial_domains_from_req,
    additional_domains_path=args.domain_list_path,
    target_count=100
)
if not domain_configs:
    print("Error: No domains loaded for analysis. Exiting.")
    return

resolver_configs: List[DnsResolver] = load_resolvers(args.resolver_list_path)
if not resolver_configs:
    print("Error: No resolvers loaded for analysis. Exiting.")
    return

print(f"Loaded {len(domain_configs)} domains and {len(resolver_configs)} resolvers.")

# 2. Initialize client and store
doh_client = DohClient()
query_store = QueryStore()
semaphore = asyncio.Semaphore(args.concurrency_limit)

# 3. Prepare and execute queries
print("Executing DNS queries. This may take a while...")
query_tasks = []
for domain_cfg in domain_configs:
    for resolver_cfg in resolver_configs:
        query_tasks.append(
            doh_client.query(
                domain_name=domain_cfg.name,
                resolver=resolver_cfg,
                timeout_seconds=args.timeout_seconds,
                semaphore=semaphore,
                domain_category=domain_cfg.category
            )
        )

start_query_time = time.perf_counter()
raw_query_results: List[QueryResult] = await asyncio.gather(*query_tasks)
await doh_client.close()
end_query_time = time.perf_counter()
print(f"All {len(raw_query_results)} queries completed in {end_query_time - start_query_time:.2f} seconds.")

# 4. Process results and store
print("Analyzing query results for blocking behavior...")
for raw_result in raw_query_results:
    final_result = detect_blocking(raw_result, blocking_ip_ranges, custom_blocking_ips)
    query_store.add_result(final_result)

# 5. Calculate aggregated statistics
print("Calculating statistics...")
performance_stats_by_resolver: Dict[str, PerformanceStats] = {}
blocking_stats_by_resolver: Dict[str, BlockingStats] = {}
categorized_blocking_stats_by_resolver: Dict[str, List[CategorizedBlockingStats]] = {}
blocked_useful_domains_by_resolver: Dict[str, List[str]] = {}
blocked_useless_domains_by_resolver: Dict[str, List[str]] = {}
passed_useless_domains_by_resolver: Dict[str, List[str]] = {}

for resolver_cfg in resolver_configs: # Iterate over original resolver configs to ensure all are processed
    resolver_url = resolver_cfg.url
    resolver_results = query_store.get_results(resolver_url=resolver_url)

    performance_stats_by_resolver[resolver_url] = calculate_performance_stats(resolver_results)
    blocking_stats_by_resolver[resolver_url] = calculate_overall_blocking_percentage(resolver_results) # Includes error counts and error rate
    categorized_blocking_stats_by_resolver[resolver_url] = calculate_categorized_blocking_percentages(resolver_results, ALL_DOMAIN_CATEGORIES)
    blocked_useful_domains_by_resolver[resolver_url] = get_blocked_useful_domains(resolver_results)
    blocked_useless_domains_by_resolver[resolver_url] = get_blocked_useless_domains(resolver_results)
    passed_useless_domains_by_resolver[resolver_url] = get_passed_useless_domains(resolver_results)

# 6. Generate Excel report
full_resolvers_for_excel = [r for r in resolver_configs if r.url in query_store.get_all_resolvers()]

excel_generator = ExcelGenerator(
    output_filepath=args.output_file,
    all_domains=domain_configs, # Use the original full list of domains
    all_resolvers=full_resolvers_for_excel,
    query_store=query_store
)
excel_generator.generate_report(
    performance_stats_by_resolver=performance_stats_by_resolver,
    blocking_stats_by_resolver=blocking_stats_by_resolver,
    categorized_blocking_stats_by_resolver=categorized_blocking_stats_by_resolver,
    blocked_useful_domains_by_resolver=blocked_useful_domains_by_resolver,
    blocked_useless_domains_by_resolver=blocked_useless_domains_by_resolver,
    passed_useless_domains_by_resolver=passed_useless_domains_by_resolver
)

print("DNS Analyzer: Analysis complete.")
if name == "main":
# Ensure event loop is always closed cleanly
try:
args = parse_arguments()
asyncio.run(run_analysis(args))
except KeyboardInterrupt:
print("\nAnalysis interrupted by user.")
except Exception as e:
print(f"An unexpected error occurred: {e}")
import traceback
traceback.print_exc() # For debugging