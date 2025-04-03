import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

df = pd.read_csv("gpt_extracted_companies.csv")

event_groups = df.groupby("Event")["Company"].apply(list).to_dict()

results = []
for event_name, raw_companies in event_groups.items():
    prompt = f"""
You are an assistant that filters out only valid company names from a noisy list.

Below is a list of items labeled as "companies" for an event called "{event_name}". However, the list includes junk, event names, error messages, and unrelated phrases.

Please return only the **real, full company names** that are likely sponsors or exhibitors. Just the names, one per line.

List:
---
{chr(10).join(raw_companies)}
---
Only output real company names. No extra text.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        output = response.choices[0].message.content
        for name in output.split("\n"):
            name = name.strip()
            if name:
                results.append({
                    "Event": event_name,
                    "Company": name
                })
    except Exception as e:
        print(f"Error for event: {event_name} — {e}")
        results.append({
            "Event": event_name,
            "Company": f"ERROR: {str(e)}"
        })

pd.DataFrame(results).to_csv("cleaned_gpt_companies.csv", index=False)
print("Cleaned company names")