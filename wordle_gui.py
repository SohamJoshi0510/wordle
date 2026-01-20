import tkinter as tk
from tkinter import messagebox
import random
from get_5_letter_words import word_list

word_list_26 = [
    "apple", "beach", "brain", "cloud", "dance", "eagle", "flame", "glass",
    "house", "index", "juice", "light", "money", "night", "ocean", "party",
    "quiet", "river", "smile", "table", "under", "voice", "water", "young", "zebra"
]

def color_mapper(word, guess):
    """Returns a list of colors for each letter in the guess"""
    colors = ['gray'] * 5
    word_letters = list(word)
    
    # First pass: mark correct positions (green)
    for i in range(5):
        if guess[i] == word[i]:
            colors[i] = 'green'
            word_letters[i] = None
    
    # Second pass: mark wrong positions (yellow)
    for i in range(5):
        if colors[i] == 'gray' and guess[i] in word_letters:
            colors[i] = 'yellow'
            word_letters[word_letters.index(guess[i])] = None
    
    return colors

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")
        self.root.geometry("500x700")
        self.root.configure(bg='#121213')
        
        self.MAX_ATTEMPTS = 6
        self.attempt = 0
        self.word = random.choice(word_list_26)
        self.struct = self.converter(self.word)
        
        # Alphabet state tracking
        self.alphabet = [chr(ord('a') + i) for i in range(26)]
        self.color_map_alphabet = {}
        
        # Create UI elements
        self.create_widgets()
        
    def converter(self, word):
        letters = set(word)
        struct = {letter: [] for letter in letters}
        for i, letter in enumerate(word):
            struct[letter].append(i)
        return struct
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="WORDLE", font=('Arial', 32, 'bold'),
                        bg='#121213', fg='white')
        title.pack(pady=20)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='#121213')
        self.board_frame.pack(pady=10)
        
        # Create grid of letter boxes
        self.letter_boxes = []
        for row in range(self.MAX_ATTEMPTS):
            row_boxes = []
            row_frame = tk.Frame(self.board_frame, bg='#121213')
            row_frame.pack(pady=2)
            for col in range(5):
                box = tk.Label(row_frame, text='', font=('Arial', 24, 'bold'),
                             width=3, height=1, bg='#3a3a3c', fg='white',
                             relief='solid', borderwidth=2)
                box.pack(side='left', padx=2)
                row_boxes.append(box)
            self.letter_boxes.append(row_boxes)
        
        # Alphabet display
        self.alphabet_frame = tk.Frame(self.root, bg='#121213')
        self.alphabet_frame.pack(pady=20)
        
        self.alphabet_labels = {}
        for i, letter in enumerate(self.alphabet):
            if i % 13 == 0:
                row = tk.Frame(self.alphabet_frame, bg='#121213')
                row.pack()
            label = tk.Label(row, text=letter.upper(), font=('Arial', 12, 'bold'),
                           width=2, bg='#818384', fg='white', relief='raised', borderwidth=1)
            label.pack(side='left', padx=2, pady=2)
            self.alphabet_labels[letter] = label
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#121213')
        input_frame.pack(pady=10)
        
        self.entry = tk.Entry(input_frame, font=('Arial', 18), width=15,
                             justify='center')
        self.entry.pack(side='left', padx=5)
        self.entry.bind('<Return>', lambda e: self.submit_guess())
        
        submit_btn = tk.Button(input_frame, text='Submit', font=('Arial', 14),
                              command=self.submit_guess, bg='#538d4e', fg='white',
                              relief='raised', borderwidth=2, padx=10)
        submit_btn.pack(side='left', padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text=f'Attempt {self.attempt + 1}/{self.MAX_ATTEMPTS}',
                                    font=('Arial', 14), bg='#121213', fg='white')
        self.status_label.pack(pady=10)
        
        # New game button
        new_game_btn = tk.Button(self.root, text='New Game', font=('Arial', 12),
                                command=self.new_game, bg='#818384', fg='white',
                                relief='raised', borderwidth=2, padx=10)
        new_game_btn.pack(pady=5)
        
        self.entry.focus()

    def animate_tile_reveal(self, box, letter, start_color, end_color, delay):
        """Smooth color fade + soft pop animation"""

        def hex_to_rgb(h):
            return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)

        steps = 8

        def animate(step=0):
            if step > steps:
                box.config(relief='solid', borderwidth=2)
                return

            interp = tuple(
                int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * step / steps)
                for i in range(3)
            )

            box.config(
                text=letter.upper(),
                bg=rgb_to_hex(interp),
                fg='white',
                borderwidth=1 if step < steps else 2
            )

            self.root.after(25, animate, step + 1)

        self.root.after(delay, animate)


    def submit_guess(self):
        if self.attempt >= self.MAX_ATTEMPTS:
            return
        
        guess = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)
        
        # Validate guess
        if len(guess) != 5:
            messagebox.showwarning("Invalid", "The word must be exactly 5 letters!")
            return
        
        if guess not in word_list:
            messagebox.showwarning("Invalid", "Word not in dictionary!")
            return
        
        # Get color mapping
        colors = color_mapper(self.word, guess)
        
        self.entry.config(state='disabled')

        for i, (letter, color) in enumerate(zip(guess, colors)):
            box = self.letter_boxes[self.attempt][i]

            if color == 'green':
                target = '#538d4e'
                self.color_map_alphabet[letter] = '#538d4e'
            elif color == 'yellow':
                target = '#b59f3b'
                if self.color_map_alphabet.get(letter) != '#538d4e':
                    self.color_map_alphabet[letter] = '#b59f3b'
            else:
                target = '#3a3a3c'
                self.color_map_alphabet.setdefault(letter, '#3a3a3c')

            self.animate_tile_reveal(
                box=box,
                letter=letter,
                start_color='#3a3a3c',
                end_color=target,
                delay=i * 200
            )

        # re-enable input after animation
        self.root.after(5 * 200 + 250, lambda: self.entry.config(state='normal'))

        # Update alphabet display
        for letter, color in self.color_map_alphabet.items():
            self.alphabet_labels[letter].config(bg=color)
        
        # Check win condition
        if guess == self.word:
            messagebox.showinfo("Congratulations!", f"You won in {self.attempt + 1} attempts!")
            self.entry.config(state='disabled')
            return
        
        self.attempt += 1
        
        # Check lose condition
        if self.attempt >= self.MAX_ATTEMPTS:
            messagebox.showinfo("Game Over", f"The word was: {self.word.upper()}")
            self.entry.config(state='disabled')
        else:
            self.status_label.config(text=f'Attempt {self.attempt + 1}/{self.MAX_ATTEMPTS}')
    
    def new_game(self):
        self.attempt = 0
        self.word = random.choice(word_list_26)
        self.struct = self.converter(self.word)
        self.color_map_alphabet = {}
        
        # Reset board
        for row in self.letter_boxes:
            for box in row:
                box.config(text='', bg='#3a3a3c')
        
        # Reset alphabet
        for label in self.alphabet_labels.values():
            label.config(bg='#818384')
        
        # Reset status and entry
        self.status_label.config(text=f'Attempt {self.attempt + 1}/{self.MAX_ATTEMPTS}')
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()