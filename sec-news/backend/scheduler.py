import time
import logging
from spiders.security_news import SecurityNewsSpider
from spiders.cve_spider import CVESpider
from models.database import Database

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
db = Database()

def save(batch, table):
    conn = db.get_connection()
    if table == "news":
        for item in batch:
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
    else:
        for cve in batch:
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

if __name__ == "__main__":
    news_spider = SecurityNewsSpider()
    cve_spider = CVESpider()
    while True:
        try:
            save(news_spider.fetch_all_news(), "news")
            save(cve_spider.fetch_recent_cves(), "cve")
        except Exception as e:
            logging.exception(e)
        time.sleep(60 * 20)