import requests
from datetime import datetime
import os


APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
BEARER = os.environ['BEARER']
exercise_endpoint = os.environ['EXERCISE_ENDPOINT']
sheet_endpoint = os.environ['SHEET_ENDPOINT']
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
}

parameters = {
    "query": exercise_text,
    "gender": "male",
    "weight_kg": 78.5,
    "height_cm": 191.42,
    "age": 34
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheet_header = {
    'Authorization': F"Bearer {BEARER}",
    "Content-Type": "application/json",
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, headers=sheet_header)
    print(sheet_response.text)
