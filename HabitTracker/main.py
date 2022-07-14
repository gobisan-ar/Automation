import os
import requests
from datetime import datetime

USERNAME = os.environ.get('USERNAME')
TOKEN = os.environ.get('TOKEN')
GRAPH_ID = os.environ.get('GRAPH_ID')


# Create user account
pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)


# Create graph
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_params = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
# print(response.text)


# Create pixel
pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

date = datetime.now().strftime("%Y%m%d")

pixel_params = {
    "date": date,
    "quantity": input("How many kilometers did you cycle today? "),
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_params, headers=headers)
print(response.text)

# Update pixel
pixel_update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"

new_pixel_params = {
    "quantity": "14.53"
}

# response = requests.put(url=pixel_update_endpoint, json=new_pixel_params, headers=headers)
# print(response.text)


# Delete pixel
pixel_delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{date}"

# response = requests.delete(url=pixel_delete_endpoint, headers=headers)
# print(response.text)
