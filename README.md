# Jicho

Jicho is a Python-based project focused on collecting, processing, and documenting observations through automated data gathering workflows.

## 📂 Project Structure

```text
Jicho/
├── main.py                   # Core Jicho OS, Terminal loop, and Dashboard UI
├── scraper.py                # KenyaLawScraper stream extraction logic
├── local_reports.csv         # Offline database for manually logged incidents
├── jicho_observations.md     # Automated deep-dive markdown logs
├── requirements.txt          # Project dependencies
└── .gitignore                # Git exclusion rules (protects local data)
```

## ✨ Features

- Humanitarian Dashboard: A multi-panel live view tracking Missing Persons, Preventive Actions, and Civic/Legislative impacts.

- Proximity Tripwire: Smart alerting system that flags incidents occurring in a customizable "Home Zone" (e.g., Nairobi / Langata).

- Source Verification: Automatically assigns trust badges based on known, verified reporting entities.

- Manual Incident Logging: Built-in wizard to safely log offline, localized citizen reports.

- Automated Truth Analysis: Scrapes, compiles, and formats deep-dive investigations on specific queries directly into Markdown reports.

- Live Telemetry: Modular web scraper utilizing RSS streams to bypass heavy API limits.

## 🛠️ Tech Stack

- Python 3
- Custom scraping utilities
- Markdown documentation

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/madoyakimberley/Jicho
cd Jicho
```

### Install Dependencies

```bash
# Initialize uv environment and install dependencies (pandas, requests)
uv venv
uv pip install -r requirements.txt
```

### Run the Project

```bash
uv run main.py
```

## 📖 Documentation

Observations and collected findings are documented in:

```text
jicho_observations.md
```

## 📌 Repository

GitHub:
https://github.com/madoyakimberley/Jicho

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📄 License

Add your preferred license (MIT, Apache 2.0, GPL, etc.) before production release.
