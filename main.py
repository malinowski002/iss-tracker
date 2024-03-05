import math

import requests
import customtkinter
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
    label_iss.place(x=x_y[0]+10, y=x_y[1]+10)


def get_x_y(lat, lon):
    lat_rad = float(lat) * PI / 180.0
    lon_rad = float(lon) * PI / 180.0

    x = (lon_rad / (2 * PI) + 0.5) * 650
    y = (0.5 - math.log(math.tan(PI / 4 + lat_rad / 2)) / (2 * PI)) * 650
    return round(x), round(y)


def main():
    root = customtkinter.CTk(fg_color="#2A2A2A")
    root.title("ISS Tracker")
    root.geometry("952x670")

    map_image = customtkinter.CTkImage(light_image=Image.open("world_map.png"), size=(650, 650))
    label_map = customtkinter.CTkLabel(root, image=map_image, text="")
    label_map.place(x=10, y=10)

    label_position = customtkinter.CTkLabel(
        root,
        text="Position",
        justify="left",
        font=("Helvetica", 16)
    )
    label_position.place(x=670, y=20)

    label_position_xy = customtkinter.CTkLabel(
        root,
        text="x y position",
        justify="left",
        font=("Helvetica", 16)
    )
    label_position_xy.place(x=670, y=100)

    label_iss = customtkinter.CTkLabel(
        root,
        text="",
        fg_color="red",
        width=10,
        height=10,
        font=("Arial", 1))
    label_iss.place(x=370, y=40)

    response = requests.get("http://api.open-notify.org/astros.json")
    people = response.json()["people"]
    people_names = "Astronauts currently on ISS:\n"

    for person in people:
        if person["craft"] == "ISS":
            people_names += f"{person['name']}\n"
    print(people_names)

    label_astronauts = customtkinter.CTkLabel(
        root,
        text=people_names,
        justify="left",
        font=("Helvetica", 16)
    )
    label_astronauts.place(x=670, y=200)

    update_position(label_position, label_iss, label_position_xy)
    root.mainloop()


main()
