import requests
import json
from bs4 import BeautifulSoup
import os

BIN_CACHE_FILE = 'static/cache/bins_cache.json'
BIN_SOURCE_URLS = [
    'https://www.freebinchecker.com/',
    'https://bins.su/',
    'https://www.bincodes.com/bin-list/',
    'https://binlist.net/',
    'https://namso-gen.com/',
    'https://ccbins.pro/',
    'https://www.binbase.com/',
    'https://bingen.pro/'
]

def fetch_bin_from_web():
    bins = set()
    for url in BIN_SOURCE_URLS:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                text = soup.get_text()
                bins.update(set(filter(lambda x: x.isdigit() and len(x) == 6, text.split())))
        except Exception as e:
            print(f"[Warning] Fetch failed from {url}: {e}")
    return list(bins)

def enrich_bin_info(bin_list):
    enriched_bins = []
    for bin_code in bin_list:
        try:
            res = requests.get(f'https://lookup.binlist.net/{bin_code}', timeout=5)
            if res.status_code == 200:
                data = res.json()
                enriched_bins.append({
                    'bin': bin_code,
                    'country': data.get('country', {}).get('name', 'Unknown'),
                    'bank': data.get('bank', {}).get('name', 'Unknown'),
                    'type': data.get('type', 'Unknown')
                })
        except Exception as e:
            print(f"[Warning] BIN {bin_code} enrich failed: {e}")
    return enriched_bins

def save_bins_cache(bins):
    os.makedirs(os.path.dirname(BIN_CACHE_FILE), exist_ok=True)
    with open(BIN_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(bins, f, indent=2, ensure_ascii=False)

def generate_bin_cache():
    print("[Info] Start fetching BINs...")
    bin_list = fetch_bin_from_web()
    print(f"[Info] Fetched {len(bin_list)} BINs. Enriching...")
    enriched = enrich_bin_info(bin_list)
    print(f"[Info] Enriched {len(enriched)} BINs. Saving cache...")
    save_bins_cache(enriched)
    print(f"[Success] BIN cache generated: {BIN_CACHE_FILE}")

if __name__ == "__main__":
    generate_bin_cache()