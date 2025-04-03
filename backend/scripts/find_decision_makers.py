
import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("APOLLO_API_KEY")

HEADERS = {
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

RELEVANT_KEYWORDS = ["marketing", "product", "innovation", "research", "development", "strategy", "sales"]
TITLES = ["VP", "Director", "Head", "Manager", "President", "Chief"]

def get_org_id(company_name):
    url = "https://api.apollo.io/v1/organizations/search"
    payload = {
        "q_organization_name": company_name,
        "page": 1,
        "per_page": 1
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            orgs = response.json().get("organizations", [])
            if orgs:
                return orgs[0].get("id")
        else:
            print(f"Org search failed for {company_name}: {response.status_code}")
    except Exception as e:
        print(f"Org search exception for {company_name}: {e}")
    return None

def enrich_person(person):
    url = "https://api.apollo.io/v1/people/match"
    payload = {
        "first_name": person.get("first_name"),
        "last_name": person.get("last_name"),
        "organization_id": person.get("organization_id"),
        "title": person.get("title")
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            enriched = response.json().get("person", {})
            return {
                "Email": enriched.get("email", "Can't find"),
                "Phone": enriched.get("phone_number", "Can't find")
            }
    except:
        pass
    return {"Email": "Can't find", "Phone": "Can't find"}

def search_people(company, event, revenue, size, industry, org_id):
    url = "https://api.apollo.io/v1/mixed_people/search"
    payload = {
        "organization_ids": [org_id],
        "person_titles": TITLES,
        "page": 1,
        "per_page": 25
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            print(f"⚠️ People search failed for {company}: {response.status_code}")
            return []
        
        people = response.json().get("people", [])
        results = []
        for person in people:
            title = person.get("title", "")
            if not title or not any(k in title.lower() for k in RELEVANT_KEYWORDS):
                continue

            enriched = enrich_person(person)

            results.append({
                "Event": event,
                "Company": company,
                "Name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                "Title": title,
                "Email": enriched["Email"],
                "Phone": enriched["Phone"],
                "LinkedIn": person.get("linkedin_url", ""),
                "Location": person.get("city", ""),
                "Revenue": revenue if revenue else "Can't find",
                "Size": size if size else "Can't find",
                "Industry": industry if industry else "Can't find"
            })
        return results
    except Exception as e:
        print(f"Error at {company}: {e}")
        return []

def main():
    df = pd.read_csv("enriched_companies_with_gpt_ranked.csv")
    df = df[df["Company"].notna()]
    df = df[~df["Company"].str.contains("I'm sorry", na=False)]
    df = df[~df["Event"].str.lower().str.contains("live exhibit", na=False)]
    df = df.drop_duplicates(subset="Company")

    print(f"Total companies to search: {len(df)}")

    all_results = []
    for _, row in df.iterrows():
        company = row["Company"]
        event = row["Event"]
        revenue = row.get("Estimated Revenue", "Can't find")
        size = row.get("Employees", "Can't find")
        industry = row.get("Industry", "Can't find")

        org_id = get_org_id(company)
        if not org_id:
            print(f"Skipping {company} — no Org ID found.")
            continue

        people = search_people(company, event, revenue, size, industry, org_id)
        all_results.extend(people)
        time.sleep(1.2)

    final_df = pd.DataFrame(all_results)
    final_df.to_csv("filtered_decision_makers.csv", index=False)
    print("Saved filtered decision makers")

if __name__ == "__main__":
    main()