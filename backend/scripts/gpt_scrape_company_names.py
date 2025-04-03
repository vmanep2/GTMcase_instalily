from openai import OpenAI
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def extract_companies_from_html_gpt(html):
    prompt = f"""
You are an AI assistant that extracts sponsor or exhibitor company names from raw HTML content of event pages.

Extract only real, complete company names from this HTML. Return a list of company names, one per line.

HTML Content:
---
{html[:15000]}
---
Only output company names, one per line. Do not include extra text or explanations.
"""
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response.choices[0].message.content
    return [line.strip() for line in content.split("\n") if line.strip()]

df = pd.read_csv("exhibitor_links.csv")
results = []

for _, row in df.iterrows():
    url = row["Exhibitor/Sponsor URL"]
    event = row["Event Name"]
    print(f"Processing: {url}")
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
        companies = extract_companies_from_html_gpt(html)
        for company in companies:
            results.append({
                "Event": event,
                "Exhibitor Page": url,
                "Company": company
            })
    except Exception as e:
        results.append({
            "Event": event,
            "Exhibitor Page": url,
            "Company": f"ERROR: {e}"
        })

pd.DataFrame(results).to_csv("gpt_extracted_companies.csv", index=False)
print("Done! Saved to gpt_extracted_companies.csv")