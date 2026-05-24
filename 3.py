import tkinter as tk
import requests
from PIL import Image, ImageTk
import io

URL = "https://nekos.best/api/v2/neko"


class GenerateImage:
    def __init__(self, root, url=URL):
        self.root = root
        self.root.title("Генерация картинок")
        self.root.geometry("500x600")
        self.url = url

        self.image_lable = tk.Label(self.root, text="Нажмите кнопку")
        self.image_lable.pack(expand=True, fill="both")

        self.next_btn = tk.Button(
            self.root, text="Следующая картинка", command=self.load_new_image
        )
        self.next_btn.pack(pady=20)

    def load_new_image(self):
        response = requests.get(self.url)
        data = response.json()
        image_url = data["results"][0]["url"]
        image_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((450, 450))
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_lable.config(image=self.tk_image, text="")


if __name__ == "__main__":
    root = tk.Tk()
    image = GenerateImage(root)
    root.mainloop()
