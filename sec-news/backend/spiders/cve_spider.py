import json
from .base_spider import BaseSpider


class CVESpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.circl_url = 'https://cve.circl.lu/api/last'

    def fetch_recent_cves(self):
        all_cves = []
        try:
            response = self.session.get(self.circl_url, timeout=10)
            if response.status_code == 200:
                cves = response.json()
                for cve in cves[:15]:
                    all_cves.append(self.parse_circl_cve(cve))
        except Exception as e:
            self.logger.error(f"×¥È¡ CIRCL CVE Ê§°Ü: {e}")
        return all_cves

    def parse_circl_cve(self, cve_data):
        cvss = cve_data.get('cvss', 0) or 0
        return {
            'cve_id': cve_data.get('id', ''),
            'summary': (cve_data.get('summary', '') or '')[:500],
            'published_date': self.parse_datetime(cve_data.get('Published', '')),
            'cvss_score': float(cvss),
            'severity': self.get_severity(float(cvss)),
            'references': json.dumps(cve_data.get('references', [])),
            'affected_products': json.dumps(cve_data.get('vulnerable_configuration', []))
        }

    def get_severity(self, cvss_score):
        if cvss_score >= 9.0:
            return 'CRITICAL'
        if cvss_score >= 7.0:
            return 'HIGH'
        if cvss_score >= 4.0:
            return 'MEDIUM'
        return 'LOW'