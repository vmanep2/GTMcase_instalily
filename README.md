# Lead Generation AI Dashboard

A smart, end-to-end dashboard that automatically:
- Finds relevant **industry events** and **trade shows**
- Extracts **exhibitor/sponsor company names** from event pages
- Enriches companies with **revenue, size, and industry**
- Locates **key decision makers** and their contact information using Apollo.io
- Generates AI-powered **outreach messages** and **rationale** for why it's a qualified lead

## Prerequisites
- Python 3.9+ with `venv`
- Node.js v18+
- [SerpAPI](https://serpapi.com/), [OpenAI](https://platform.openai.com/), and [Apollo](https://apollo.io/) API keys

## Setup Instructions
```bash
git clone https://github.com/vmanep2/GTMcase_instalily.git
cd GTMcase_instalily
```

## Create .env in root directory with the following exact names and your own API keys
```bash
OPENAI_KEY=...
SERPAPI_KEY=...
APOLLO_API_KEY=...
```

## Run the Full App
```bash
chmod +x launch.sh
./launch.sh
```