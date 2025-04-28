import requests
import json
import random
from bs4 import BeautifulSoup
from utils.google_drive_uploader import upload_file_to_drive
from utils.luhn_generator import generate_full_card
import os

BIN_SOURCES = [
    "https://freebinchecker.com/",
    "https://bins.su/",
    "https://binssrc.com/",
    "https://bincheck.io/",
    "https://allbins.info/",
    "https://mybinsearch.com/",
    "https://binssite.com/"
]

def fetch_bins():
    bins = set()
    for url in BIN_SOURCES:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text()
            for word in text.split():
                if word.isdigit() and len(word) == 6:
                    bins.add(word)
        except Exception as e:
            print(f"[Warning] Error fetching BINs from {url}: {e}")
    return list(bins)

def enrich_bins(bin_list):
    enriched = []
    for bin_code in bin_list:
        try:
            res = requests.get(f"https://lookup.binlist.net/{bin_code}", timeout=5)
            if res.status_code == 200:
                data = res.json()
                enriched.append({
                    "bin": bin_code,
                    "bank": data.get('bank', {}).get('name', 'Unknown'),
                    "country": data.get('country', {}).get('name', 'Unknown'),
                    "type": data.get('type', 'Unknown'),
                    "full_card": generate_full_card(bin_code)
                })
        except Exception as e:
            print(f"[Warning] BIN {bin_code} enrich error: {e}")
    return enriched

def save_to_local(bins):
    os.makedirs("static", exist_ok=True)
    with open('static/bins_real_full.json', 'w', encoding='utf-8') as f:
        json.dump(bins, f, indent=2, ensure_ascii=False)

def auto_crawl_and_upload():
    print("[Crawler] Fetching BINs...")
    bins = fetch_bins()
    print(f"[Crawler] Found {len(bins)} BINs. Enriching...")
    enriched = enrich_bins(bins)
    print(f"[Crawler] Enriched {len(enriched)} BINs. Saving...")
    save_to_local(enriched)
    print("[Uploader] Uploading to Google Drive...")
    upload_file_to_drive('static/bins_real_full.json', 'HopeHubData/BIN/')
    print("[Success] BIN crawler cycle complete.")
