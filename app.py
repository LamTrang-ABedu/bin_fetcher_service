from utils.bin_crawler import start_scheduler
from flask import Flask, jsonify
from utils.cloudflare_r2 import list_bins_from_r2

app = Flask(__name__)

@app.route('/api/binlist', methods=['GET'])
def get_binlist():
    bins = list_bins_from_r2()
    return jsonify({'status': 'ok', 'bins': bins})

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=8000)
