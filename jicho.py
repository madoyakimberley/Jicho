import pandas as pd
import datetime
import os
import time
from scraper import KenyaLawScraper

# ---------------------------------------------------------
# ANSI COLOR PALETTE (Matches the mockup aesthetics)
# ---------------------------------------------------------
class UI:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    DIM = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class JichoTerminal:
    def __init__(self):
        # Simulated Boot Sequence mimicking the UI design
        print(f"\n{UI.GREEN}[0.002s] BOOT_SEQUENCE_INITIATED...{UI.RESET}")
        time.sleep(0.4)
        
        print(f"{UI.GREEN}[0.412s] LOADING JICHO_LIBS...{UI.RESET}")
        self.scraper = KenyaLawScraper()
        time.sleep(0.4)
        
        print(f"{UI.GREEN}[0.890s] ENVIRONMENT READY.{UI.RESET}\n")
        
        # System Info Header
        print(f"{UI.GREEN}{UI.BOLD}Python 3.12.0 (main) [JICHO_OS]{UI.RESET}")
        print("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.\n")
        
        print(f"{UI.DIM}[ INFO ] Daemon started at 0x7f882a1c{UI.RESET}")

    def generate_disk_report(self, df, query_term):
        if df.empty:
            return
            
        filename = "jicho_observations.md"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a") as f:
            if not file_exists:
                f.write("# JICHO SYSTEM OBSERVATION FILE\n*Objective data tracking independent of media narrative.*\n\n")
            
            f.write(f"\n## Search Target: {query_term.upper()} — Captured at {timestamp}\n")
            f.write(f"Total Records Extracted: {len(df)}\n\n")
            
            report_columns = ['target_query', 'county', 'specific_location', 'suspect_details', 'title', 'source']
            f.write(df[report_columns].to_markdown(index=False))
            f.write("\n\n" + "-"*60 + "\n")
            
        # Success message in Bright Green
        print(f"{UI.GREEN}[ SUCCESS ]{UI.RESET} Clean tracking logs appended to: {UI.CYAN}{filename}{UI.RESET}")

    def execute_investigation(self, query_term):
        # Info message in Cyan/Blue
        print(f"\n{UI.CYAN}>>> from jicho.core import monitor{UI.RESET}")
        print(f"{UI.CYAN}>>> monitor.execute_scan(target='{query_term.upper()}'){UI.RESET}")
        
        raw_data = self.scraper.fetch_cases_by_query(query_term)
        
        if not raw_data:
            # Error/Empty message in Red
            print(f"{UI.RED}[ ERROR ] No records extracted matching safety verifiers.{UI.RESET}")
            return
            
        df = pd.DataFrame(raw_data)
        county_distribution = df['county'].value_counts()
        
        # Dimmed framing for the data tables
        print(f"\n{UI.DIM}" + "="*70 + f"{UI.RESET}")
        print(f"{UI.BOLD} JICHO TRUTH ANALYSIS FOR: '{query_term.upper()}'{UI.RESET}")
        print(f"{UI.DIM}" + "="*70 + f"{UI.RESET}")
        
        print(f"\n{UI.DIM}[GEOGRAPHIC DISTRIBUTION RATIOS]{UI.RESET}")
        for county, count in county_distribution.items():
            print(f" {UI.GREEN}❖{UI.RESET} {county} County: {UI.CYAN}{count}{UI.RESET} verified occurrence(s)")
            
        print(f"\n{UI.DIM}[LIVE STREAM DETECTED ACTORS & MICRO-LOCATIONS]{UI.RESET}")
        for idx, row in df.iterrows():
            loc = row.get('specific_location', 'UNSPECIFIED SUB-ZONE')
            actor = row.get('suspect_details', 'SEE FULL BULLETINS')
            source = row.get('source', 'Media Wire')
            
            # Formatted list items
            print(f" {UI.GREEN}↳{UI.RESET} {UI.DIM}{source}{UI.RESET} | Actor: {UI.RED}{actor}{UI.RESET} | Loc: {UI.CYAN}{loc}{UI.RESET}")
            
        print(f"{UI.DIM}" + "="*70 + f"{UI.RESET}\n")
        
        self.generate_disk_report(df, query_term)

    def interactive_loop(self):
        while True:
            try:
                # Custom prompt styling: "jicho > " in green
                print(f"\n{UI.GREEN}jicho > {UI.RESET}", end="")
                user_input = input().strip()
                
                if user_input.lower() == 'exit':
                    print(f"\n{UI.DIM}[0.002s] SHUTTING DOWN JICHO_LIBS...{UI.RESET}")
                    print(f"{UI.DIM}[0.412s] JICHO OFFLINE. SYSTEM SAFE.{UI.RESET}")
                    break
                if not user_input:
                    continue
                    
                self.execute_investigation(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n{UI.RED}[ JICHO INTERRUPT ]{UI.RESET} Shutting down system loops safely.")
                break

if __name__ == "__main__":
    engine = JichoTerminal()
    engine.interactive_loop()