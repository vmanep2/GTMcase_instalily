from dotenv import load_dotenv
import os
import sys
from serpapi import GoogleSearch
import pandas as pd
import re

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

def extract_date(text):
    match = re.search(r'([A-Z][a-z]+\s\d{1,2}–\d{1,2},?\s2025|[A-Z][a-z]+\s\d{1,2},?\s2025|2025)', text)
    return match.group(0) if match else "N/A"

def search_events(query, num_results=10):
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": API_KEY, 
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    event_rows = []
    for res in results.get("organic_results", []):
        title = res.get("title", "N/A")
        link = res.get("link", "N/A")
        snippet = res.get("snippet", "No description provided.")
        date = extract_date(snippet)

        event_rows.append({
            "Event Name": title,
            "URL": link,
            "Date": date,
            "Description": snippet
        })

    return pd.DataFrame(event_rows)

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "2025 signage and graphics trade shows"
    df = search_events(query)
    pd.set_option('display.max_colwidth', None)
    df.to_csv("events_output.csv", index=False)
    print("Saved to events_output.csv")