import tkinter as tk
from tkinter import messagebox
import random

class LetterGuesser:
    def __init__(self, root):
        self.root = root
        root.title("Word Wizard")
        
        self.words = ["zebra", "quilt", "fjord", "waltz", "jumbo", "pixel", "vortex", "sphinx", "yacht", "gnome"]
        self.target = random.choice(self.words)
        self.chances = 7
        self.guesses = []
        self.hint_used = False

        self.create_ui()

    def create_ui(self):
        self.cells = []
        for i in range(7):
            row = []
            for j in range(5):
                e = tk.Entry(self.root, width=2, font=('Courier', 22, 'bold'), justify='center')
                e.grid(row=i, column=j, padx=3, pady=3)
                row.append(e)
            self.cells.append(row)

        tk.Button(self.root, text="Check", command=self.verify_guess, bg='#4CAF50', fg='white').grid(row=7, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Clue", command=self.request_clue, bg='#2196F3', fg='white').grid(row=7, column=3, columnspan=2, pady=10)

    def verify_guess(self):
        guess = ''.join(e.get().lower() for e in self.cells[7 - self.chances])

        if len(guess) != 5:
            messagebox.showwarning("Hold up!", "Please enter a 5-letter word.")
            return

        self.guesses.append(guess)
        self.paint_cells(7 - self.chances, guess)

        if guess == self.target:
            messagebox.showinfo("Bravo!", f"You cracked it in {8 - self.chances} attempts!")
            self.root.quit()
        elif self.chances == 1:
            messagebox.showinfo("Game Over", f"Better luck next time! The word was {self.target}.")
            self.root.quit()
        else:
            self.chances -= 1

    def paint_cells(self, row, word):
        for i, letter in enumerate(word):
            if letter == self.target[i]:
                color = '#9C27B0'  # Purple
            elif letter in self.target:
                color = '#FF9800'  # Orange
            else:
                color = '#607D8B'  # Blue Grey
            self.cells[row][i].config(bg=color, fg='white')

    def request_clue(self):
        if self.hint_used:
            messagebox.showinfo("Oops", "You've already used your clue!")
            return

        correct_count = sum(1 for guess in self.guesses for i, letter in enumerate(guess) if letter == self.target[i])
        if correct_count >= 3:
            messagebox.showinfo("Nice try", "You already know 3 or more letters!")
            return

        unknown = [i for i, letter in enumerate(self.target) if all(guess[i] != letter for guess in self.guesses)]
        if unknown:
            clue_index = random.choice(unknown)
            messagebox.showinfo("Here's a clue", f"Letter {clue_index + 1} is '{self.target[clue_index]}'")
            self.hint_used = True
        else:
            messagebox.showinfo("Interesting", "No new letters to reveal!")

if __name__ == "__main__":
    root = tk.Tk()
    game = LetterGuesser(root)
    root.mainloop()
