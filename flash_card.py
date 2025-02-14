from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
flip_timer = None
countdown_timer = 5

# Read data from csv file
data = pd.read_csv("data/french_words.csv")
to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer, countdown_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    word = current_card["French"]
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(word_text, text=word, fill="black")
    canvas.itemconfig(definition_text, text="French", fill="black")
    countdown_timer = 5
    update_timer()
    flip_timer = window.after(5000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(definition_text, text="English", fill="white")

def update_timer():
    global countdown_timer
    if countdown_timer > 0:
        countdown_label.config(text=f"Time: {countdown_timer}s")
        countdown_timer -= 1
        window.after(1000, update_timer)

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Create a canvas and add images
canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Add text items to the canvas
word_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "bold"))
definition_text = canvas.create_text(400, 263, text="", font=("Arial", 20, "italic"))

# Add timer display
countdown_label = Label(window, text=f"Time: {countdown_timer}s", bg=BACKGROUND_COLOR, fg="black", font=("Arial", 16))
countdown_label.grid(row=0, column=1, sticky="NE", padx=60, pady=30)

# Load button images and add buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=next_card)
known_button.grid(row=1, column=1)

flip_timer = window.after(5000, func=flip_card)
next_card()

window.mainloop()