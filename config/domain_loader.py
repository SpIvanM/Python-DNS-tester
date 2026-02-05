from typing import List, Dict, Optional
from pathlib import Path
from data.models import DomainConfig, DomainCategory

def load_domains(initial_domains_raw: List[Dict[str, str]], additional_domains_path: Optional[str] = None, target_count: int = 100) -> List[DomainConfig]:
    """
    Loads and categorizes a list of 100 domain names, ensuring unique entries and categories.
    Expands with generic domains if target_count is not met.
    """
all_domains: Dict[str, DomainConfig] = {}

# 1. Process initial domains from the prompt context
explicit_domains = [
    ("rutube.ru", "Useful"),
    ("vkvideo.ru", "Useful"),
    ("photosight.ru", "Questionable"),
    ("rutracker.org", "Questionable"),
    ("pinterest.com", "Questionable"),
    ("google.com/safesearch", "Useful"), # Interpreted as relevant to safe search mechanisms
    ("yandex.ru/safesearch", "Useful"),
    ("youtube.com/safesearch", "Useful"),
    ("tiktok.com", "Useless"),
    ("xxx.com", "Useless"),
    ("pornhub.com", "Useless"),
    ("reddit.com", "Questionable"), # Borderline/time-waster
    ("tinder.com", "Useless"),     # Erotics/time-waster
    ("onlyfans.com", "Useless"),   # Erotics
]

for domain_name, category in explicit_domains:
    name_lower = domain_name.lower()
    all_domains[name_lower] = DomainConfig(name=name_lower, category=DomainCategory(category))

# Override with initial_domains_raw if provided for custom entries
for item in initial_domains_raw:
    name = item['name'].lower()
    category = item['category']
    all_domains[name] = DomainConfig(name=name, category=DomainCategory(category))

# 2. Add generic domains to fill up to target_count
generic_domains_pool = [
    # Borderline usefulness / decency, time-wasters
    ("instagram.com", "Useless"),
    ("facebook.com", "Useless"),
    ("twitter.com", "Useless"),
    ("discord.com", "Questionable"),
    ("tumblr.com", "Useless"),
    ("4chan.org", "Useless"),
    ("twitch.tv", "Questionable"),

    # Erotics (additional examples)
    ("chaturbate.com", "Useless"),
    ("stripchat.com", "Useless"),
    ("xhamster.com", "Useless"),
    ("redtube.com", "Useless"),
    ("xvideos.com", "Useless"),
    ("eroprofile.com", "Useless"),
    ("hentai.xxx", "Useless"),
    ("youporn.com", "Useless"),
    ("spankbang.com", "Useless"),
    ("manyvids.com", "Useless"),

    # Ad and analytics servers
    ("google-analytics.com", "Useless"),
    ("doubleclick.net", "Useless"),
    ("facebook.net", "Useless"),
    ("ad.doubleclick.net", "Useless"),
    ("ads.google.com", "Useless"),
    ("tracking.com", "Useless"),
    ("analytics.yandex.ru", "Useless"),
    ("mc.yandex.ru", "Useless"),
    ("vk.com/ads", "Useless"),
    ("googlesyndication.com", "Useless"),
    ("amazon-adsystem.com", "Useless"),
    ("adnxs.com", "Useless"),
    ("criteo.com", "Useless"),
    ("taboola.com", "Useless"),
    ("outbrain.com", "Useless"),
    ("quantserve.com", "Useless"),
    ("mixpanel.com", "Useless"),
    ("segment.com", "Useless"),
    ("hotjar.com", "Useless"),
    ("datadoghq.com", "Useless"),
    ("newrelic.com", "Useless"),
    ("sentry.io", "Useless"),
    ("bing.com/ads", "Useless"),
    ("yahoo.com/ads", "Useless"),
    ("msn.com/ads", "Useless"),

    # VPN services (useful for privacy/security)
    ("nordvpn.com", "Useful"),
    ("expressvpn.com", "Useful"),
    ("protonvpn.com", "Useful"),
    ("surfshark.com", "Useful"),
    ("privateinternetaccess.com", "Useful"),
    ("cyberghostvpn.com", "Useful"),
    ("purevpn.com", "Useful"),
    ("vyprvpn.com", "Useful"),
    ("ipvanish.com", "Useful"),
    ("torguard.net", "Useful"),

    # Other useful/common domains
    ("google.com", "Useful"),
    ("yandex.ru", "Useful"),
    ("youtube.com", "Useful"),
    ("wikipedia.org", "Useful"),
    ("github.com", "Useful"),
    ("stackoverflow.com", "Useful"),
    ("microsoft.com", "Useful"),
    ("apple.com", "Useful"),
    ("cloudflare.com", "Useful"),
    ("openai.com", "Useful"),
    ("amazon.com", "Useful"),
    ("ebay.com", "Useful"),
    ("aliexpress.com", "Useful"),
    ("telegram.org", "Useful"),
    ("signal.org", "Useful"),
    ("whatsapp.com", "Useful"),
    ("zoom.us", "Useful"),
    ("slack.com", "Useful"),
    ("getpocket.com", "Useful"),
    ("evernote.com", "Useful"),
    ("dropbox.com", "Useful"),
    ("onedrive.live.com", "Useful"),
    ("drive.google.com", "Useful"),
    ("translate.google.com", "Useful"),
    ("bing.com", "Useful"),
    ("duckduckgo.com", "Useful"),
    ("mozilla.org", "Useful"),
    ("brave.com", "Useful"),
    ("torproject.org", "Useful"),
    ("fsf.org", "Useful"),
    ("opensource.org", "Useful"),
]

for domain_name, category in generic_domains_pool:
    if len(all_domains) >= target_count:
        break
    name = domain_name.lower()
    if name not in all_domains:
        all_domains[name] = DomainConfig(name=name, category=DomainCategory(category))

# 3. Load additional domains from file if provided
if additional_domains_path:
    try:
        with open(additional_domains_path, 'r', encoding='utf-8') as f:
            for line in f:
                domain_name = line.strip().lower()
                if domain_name and domain_name not in all_domains:
                    # Assign default 'Questionable' category for file-loaded domains if not already specified
                    all_domains[domain_name] = DomainConfig(name=domain_name, category="Questionable")
                    if len(all_domains) >= target_count:
                        break
    except FileNotFoundError:
        print(f"Warning: Additional domains file not found at '{additional_domains_path}'. Skipping.")
    except Exception as e:
        print(f"Error loading additional domains from '{additional_domains_path}': {e}")

# 4. Ensure we have exactly target_count unique domains (or as close as possible)
final_domains: List[DomainConfig] = list(all_domains.values())

# Sort for consistent output if trimming is needed
final_domains.sort(key=lambda d: (d.category, d.name)) 

if len(final_domains) > target_count:
    final_domains = final_domains[:target_count]

return final_domains