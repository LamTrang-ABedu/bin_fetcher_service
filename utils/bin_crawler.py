import requests
import json
import random
import time
import threading
from bs4 import BeautifulSoup
from utils.cloudflare_r2 import upload_to_r2
from utils.luhn_generator import generate_full_card

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

def enrich_bin(bin_code):
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_code}", timeout=5)
        if res.ok:
            data = res.json()
            return {
                'bin': bin_code,
                'bank': data.get('bank', {}).get('name', 'Unknown'),
                'country': data.get('country', {}).get('name', 'Unknown'),
                'type': data.get('type', 'Unknown')
            }
    except:
        pass
    return None

def auto_crawl_and_upload():
    print("[Info] Start fetching BINs...")
    bin_list = fetch_bin_from_web()
    print(f"[Info] Fetched {len(bin_list)} BINs. Enriching...")
    enriched = []
    for bin_code in bin_list:
        info = enrich_bin(bin_code)
        if info:
            card = generate_full_card(bin_code)
            card.update(info)
            enriched.append(card)
    print(f"[Info] {len(enriched)} BINs enriched. Uploading to R2...")
    json_data = json.dumps(enriched, indent=2)
    upload_to_r2('bins_real_full.json', json_data)
    print("[Success] Upload complete!")

def start_scheduler():
    def scheduler():
        while True:
            auto_crawl_and_upload()
            time.sleep(4 * 3600)  # 4 giờ
    t = threading.Thread(target=scheduler)
    t.daemon = True
    t.start()