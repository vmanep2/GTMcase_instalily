from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import pandas as pd
import os
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

@app.route("/api/search_events", methods=["POST"])
def search_events():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    os.environ["SEARCH_QUERY"] = query

    try:
        subprocess.run(["python3", "run_pipeline.py"], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Pipeline failed: {str(e)}"}), 500

    try:
        df = pd.read_csv("filtered_decision_makers.csv")
        df = df.fillna("Can't Find")
        print("Returning filtered_decision_makers.csv")
        print(df.head())
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": f"Failed to load results: {str(e)}"}), 500
    
@app.route("/api/generate_content", methods=["POST"])
def generate_content():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        return jsonify({ "content": content })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)