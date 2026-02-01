import requests
import os
from dotenv import load_dotenv
API_URL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
api_token = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {api_token}"}


def analyze_content(text):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})
        results = response.json()

        toxic_score = 0
        for label in results[0]:
            if label['label'] == 'toxic':
                toxic_score = label['score']

        return toxic_score
    except Exception as e:
        print(f"AI Error: {e}")
        return 0