import tkinter as tk
from tkinter import *
import random

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("APPLICATION")
        w = master.winfo_screenwidth()
        h = master.winfo_screenheight()
        master.geometry("%dx%d" % (w, h))
        master.configure(bg="#333333")  # Donkere achtergrondkleur

        self.canvas = Canvas(master, width=500, height=300, bg="#F0F0F0")  # Lichtgekleurde canvas-achtergrond
        self.canvas.pack(pady=20)

        self.shapes = ["circle", "rectangle", "triangle"]
        self.colors = ["RED", "GREEN", "BLUE", "YELLOW"]
        self.selected_combinations = []

        self.shape_labels = []
        self.draw_button = None

        for i, shape in enumerate(self.shapes):
            x = 50 + (i * 125)  # Aangepaste tussenruimte
            y = 100
            if shape == "circle":
                self.canvas.create_oval(x, y, x + 120, y + 120, fill="#F0F0F0", outline="#000000", width=2)  # Lichtgekleurde vulling en zwarte omtrek
            elif shape == "rectangle":
                self.canvas.create_rectangle(x, y, x + 120, y + 120, fill="#F0F0F0", outline="#000000", width=2)
            elif shape == "triangle":
                self.canvas.create_polygon(x + 60, y, x, y + 120, x + 120, y + 120, fill="#F0F0F0", outline="#000000", width=2)

        for i, shape in enumerate(self.shapes):
            for j, color in enumerate(self.colors):
                x = 590 + (i * 125) + (j % 2) * 40  # Aangepaste tussenruimte
                y = 410 + (j // 2) * 40
                button = Button(master, bg=color, command=lambda s=shape, c=color: self.select_combination(s, c), relief="flat")  # Vlakke knopstijl
                button.place(x=x, y=y, width=40, height=40)

        self.reset_button = Button(master, text="Reset", command=self.reset_selections, bg="#800000", fg="#FFFFFF", relief="flat", font=("Arial", 12, "bold"))  # Rode knop met witte tekst en vet lettertype
        self.reset_button.place(x=700, y=580, width=100)

        self.draw_button = Button(master, text="Draw", command=self.draw_shapes, bg="#336699", fg="#FFFFFF", relief="flat", font=("Arial", 12, "bold"))  # Blauwe knop met witte tekst en vet lettertype
        self.draw_button.place(x=820, y=580, width=100)

        self.send_button = Button(master, text="Send", command=self.send_values, bg="#336699", fg="#FFFFFF", relief="flat", font=("Arial", 12, "bold"))  # Blauwe knop met witte tekst en vet lettertype
        self.send_button.place(x=940, y=580, width=100)

        self.action_var = StringVar()
        self.action_var.set("load")  # Standaardactie is "load"

        self.load_button = Radiobutton(master, text="Load", variable=self.action_var, value="load", bg="#333333", fg="#FFFFFF", font=("Arial", 10, "italic"), selectcolor="#333333")
        self.load_button.place(x=560, y=580)

        self.unload_button = Radiobutton(master, text="Unload", variable=self.action_var, value="unload", bg="#333333", fg="#FFFFFF", font=("Arial", 10, "italic"), selectcolor="#333333")
        self.unload_button.place(x=620, y=580)

    def select_combination(self, shape, color):
        action = self.action_var.get()  # Geselecteerde actie ("load" of "unload")
        if len(self.selected_combinations) < 3:
            self.selected_combinations.append((shape, color, action))
            self.update_combination_labels()

            if len(self.selected_combinations) == 3:
                self.draw_button.configure(state="normal")

    def update_combination_labels(self):
        for label in self.shape_labels:
            label.destroy()

        for i, combination in enumerate(self.selected_combinations):
            shape, color, action = combination
            label_text = f"{color}\n{shape}\n{action}"  # Waarden scheiden met nieuwe regels
            label = Label(self.master, text=label_text, bg="#333333", fg="#FFFFFF", font=("Arial", 10, "italic"))  # Witte labeltekst met cursief lettertype
            label.place(x=590 + i * 125, y=510)  # Aangepaste tussenruimte
            self.shape_labels.append(label)

    def draw_shapes(self):
        self.canvas.delete("all")
        for i, combination in enumerate(self.selected_combinations):
            shape, color, action = combination
            if shape == "circle":
                self.canvas.create_oval(50 + (i * 125), 100, 170 + (i * 125), 220, fill=color, outline="black")  # Omtrek toegevoegd
            elif shape == "rectangle":
                self.canvas.create_rectangle(50 + (i * 125), 100, 170 + (i * 125), 220, fill=color, outline="black")  # Omtrek toegevoegd
            elif shape == "triangle":
                self.canvas.create_polygon(110 + (i * 125), 100, 50 + (i * 125), 220, 170 + (i * 125), 220, fill=color, outline="black")  # Omtrek toegevoegd

    def reset_selections(self):
        self.selected_combinations = []
        self.update_combination_labels()
        self.draw_button.configure(state="disabled")

    def send_values(self):
        selected_values = self.selected_combinations
        # Voer acties uit met de geselecteerde waarden
        # Bijvoorbeeld, print ze of geef ze door aan het hoofdbestand
       #root.destroy()  # Sluit het toepassingsvenster
        return self.selected_combinations
    
    def destroy(self):
        self.master.destroy()


# root = tk.Tk()
# app = DrawingApp(root)
# root.mainloop()
