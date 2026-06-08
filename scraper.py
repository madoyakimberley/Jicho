import requests
import xml.etree.ElementTree as ET
import re
from html import unescape

class KenyaLawScraper:
    def __init__(self):
        # Pointing to the live global record stream configured specifically for Kenyan geocodes
        self.stream_url = "https://news.google.com/rss/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Micro-locations across key Kenyan urban centers
        self.sub_locations = [
            "kilimani", "lang'ata", "langata", "kasarani", "westlands", "kibera", "makadara",
            "githurai", "ruiru", "thika", "embakasi", "shanzu", "nyali", "likoni", "molo",
            "kondele", "milimani", "naivasha", "uasin gishu", "dandora", "kisauni", "ruai"
        ]

    def clean_text(self, html_text):
        """Strips HTML artifacts from live feeds."""
        clean = re.sub(r'<[^>]+>', '', html_text)
        return unescape(clean)

    def parse_granular_details(self, text):
        """Scans live headlines for precise micro-locations and proper nouns (suspects)."""
        text_lower = text.lower()
        
        # 1. Look for precise neighborhood/estate markers
        detected_sub = "UNSPECIFIED SUB-ZONE"
        for sub in self.sub_locations:
            if sub in text_lower:
                detected_sub = sub.upper()
                break
                
        # 2. Extract prominent figures or suspects mentioned in the headline
        words = text.split()
        suspect_names = []
        
        for i in range(1, len(words) - 1):
            # Ensure words exist and have content before checking capitalization
            if words[i] and words[i+1] and words[i][0].isupper() and words[i+1][0].isupper():
                # Clean up punctuation trailing or leading the names (like quotes or commas)
                name1 = re.sub(r'[^\w\s]', '', words[i])
                name2 = re.sub(r'[^\w\s]', '', words[i+1])
                
                # Filter out heavy system/context keywords to avoid false positives
                if name1.lower() not in ['kenya', 'court', 'police', 'dci', 'nairobi', 'state', 'suspect']:
                    suspect_names.append(f"{name1} {name2}")
                    
        detected_actor = suspect_names[0] if suspect_names else "SEE FULL BULLETINS"
        return detected_sub, detected_actor

    def fetch_cases_by_query(self, user_query):
        """Fetches active breaking bulletins from the live wire."""
        found_incidents = []
        print(f"\n[JICHO LIVE SEARCH] Scanning active live streams for: '{user_query}'...")
        
        # Target the query directly to Kenyan security/legal contexts
        params = {
            "q": f"{user_query} Kenya",
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
            
            for item in items[:8]:  # Evaluate the latest 8 breaking records
                raw_title = item.find('title').text if item.find('title') is not None else ""
                source_name = item.find('source').text if item.find('source') is not None else "Media Wire"
                
                # FIXED: Extract and clean up the live publication date string from the item block
                raw_pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                # Cleans 'Mon, 08 Jun 2026 12:30:00 GMT' into a punchier '08 Jun 12:30' format
                pub_date = re.sub(r'^[A-Za-z]{3},\s*', '', raw_pub_date).replace(' :00 GMT', '').strip()
                pub_date = ' '.join(pub_date.split()[:3]) + " " + ':'.join(pub_date.split()[3].split(':')[:2]) if raw_pub_date else "LIVE"
                
                # Split off the trailing publisher tag (e.g., " - Citizen Digital")
                title_clean = raw_title.split(" - ")[0]
                title_clean = self.clean_text(title_clean)
                
                # Extract locations and suspects from the live headline string
                county_match = re.search(counties_regex, title_clean.lower())
                detected_county = county_match.group(0).capitalize() if county_match else "National Ledger"
                
                specific_loc, suspect_details = self.parse_granular_details(title_clean)
                
                found_incidents.append({
                    "target_query": user_query.upper(),
                    "title": title_clean,
                    "county": detected_county,
                    "specific_location": specific_loc,
                    "suspect_details": suspect_details,
                    "source": f"{source_name} | {pub_date}"
                })
                
        except Exception as e:
            print(f"[!] Live Feed Intake Failure: {e}")
            
        # Absolute structural truth: if the wire is clear, return nothing. No fake fallbacks.
        return found_incidents