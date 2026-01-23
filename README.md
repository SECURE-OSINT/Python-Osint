# Python-Osint
This project is created for educational and cybersecurity research purposes only. The author is not responsible for any illegal or malicious use of this tool. Please ensure you respect local laws and the privacy of others.


## Usage

Install dependencies:

pip install -r requirements.txt

Generate a report from a JSON input file:

python main.py --input reports/sample_input.json --output reports/report.html

Generate a report from CLI fields only:

python main.py --full-name "Example Person" --email example@email.com --phone "+33 6 00 00 00 00" --username exampleuser

Add findings, sources, notes, and limitations from the CLI:

python main.py \
  --finding "Profil public|Public profile|Bio publique|Public bio|https://example.com/profile|medium" \
  --source "Profil public|Public profile|https://example.com/profile|medium|Page publique|Public page" \
  --note "Note en francais|Note in English" \
  --limitation "Donnees basees sur les informations fournies|Data is based on provided information"

The output is an HTML report with a slide-like layout. You can open it in a browser and export it to PDF or import it into presentation tools.

## Input format (JSON)

reports/sample_input.json is a template. The expected structure is:

- subject: full_name, email, phone, username
- findings: list of objects with category, category_en, details, details_en, source, reliability
- sources: list of objects with label, label_en, url, reliability, notes, notes_en
- notes: list of objects with fr, en
- limitations: list of objects with fr, en

## Safety

This tool only formats user-provided information into a report. It does not perform automated data collection or lookups.
