import customtkinter
import requests
from PIL import Image

from iss_tracker import update_position, get_astronauts_names


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

    label_astronauts = customtkinter.CTkLabel(
        root,
        text=get_astronauts_names(),
        justify="left",
        font=("Helvetica", 16)
    )
    label_astronauts.place(x=670, y=200)

    update_position(label_position, label_iss, label_position_xy)
    root.mainloop()


if __name__ == "__main__":
    main()
