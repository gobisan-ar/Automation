import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = "63"
HEIGHT_CM = "172"
AGE = "23"

NT_APP_ID = os.environ.get('NT_APP_ID')
NT_API_KEY = os.environ.get('NT_API_KEY')
NT_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEET_TOKEN = os.environ.get('SHEET_TOKEN')
SHEET_ENDPOINT = os.environ.get('SHEET_ENDPOINT')

exercise_done = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": NT_APP_ID,
    "x-app-key": NT_API_KEY,
}

exercise_params = {
    "query": exercise_done,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=NT_ENDPOINT, json=exercise_params, headers=headers)
result = response.json()
print(result)

date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer {SHEET_TOKEN}"
}

for exercise in result["exercises"]:
    sheet_body = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheet_body, headers=bearer_headers)

    print(sheet_response.text)
