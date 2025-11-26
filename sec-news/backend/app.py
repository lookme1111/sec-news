from flask import Flask, render_template, jsonify
from models.database import Database
from spiders.security_news import SecurityNewsSpider
from spiders.cve_spider import CVESpider

app = Flask(__name__)
db = Database()

@app.route("/")
def index():
    conn = db.get_connection()
    news = conn.execute(
        "SELECT * FROM security_news ORDER BY publish_date DESC LIMIT 30"
    ).fetchall()
    stats = {
        "news_count": conn.execute("SELECT COUNT(*) FROM security_news").fetchone()[0],
        "cve_count": conn.execute("SELECT COUNT(*) FROM cve_data").fetchone()[0],
    }
    cves = conn.execute(
        "SELECT * FROM cve_data ORDER BY cvss_score DESC, published_date DESC LIMIT 8"
    ).fetchall()
    conn.close()
    return render_template("index.html", news_list=news, stats=stats, recent_cves=cves)

@app.route("/cve")
def cve():
    conn = db.get_connection()
    rows = conn.execute(
        "SELECT * FROM cve_data ORDER BY published_date DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return render_template("cve.html", cve_list=rows)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/refresh", methods=["POST"])
def refresh():
    news = SecurityNewsSpider().fetch_all_news()
    cves = CVESpider().fetch_recent_cves()
    conn = db.get_connection()
    for item in news:
        conn.execute(
            """INSERT OR IGNORE INTO security_news
               (title,url,source,publish_date,content,category)
               VALUES (?,?,?,?,?,?)""",
            (
                item["title"],
                item["url"],
                item.get("source"),
                item.get("publish_date"),
                item.get("content"),
                item.get("category"),
            ),
        )
    for cve in cves:
        conn.execute(
            """INSERT OR IGNORE INTO cve_data
               (cve_id,summary,published_date,cvss_score,severity,references,affected_products)
               VALUES (?,?,?,?,?,?,?)""",
            (
                cve["cve_id"],
                cve["summary"],
                cve["published_date"],
                cve["cvss_score"],
                cve["severity"],
                cve["references"],
                cve["affected_products"],
            ),
        )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "news": len(news), "cves": len(cves)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)