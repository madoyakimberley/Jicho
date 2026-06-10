import time

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
        county_match = item['county'].strip().lower() == self.WATCH_COUNTY.lower()
        sub_loc_match = self.WATCH_SUB_LOC.lower() in item['specific_location'].lower()
        
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

    def display_view(self):
        """Gathers intelligence streams and outputs the multi-panel humanitarian console."""
        print(f"\n{UI.DIM}[ synchronizing humanitarian channels / inasawazisha njia za kibinadamu... ]{UI.RESET}")
        
        missing_data = self.scraper.fetch_missing_persons()
        preventive_data = self.scraper.fetch_preventive_actions()
        law_data = self.scraper.fetch_law_updates()
        
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
                trust_badge = self.verify_trust_level(item['source'])
                print(f"  {UI.YELLOW}⚡{UI.RESET} {alert}{item['title']}")
                print(f"     {UI.DIM}Sector: {UI.CYAN}{item['specific_location']}{UI.DIM} | Status: {trust_badge} | Log: {item['source']}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No trace records or missing reports logged in the current window.{UI.RESET}\n")

        # PANEL 2: POSITIVE & PREVENTIVE SAFETY ANGLING
        print(f"\n{UI.GREEN}{UI.BOLD}➔ PANEL II: PREVENTIVE ACTIONS & SUCCESSES (HATUA ZA KUZUIA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if preventive_data:
            for item in preventive_data:
                alert = self.process_proximity_tripwire(item)
                trust_badge = self.verify_trust_level(item['source'])
                print(f"  {UI.GREEN}✓{UI.RESET} {alert}{item['title']}")
                print(f"     {UI.DIM}Jurisdiction: {UI.CYAN}{item['county']}{UI.DIM} | Actors: {UI.GREEN}{item['actors']}{UI.DIM} | Status: {trust_badge}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No proactive preventions verified in current stream window.{UI.RESET}\n")

        # PANEL 3: LEGISLATIVE TRACKER & CITIZEN EFFECTS
        print(f"\n{UI.MAGENTA}{UI.BOLD}➔ PANEL III: CIVIC IMPACT & LAW TRACKER (SHERIA MPYA){UI.RESET}")
        print(f"{UI.DIM}--------------------------------------------------------------------------------{UI.RESET}")
        if law_data:
            for item in law_data:
                trust_badge = self.verify_trust_level(item['source'])
                print(f"  {UI.MAGENTA}⚖{UI.RESET} {UI.BOLD}{item['title']}{UI.RESET}")
                print(f"     {UI.DIM}Verification: {trust_badge}{UI.DIM} | Source: {item['source']}{UI.RESET}\n")
        else:
            print(f"  {UI.DIM}No structural legislative updates detected on immediate wires.{UI.RESET}\n")

        print(f"{UI.CYAN}================================================================================{UI.RESET}")
        print(f"{UI.DIM}To report a sighting or log a local incident, type 'report' in the main menu.{UI.RESET}")
        print(f"{UI.CYAN}================================================================================{UI.RESET}\n")