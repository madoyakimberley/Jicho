import requests
import xml.etree.ElementTree as ET
import re
from html import unescape

class KenyaLawScraper:
    def __init__(self):
        self.stream_url = "https://news.google.com/rss/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        self.sub_locations = [
            "kilimani", "lang'ata", "langata", "kasarani", "westlands", "kibera", "makadara",
            "githurai", "ruiru", "thika", "embakasi", "shanzu", "nyali", "likoni", "molo",
            "kondele", "milimani", "naivasha", "uasin gishu", "dandora", "kisauni", "ruai"
        ]

    def clean_text(self, html_text):
        """Strips HTML tags from feed items."""
        clean = re.sub(r'<[^>]+>', '', html_text)
        return unescape(clean)

    def parse_granular_details(self, text):
        """Extracts urban sectors and identifies actors/suspects/proper nouns."""
        text_lower = text.lower()
        detected_sub = "UNSPECIFIED SUB-ZONE"
        for sub in self.sub_locations:
            if sub in text_lower:
                detected_sub = sub.upper()
                break
                
        words = text.split()
        suspect_names = []
        for i in range(1, len(words) - 1):
            if words[i] and words[i+1] and words[i][0].isupper() and words[i+1][0].isupper():
                name1 = re.sub(r'[^\w\s]', '', words[i])
                name2 = re.sub(r'[^\w\s]', '', words[i+1])
                if name1.lower() not in ['kenya', 'court', 'police', 'dci', 'nairobi', 'state', 'suspect', 'missing', 'law', 'bill', 'gazette']:
                    suspect_names.append(f"{name1} {name2}")
                    
        detected_actor = suspect_names[0] if suspect_names else "SEE FULL BULLETINS"
        return detected_sub, detected_actor

    def fetch_stream(self, custom_query, limit=5):
        """Core telemetry gatherer for live streams."""
        found_records = []
        params = {
            "q": custom_query,
            "hl": "en-KE",
            "gl": "KE",
            "ceid": "KE:en"
        }
        
        try:
            response = requests.get(self.stream_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            counties_regex = r'\b(nairobi|kiambu|mombasa|nakuru|kisumu|machakos|meru|eldoret|nyeri|kakamega|garissa|kwale|kisii|kilifi|turkana)\b'
            
            for item in items[:limit]:
                raw_title = item.find('title').text if item.find('title') is not None else ""
                source_name = item.find('source').text if item.find('source') is not None else "Media Wire"
                
                raw_pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                pub_date = re.sub(r'^[A-Za-z]{3},\s*', '', raw_pub_date).replace(' :00 GMT', '').strip()
                pub_date = ' '.join(pub_date.split()[:3]) + " " + ':'.join(pub_date.split()[3].split(':')[:2]) if raw_pub_date else "LIVE"
                
                title_clean = raw_title.split(" - ")[0]
                title_clean = self.clean_text(title_clean)
                
                county_match = re.search(counties_regex, title_clean.lower())
                detected_county = county_match.group(0).capitalize() if county_match else "National Ledger"
                specific_loc, actors = self.parse_granular_details(title_clean)
                
                found_records.append({
                    "title": title_clean,
                    "county": detected_county,
                    "specific_location": specific_loc,
                    "actors": actors,
                    "source": f"{source_name} | {pub_date}"
                })
        except Exception:
            pass
            
        return found_records

    def fetch_cases_by_query(self, user_query):
        return self.fetch_stream(f"{user_query} Kenya", limit=8)

    def fetch_missing_persons(self):
        return self.fetch_stream('"missing child" OR "missing person" OR "disappeared" Kenya', limit=4)

    def fetch_preventive_actions(self):
        return self.fetch_stream('"police foiled" OR "rescued" OR "arrested before" OR "prevented" Kenya', limit=4)

    def fetch_law_updates(self):
        return self.fetch_stream('"gazette notice" OR "new law passed" OR "signed into law" impact Kenya', limit=4)