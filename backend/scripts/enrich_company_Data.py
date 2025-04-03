import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import csv
from io import StringIO
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

df = pd.read_csv("cleaned_gpt_companies.csv")
df = df[~df["Company"].str.contains("I'm sorry", na=False)]
df = df[~df["Event"].str.lower().str.strip().isin(["live exhibit", "", "none", "-"])]
companies = df[["Company", "Event"]].dropna(subset=["Company"]).drop_duplicates(subset="Company")

def batch_list(df, batch_size):
    for i in range(0, len(df), batch_size):
        yield df.iloc[i:i + batch_size]

# Robust parser for GPT CSV output
def parse_gpt_csv(content, original_batch):
    rows = []
    content = content.replace("```csv", "").replace("```", "").strip()

    try:
        f = StringIO(content)
        reader = csv.DictReader(f, skipinitialspace=True)
        for line in reader:
            company = (line.get("Company") or "").strip().strip('"')
            if not company:
                continue
            rows.append({
                "Company": company,
                "Estimated Revenue": (line.get("Estimated Revenue") or "").strip(),
                "Employees": (line.get("Employees") or "").strip(),
                "Industry": (line.get("Industry") or "").strip()
            })
    except Exception as e:
        print(f"Failed to parse GPT CSV for batch {[c for c in original_batch['Company']]}: {e}")
    return rows

results = []

for batch_df in batch_list(companies, 10):
    batch_list_companies = batch_df["Company"].tolist()
    print(f"Processing batch: {batch_list_companies}")

    prompt = f"""
You're an AI assistant helping with B2B sales research.

Estimate the following for each company:
- Estimated Revenue (range)
- Employee Size (range)
- Industry (real-world industry name, not numeric)

List:
{chr(10).join(batch_list_companies)}

Respond in CSV format with headers: Company, Estimated Revenue, Employees, Industry.
Only include companies from the list.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        if not content:
            print(f"Empty response for batch: {batch_list_companies}")
            continue

        print("GPT Response:")
        print(content)
        print("-" * 60)

        parsed_rows = parse_gpt_csv(content, batch_df)

        if len(parsed_rows) < len(batch_list_companies):
            found_companies = [r["Company"] for r in parsed_rows]
            missing = list(set(batch_list_companies) - set(found_companies))
            print(f" Not found in GPT output: {missing}")

        results.extend(parsed_rows)

    except Exception as e:
        print(f"GPT API error: {e}")
        continue

    time.sleep(1.5)  # Avoid rate limiting

if not results:
    print("No valid GPT responses. Exiting.")
    exit()

enriched_df = pd.DataFrame(results)
final_df = companies.merge(enriched_df, on="Company", how="left")


unmatched = final_df[final_df["Estimated Revenue"].isna()]
if not unmatched.empty:
    print("These companies were not enriched by GPT:")
    print(unmatched["Company"].tolist())

final_df = final_df[~final_df["Estimated Revenue"].isna()]

def revenue_score(rev):
    if pd.isna(rev): return 0
    rev = rev.lower().replace("$", "").replace(",", "").replace("+", "").strip()
    match = re.search(r'(\d+\.?\d*)\s*(m|b)', rev)
    if not match: return 0
    number, unit = match.groups()
    try:
        number = float(number)
        return int(number * 1000) if unit == "b" else int(number)
    except:
        return 0

def employee_score(emp):
    if pd.isna(emp): return 0
    emp = emp.lower().replace(",", "").replace("+", "").strip()
    match = re.search(r'(\d+)', emp)
    if not match: return 0
    try:
        return int(match.group(1))
    except:
        return 0

final_df["Revenue Score"] = final_df["Estimated Revenue"].apply(revenue_score)
final_df["Employee Score"] = final_df["Employees"].apply(employee_score)

final_df = final_df.sort_values(by=["Revenue Score", "Employee Score"], ascending=False)

cols = ["Company", "Event", "Estimated Revenue", "Employees", "Industry", "Revenue Score", "Employee Score"]
final_df = final_df[[col for col in cols if col in final_df.columns]]

# Save to CSV
final_df.to_csv("enriched_companies_with_gpt_ranked.csv", index=False)
print("Ranked company data saved to enriched_companies_with_gpt_ranked.csv")
