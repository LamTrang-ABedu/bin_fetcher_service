from flask import Flask, render_template, request, jsonify
import json
import os
from utils.bin_fetcher import generate_bin_cache

app = Flask(__name__)

@app.route('/binlist')
def binlist_page():
    return render_template('binlist_view.html')

@app.route('/api/binlist')
def api_binlist():
    try:
        with open('static/cache/bins_cache.json', 'r', encoding='utf-8') as f:
            bins = json.load(f)
        return jsonify({'status': 'ok', 'bins': bins})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/refresh-bin')
def api_refresh_bin():
    try:
        generate_bin_cache()
        return jsonify({'status': 'ok', 'message': 'BIN cache refreshed successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)