import pandas as pd
import datetime
import os
import time
from scraper import KenyaLawScraper

class UI:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    DIM = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'

class HumanitarianDashboard:
    def __init__(self, scraper_instance):
        self.scraper = scraper_instance
        # SMART PROXIMITY TRIPWIRE CONFIGURATION
        self.WATCH_COUNTY = "Nairobi"
        self.WATCH_SUB_LOC = "LANGATA"
        
        # Actionable Routing Data
        self.HOTLINES = f"{UI.BOLD}📞 Childline Kenya: 116 | DCI Toll-Free: 0800 722 203{UI.RESET}"

    def process_proximity_tripwire(self, item):
        """Checks if a critical incident or alert occurs close to the local zone."""
        county = item.get('county', '')
        sub_loc = item.get('specific_location', '')
        
        county_match = county.strip().lower() == self.WATCH_COUNTY.lower()
        sub_loc_match = self.WATCH_SUB_LOC.lower() in sub_loc.lower()
        
        if county_match or sub_loc_match:
            return f"{UI.RED}{UI.BOLD}[ PROXIMITY ALERT — {self.WATCH_SUB_LOC.upper()} ]{UI.RESET} "
        return ""

    def verify_trust_level(self, source_string):
        """Assigns a trust badge based on known, verified reporting entities."""
        trusted_outlets = ['citizen', 'nation', 'standard', 'star', 'kbc', 'dci', 'police']
        source_lower = source_string.lower()
        
        if any(outlet in source_lower for outlet in trusted_outlets):
            return f"{UI.BLUE}{UI.BOLD}[VERIFIED SOURCE]{UI.RESET}"
        return f"{UI.DIM}[UNVERIFIED/PENDING]{UI.RESET}"

    def fetch_local_reports(self):
        """Reads the locally logged incident CSV to display on the dashboard."""
        filename = "local_reports.csv"
        if not os.path.isfile(filename):
            return []
        try:
            # Read the CSV and replace any empty values with blank strings
            df = pd.read_csv(filename).fillna("")
            if df.empty:
                return []
            # Return the 5 most recent records
            return df.tail(5).to_dict('records')
        except Exception:
            return []

    def display_view(self):
        """Gathers intelligence streams and outputs the multi-panel humanitarian console."""
        print(f"\n{UI.DIM}[ synchronizing humanitarian channels / inasawazisha njia za kibinadamu... ]{UI.RESET}")
        
        missing_data = self.scraper.fetch_missing_persons()
        preventive_data = self.scraper.fetch_preventive_actions()
        law_data = self.scraper.fetch_law_updates()
        local_data = self.fetch_local_reports()
        
        print(f"\n{UI.BOLD}{UI.CYAN}================================================================================{UI.RESET}")
        print(f"{UI.BOLD}{UI.CYAN}            JICHO COMMUNITY SAFETY DASHBOARD | USALAMA WA JAMII                 {UI.RESET}")
        print(f"{UI.BOLD}{UI.CYAN}================================================================================{UI.RESET}")

        # PANEL 1: MISSING CHILDREN & AMBER ALERTS
        print(f"\n{UI.YELLOW}{UI.BOLD}➔ PANEL I: ACTIVE AMBER ALERTS (WATU WALIOKOSA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if missing_data:
            print(f"  {UI.DIM}If you have a visual match, immediately contact authorities below:{UI.RESET}")
            print(f"  {self.HOTLINES}\n")
            for item in missing_data:
                alert = self.process_proximity_tripwire(item)
                trust_badge = self.verify_trust_level(item.get('source', ''))
                print(f"  {UI.YELLOW}⚡{UI.RESET} {alert}{item.get('title', 'Unknown Title')}")
                print(f"     {UI.DIM}Sector: {UI.CYAN}{item.get('specific_location', 'Unknown')}{UI.DIM} | Status: {trust_badge} | Log: {item.get('source', 'Unknown')}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No trace records or missing reports logged in the current window.{UI.RESET}\n")

        # PANEL 2: POSITIVE & PREVENTIVE SAFETY ANGLING
        print(f"\n{UI.GREEN}{UI.BOLD}➔ PANEL II: PREVENTIVE ACTIONS & SUCCESSES (HATUA ZA KUZUIA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if preventive_data:
            for item in preventive_data:
                alert = self.process_proximity_tripwire(item)
                trust_badge = self.verify_trust_level(item.get('source', ''))
                print(f"  {UI.GREEN}✓{UI.RESET} {alert}{item.get('title', 'Unknown Title')}")
                print(f"     {UI.DIM}Jurisdiction: {UI.CYAN}{item.get('county', 'Unknown')}{UI.DIM} | Actors: {UI.GREEN}{item.get('actors', 'Unknown')}{UI.DIM} | Status: {trust_badge}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No proactive preventions verified in current stream window.{UI.RESET}\n")

        # PANEL 3: LEGISLATIVE TRACKER & CITIZEN EFFECTS
        print(f"\n{UI.MAGENTA}{UI.BOLD}➔ PANEL III: CIVIC IMPACT & LAW TRACKER (SHERIA MPYA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if law_data:
            for item in law_data:
                trust_badge = self.verify_trust_level(item.get('source', ''))
                print(f"  {UI.MAGENTA}⚖{UI.RESET} {UI.BOLD}{item.get('title', 'Unknown Title')}{UI.RESET}")
                print(f"     {UI.DIM}Verification: {trust_badge}{UI.DIM} | Source: {item.get('source', 'Unknown')}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No structural legislative updates detected on immediate wires.{UI.RESET}\n")

        # PANEL 4: NEW LOCAL REPORTS
        print(f"\n{UI.BLUE}{UI.BOLD}➔ PANEL IV: CITIZEN LOGGED INCIDENTS (RIPOTI ZA MTAA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if local_data:
            for item in local_data:
                # Structure dictionary to reuse the proximity tripwire
                check_item = {'county': item.get('county', ''), 'specific_location': item.get('location', '')}
                alert = self.process_proximity_tripwire(check_item)
                
                print(f"  {UI.BLUE}📝{UI.RESET} {alert}{UI.BOLD}{item.get('type', '').upper()}{UI.RESET} - {item.get('details', '')}")
                print(f"     {UI.DIM}Sector: {UI.CYAN}{item.get('location', '')} ({item.get('county', '')}){UI.DIM} | Logged: {item.get('timestamp', '')}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No local citizen reports logged on disk.{UI.RESET}\n")

        print(f"{UI.CYAN}================================================================================{UI.RESET}")
        print(f"{UI.DIM}To report a sighting or log a local incident, type 'report' in the main menu.{UI.RESET}")
        print(f"{UI.CYAN}================================================================================{UI.RESET}\n")


class JichoTerminal:
    def __init__(self):
        print(f"\n{UI.GREEN}[0.002s] BOOT_SEQUENCE_INITIATED...{UI.RESET}")
        time.sleep(0.3)
        print(f"{UI.GREEN}[0.412s] LOADING JICHO_LIBS & UV ENVIRONMENT...{UI.RESET}")
        
        self.scraper = KenyaLawScraper()
        self.dashboard = HumanitarianDashboard(self.scraper)
        
        time.sleep(0.3)
        print(f"{UI.GREEN}[0.890s] ENVIRONMENT READY.{UI.RESET}\n")
        print(f"{UI.GREEN}{UI.BOLD}Python 3.12 (uv) [JICHO_OS v2.0]{UI.RESET}")
        print("Commands: type a crime (e.g. 'Femicide'), 'dashboard', 'report', or 'exit'\n")

    def log_manual_incident(self):
        """Step-by-step wizard to log local incidents offline."""
        print(f"\n{UI.YELLOW}{UI.BOLD}[ INITIATING MANUAL INCIDENT LOG ]{UI.RESET}")
        print(f"{UI.DIM}Enter details below. Press Enter to skip optional fields.{UI.RESET}\n")
        
        incident_type = input(f" {UI.CYAN}Incident Type{UI.DIM} (e.g., Missing Person, Theft, Suspicious Activity): {UI.RESET}").strip()
        
        if not incident_type:
            print(f"\n{UI.RED}[ ABORTED ] Incident type is required.{UI.RESET}")
            return
            
        county = input(f" {UI.CYAN}County{UI.DIM}: {UI.RESET}").strip()
        location = input(f" {UI.CYAN}Specific Location / Sub-county{UI.DIM}: {UI.RESET}").strip()
        details = input(f" {UI.CYAN}Description / Actors{UI.DIM}: {UI.RESET}").strip()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = "local_reports.csv"
        file_exists = os.path.isfile(filename)
        
        # Append to a local CSV file
        with open(filename, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("timestamp,type,county,location,details\n")
            # Basic sanitization to prevent CSV breaking from commas in input
            details_safe = details.replace(",", ";")
            f.write(f"{timestamp},{incident_type},{county},{location},{details_safe}\n")
            
        print(f"\n{UI.GREEN}✓ [ SECURE ] Incident permanently logged locally to {filename}.{UI.RESET}")

    def generate_disk_report(self, df, query_term):
        if df.empty: return
        filename = "jicho_observations.md"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a") as f:
            if not file_exists:
                f.write("# JICHO SYSTEM OBSERVATION FILE\n\n")
            f.write(f"\n## Target: {query_term.upper()} — {timestamp}\n")
            report_columns = ['county', 'specific_location', 'actors', 'title', 'source']
            f.write(df[report_columns].to_markdown(index=False))
            f.write("\n\n" + "-"*60 + "\n")

    def execute_investigation(self, query_term):
        """Standard single-target deep dive."""
        print(f"\n{UI.CYAN}>>> monitor.execute_scan(target='{query_term.upper()}'){UI.RESET}")
        raw_data = self.scraper.fetch_cases_by_query(query_term)
        
        if not raw_data:
            print(f"{UI.RED}[ ERROR ] No records extracted.{UI.RESET}")
            return
            
        df = pd.DataFrame(raw_data)
        
        print(f"\n{UI.DIM}" + "="*70 + f"{UI.RESET}")
        print(f"{UI.BOLD} JICHO TRUTH ANALYSIS FOR: '{query_term.upper()}'{UI.RESET}")
        print(f"{UI.DIM}" + "="*70 + f"{UI.RESET}")
        
        print(f"\n{UI.DIM}[LIVE STREAM DETECTED ACTORS & MICRO-LOCATIONS]{UI.RESET}")
        for idx, row in df.iterrows():
            loc = row.get('specific_location', 'UNSPECIFIED SUB-ZONE')
            actor = row.get('actors', 'SEE FULL BULLETINS')
            source = row.get('source', 'Media Wire')
            
            proximity_warning = self.dashboard.process_proximity_tripwire(row)
            
            print(f" {UI.GREEN}↳{UI.RESET} {proximity_warning}{UI.DIM}{source}{UI.RESET} | Actor: {UI.RED}{actor}{UI.RESET} | Loc: {UI.CYAN}{loc}{UI.RESET}")
            
        print(f"{UI.DIM}" + "="*70 + f"{UI.RESET}\n")
        self.generate_disk_report(df, query_term)

    def interactive_loop(self):
        while True:
            try:
                print(f"\n{UI.GREEN}jicho > {UI.RESET}", end="")
                user_input = input().strip()
                
                if user_input.lower() == 'exit':
                    print(f"\n{UI.DIM}[0.002s] SHUTTING DOWN JICHO_LIBS...{UI.RESET}")
                    print(f"{UI.DIM}[0.412s] JICHO OFFLINE. SYSTEM SAFE.{UI.RESET}")
                    break
                elif user_input.lower() == 'dashboard':
                    self.dashboard.display_view()
                elif user_input.lower() == 'report':
                    self.log_manual_incident()
                elif not user_input:
                    continue
                else:
                    self.execute_investigation(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n{UI.RED}[ JICHO INTERRUPT ]{UI.RESET} Shutting down system loops safely.")
                break

if __name__ == "__main__":
    engine = JichoTerminal()
    engine.interactive_loop()