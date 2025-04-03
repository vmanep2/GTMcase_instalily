import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def find_exhibitor_links(base_url):
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        exhibitor_links = []

        keywords = [
            "exhibitor", "sponsor", "partner", "vendor", "company", 
            "attending", "list", "who's coming", "gallery", "directory"
        ]

        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True).lower()
            href = a["href"].lower()
            
            if any(kw in text for kw in keywords) or any(kw in href for kw in keywords):
                full_url = requests.compat.urljoin(base_url, a["href"])
                exhibitor_links.append((text if text else href, full_url))

        return exhibitor_links
    except Exception as e:
        return [("error", str(e))]

df = pd.read_csv("events_output.csv")

results = []
for idx, row in df.iterrows():
    event_name = row["Event Name"]
    url = row["URL"]
    links = find_exhibitor_links(url)
    for label, link in links:
        results.append({
            "Event Name": event_name,
            "Event URL": url,
            "Link Text": label,
            "Exhibitor/Sponsor URL": link
        })

output_df = pd.DataFrame(results)
output_df.to_csv("exhibitor_links.csv", index=False)
print("Saved exhibitor_links.csv")