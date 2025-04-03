import os
import subprocess

query = os.getenv("SEARCH_QUERY")

# Run each script step-by-step
pipeline = [
    ["python3", "scripts/find_events.py", query],
    ["python3", "scripts/scrape_events.py"],
    ["python3", "scripts/gpt_scrape_company_names.py"],
    ["python3", "scripts/filter_gpt_companies.py"],
    ["python3", "scripts/enrich_company_Data.py"],
    ["python3", "scripts/find_decision_makers.py"],
]

for step in pipeline:
    try:
        print(f"Running: {' '.join(step)}")
        subprocess.run(step, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Step failed: {' '.join(step)}")
        print(e)
        exit(1)