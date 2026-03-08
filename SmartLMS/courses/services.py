import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUMMARIZER_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def generate_lesson_summary(text):
    if len(text)<100:
        return text,[]

    payload = {
        "inputs":text,
        "parameters":{
            "max_length":150,
            "min_length":150,
            "do_sample":False,
        }
    }

    try:
        response = requests.post(SUMMARIZER_API_URL, json=payload, headers=HEADERS)
        result = response.json()
        summary = result[0]["summary_text"]

        key_points=summary.split(". ")

        return summary,key_points

    except Exception as e:
        print(f"AI summarizer failed with exception: {e}")

        return "generation failed",[]


QUIZ_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def generate_quiz_questions(lesson_content):
    prompt = f"Generate 3 multiple choice questions based on this text: {lesson_content}"

    payload = {"input":prompt, "parameters":{"max_length":250}}

    try:
        response = requests.post(QUIZ_API_URL, json=payload, headers=HEADERS)
        return response.json()[0]["generated_text"]

    except Exception as e:

        return f"generation failed: {e}"


