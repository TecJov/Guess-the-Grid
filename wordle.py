import tkinter as tk
from tkinter import messagebox
import random

class WordleGame:
    def __init__(self, root):
        self.root = root
        root.title("Wordle Plus")
        
        self.words = ["phone", "apple", "beach", "cloud", "dance", "eagle", "frown", "grape", "house", "igloo"]
        self.secret = random.choice(self.words)
        self.tries_left = 6
        self.past_guesses = []
        self.used_hint = False

        self.setup_ui()

    def setup_ui(self):
        self.boxes = []
        for i in range(6):
            row = []
            for j in range(5):
                e = tk.Entry(self.root, width=2, font=('Helvetica', 20), justify='center')
                e.grid(row=i, column=j, padx=2, pady=2)
                row.append(e)
            self.boxes.append(row)

        tk.Button(self.root, text="Enter", command=self.check_guess).grid(row=6, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Hint", command=self.get_hint).grid(row=6, column=3, columnspan=2, pady=10)

    def check_guess(self):
        guess = ''
        for e in self.boxes[6 - self.tries_left]:
            guess += e.get().lower()

        if len(guess) != 5:
            messagebox.showwarning("Oops", "Word should be 5 letters!")
            return

        self.past_guesses.append(guess)
        self.color_boxes(6 - self.tries_left, guess)

        if guess == self.secret:
            messagebox.showinfo("Great Job!", f"You got it in {7 - self.tries_left} tries!")
            self.root.quit()
        elif self.tries_left == 1:
            messagebox.showinfo("Womp womp", f"Out of guesses! The word was {self.secret}.")
            self.root.quit()
        else:
            self.tries_left -= 1

    def color_boxes(self, row, word):
        for i, letter in enumerate(word):
            if letter == self.secret[i]:
                color = 'green'
            elif letter in self.secret:
                color = 'yellow'
            else:
                color = 'gray'
            self.boxes[row][i].config(bg=color, fg='white' if color != 'yellow' else 'black')

    def get_hint(self):
        if self.used_hint:
            messagebox.showinfo("Sorry", "You already used your hint!")
            return

        green_count = sum(1 for guess in self.past_guesses for i, letter in enumerate(guess) if letter == self.secret[i])
        if green_count >= 3:
            messagebox.showinfo("Can't help", "You already know 3 or more letters!")
            return

        not_guessed = [i for i, letter in enumerate(self.secret) if all(guess[i] != letter for guess in self.past_guesses)]
        if not_guessed:
            hint_pos = random.choice(not_guessed)
            messagebox.showinfo("Here's a hint", f"Letter {hint_pos + 1} is '{self.secret[hint_pos]}'")
            self.used_hint = True
        else:
            messagebox.showinfo("Weird", "No letters left to hint!")

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()