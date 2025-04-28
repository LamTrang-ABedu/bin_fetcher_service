from flask import Flask, jsonify
from crawler_bin import auto_crawl_and_upload

app = Flask(__name__)

@app.route('/')
def index():
    return 'HopeHub BIN Crawler is running!'

@app.route('/api/force-crawl-bin')
def force_crawl_bin():
    auto_crawl_and_upload()
    return jsonify({"status": "success", "message": "Manual crawl triggered."})

if __name__ == "__main__":
    from threading import Thread
    import time

    def scheduler():
        while True:
            auto_crawl_and_upload()
            time.sleep(4 * 3600)  # mỗi 4 giờ tự crawl lại

    Thread(target=scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)