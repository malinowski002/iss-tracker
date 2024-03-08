import math
import requests
from PIL import Image

PI = 3.14159


def get_current_position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    longitude = response.json()["iss_position"]["longitude"]
    latitude = response.json()["iss_position"]["latitude"]
    return longitude, latitude


def update_position(label_position, label_iss, label_position_xy):
    longitude, latitude = get_current_position()
    label_position.configure(text=f"Position (degrees)\nlatitude = {latitude}\nlongitude = {longitude}")
    label_position.after(3000, update_position, label_position, label_iss, label_position_xy)

    x_y = get_x_y(latitude, longitude)
    label_position_xy.configure(text=f"Position (pixels)\nlatitude = {x_y[0]}\nlongitude = {x_y[1]}")
    label_iss.place(x=x_y[0] + 10, y=x_y[1] + 10)


def get_x_y(lat, lon):
    lat_rad = float(lat) * PI / 180.0
    lon_rad = float(lon) * PI / 180.0

    x = (lon_rad / (2 * PI) + 0.5) * 650
    y = (0.5 - math.log(math.tan(PI / 4 + lat_rad / 2)) / (2 * PI)) * 650
    return round(x), round(y)


def get_astronauts_names():
    response = requests.get("http://api.open-notify.org/astros.json")
    people = response.json()["people"]
    people_names = "Astronauts currently on ISS:\n"

    for person in people:
        if person["craft"] == "ISS":
            people_names += f"{person['name']}\n"
    print(people_names)
    return people_names
