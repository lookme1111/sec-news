from datetime import datetime
from bs4 import BeautifulSoup
from .base_spider import BaseSpider


class SecurityNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.sources = [
            {'name': '安全客', 'url': 'https://www.anquanke.com/', 'type': 'news'},
            {'name': 'FreeBuf', 'url': 'https://www.freebuf.com/', 'type': 'news'},
            {'name': 'Qualys', 'url': 'https://blog.qualys.com/', 'type': 'blog'}
        ]

    def fetch_all_news(self):
        all_articles = []
        for source in self.sources:
            try:
                self.logger.info(f"开始抓取 {source['name']}")
                html = self.fetch_html(source['url'])
                if html:
                    articles = self.parse_articles(html, source)
                    all_articles.extend(articles)
                    self.logger.info(f"{source['name']} 抓取到 {len(articles)} 篇文章")
            except Exception as e:
                self.logger.error(f"抓取 {source['name']} 失败: {e}")
        return all_articles

    def parse_articles(self, html, source):
        soup = BeautifulSoup(html, 'html.parser')
        articles = []

        if source['name'] == '安全客':
            items = soup.select('.title > a')[:10]
            for item in items:
                articles.append({
                    'title': item.get_text().strip(),
                    'url': 'https://www.anquanke.com' + item['href'],
                    'source': source['name'],
                    'publish_date': datetime.now(),
                    'category': '安全资讯'
                })

        elif source['name'] == 'FreeBuf':
            items = soup.select('.news-info h4 a')[:10]
            for item in items:
                articles.append({
                    'title': item.get_text().strip(),
                    'url': item['href'],
                    'source': source['name'],
                    'publish_date': datetime.now(),
                    'category': '安全资讯'
                })

        elif source['name'] == 'Qualys':
            items = soup.select('article h2 a')[:10]
            for item in items:
                articles.append({
                    'title': item.get_text().strip(),
                    'url': item['href'],
                    'source': source['name'],
                    'publish_date': datetime.now(),
                    'category': '博客'
                })

        return articles