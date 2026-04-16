import os
import html
from datetime import datetime, timedelta

# ClipPeaks SSG Builder (ESPN-Style / EN-First)
BASE_DIR = "/Volumes/KIOXIA/clippeaks/"
OUTPUT_DIR = os.path.join(BASE_DIR, "public")

def is_expired(date_str, is_top_10=False):
    if is_top_10: return False
    item_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    limit_date = datetime.now() - timedelta(days=14)
    return item_date < limit_date

def sanitize(text):
    return html.escape(str(text))

def generate_html(data_items):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClipPeaks - Broadcast Network</title>
    <style>
        body { background-color: #050505; color: #fff; font-family: 'Helvetica Neue', Impact, sans-serif; margin: 0; padding: 0; }
        .ticker-wrap { background-color: #CC0000; width: 100%; overflow: hidden; height: 55px; line-height: 55px; border-bottom: 3px solid #FFD700; }
        .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; animation: ticker 25s linear infinite; font-weight: 900; font-size: 1.8rem; letter-spacing: 2px; font-style: italic; color: #fff;}
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
        .article-card { background: #111; margin-bottom: 60px; display: flex; flex-direction: column; border-top: 6px solid #CC0000; padding: 25px;}
        .article-card.mega { padding: 40px; box-shadow: 0 20px 50px rgba(204,0,0,0.15); border: 2px solid #222; border-top: 8px solid #CC0000; }
        .headline-en { font-size: 4.5rem; font-weight: 900; color: #FFD700; margin: 0 0 5px 0; text-transform: uppercase; font-style: italic; line-height: 1; letter-spacing: -1px; }
        .headline-jp { font-size: 1.4rem; color: #aaa; margin: 0 0 25px 0; font-family: 'Arial', sans-serif; font-weight: bold; }
        .data-proof { font-size: 1.5rem; font-weight: 900; color: #000; background: #FFD700; padding: 10px 20px; display: inline-block; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 1px; }
        .embed-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin-bottom: 30px; border: 4px solid #333; }
        .embed-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
        .deep-dive { font-size: 1.3rem; line-height: 1.8; color: #eee; font-family: 'Arial', sans-serif; border-left: 5px solid #CC0000; padding-left: 20px; margin-top: 10px; }
        .deep-dive strong { font-size: 1.8rem; color: #FFD700; font-family: 'Helvetica Neue', sans-serif; font-style: italic; text-transform: uppercase; display: block; margin-bottom: 10px; }
        .scarcity { margin-top: 25px; padding: 15px; background: rgba(204,0,0,0.1); border: 1px dashed #CC0000; color: #CC0000; font-weight: bold; font-family: 'Arial', sans-serif; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="ticker-wrap"><div class="ticker">
"""
    ticker_texts = [f"BREAKING: {sanitize(item['title_en'])} - PEAK DENSITY: {sanitize(item['density'])}" for item in data_items]
    html_content += "&nbsp;&nbsp;&nbsp;&nbsp;⚠️&nbsp;&nbsp;&nbsp;&nbsp;".join(ticker_texts)
    
    html_content += """
    </div></div>
    <div class="container">
"""

    for idx, item in enumerate(data_items):
        is_mega = " mega" if idx == 0 else ""
        html_content += f"""
        <div class="article-card{is_mega}">
            <h1 class="headline-en">BREAKING: {sanitize(item['title_en'])}</h1>
            <h2 class="headline-jp">[{sanitize(item['title_jp'])}]</h2>
            <div><span class="data-proof">PEAK DENSITY: {sanitize(item['density'])} | MAX SC: {sanitize(item['max_sc'])}</span></div>
            
            <div class="embed-container">
                <iframe src="https://www.youtube.com/embed/{sanitize(item['video_id'])}" frameborder="0" allowfullscreen></iframe>
            </div>
            
            <div class="deep-dive">
                <strong>Deep Dive Analysis</strong>
                {sanitize(item['narrative_en'])}<br><br>
                <span style="color:#aaa; font-size: 1.05rem;">(JP Mirror: {sanitize(item['narrative_jp'])})</span>
            </div>
            
            <div class="scarcity">⚠️ This Exclusive Insight and Data will self-destruct in 14 days. Access the raw coordinates instantly via Notion Premium.</div>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
"""
    return html_content

def build_ssg():
    print("Initiating ClipPeaks SSG Builder (ESPN-Style)...")
    raw_data = [
        {
            "id": "uuid-001",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "title_en": "THE ULTIMATE HYPE OF NEW OUTFIT",
            "title_jp": "激動: 待望の新衣装で世界トレンド1位へ",
            "video_id": "dQw4w9WgXcQ",
            "density": "0.85",
            "max_sc": "$1,000 USD (150,000 JPY)",
            "narrative_en": "Massive vertical growth in concurrent viewers right from the start. The outfit change segment triggered the highest chat density of the week.",
            "narrative_jp": "開始直後から同接が垂直立ち上がり。中盤の衣装チェンジでチャット密度が今週の全配信中最大を記録。",
            "is_top_10": False
        },
        {
            "id": "uuid-002",
            "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S"),
            "title_en": "OUTLIER DETECTED: UNMEASURABLE MADNESS",
            "title_jp": "殿堂入り: 同接の限界を超えた伝説の一撃",
            "video_id": "yPyQpS5F_m8",
            "density": "UNMEASURABLE",
            "max_sc": "$10,000 USD (1,500,000 JPY)",
            "narrative_en": "System flagged an Outlier. Throw away the illusion of concurrent viewers; this is what true, concentrated fanaticism looks like.",
            "narrative_jp": "システムがOutlier(外れ値)を検知。同接数という幻想を捨てろ、これが真の熱狂だ。[年間TOP 10 聖域保護対象]",
            "is_top_10": True
        }
    ]

    valid_data = []
    for item in raw_data:
        if not is_expired(item["date"], item.get("is_top_10", False)):
            valid_data.append(item)
            print(f"PROTECTED: {item['title_en']}")
        else:
            print(f"PURGED: 14-day rule executed on '{item['title_en']}'.")

    html_output = generate_html(valid_data)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"BUILD COMPLETE: {out_path}")

if __name__ == "__main__":
    build_ssg()