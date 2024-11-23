import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import string
import re

def caesar_encrypt(text, shift):
    """Encrypt text using Caesar Cipher with the given shift."""
    result = []
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            result.append(encrypted_char)
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar Cipher with the given shift."""
    return caesar_encrypt(text, -shift)

def caesar_brute_force(ciphertext, top_n=10):
    """Attempt to decrypt Caesar cipher without knowing the key, returning top N candidates."""
    potential_texts = []
    for shift in range(26):
        decrypted_text = caesar_decrypt(ciphertext, shift)
        score = english_score(decrypted_text)
        potential_texts.append((score, shift, decrypted_text))
    # Sort by score in descending order and return top N candidates
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]

def rail_fence_encrypt(text, num_rails):
    """Encrypt text using Rail Fence Cipher with the given number of rails."""
    if num_rails <= 1:
        return text

    rail = ['' for _ in range(num_rails)]
    rail_idx = 0
    direction = 1  # 1: down, -1: up

    for char in text:
        rail[rail_idx] += char
        rail_idx += direction

        if rail_idx == 0 or rail_idx == num_rails - 1:
            direction *= -1

    return ''.join(rail)

def rail_fence_decrypt(ciphertext, key):
    if key == 1:
        return ciphertext

    # Create the rail matrix
    rail = [[None for _ in range(len(ciphertext))] for _ in range(key)]

    # Determine the pattern of positions to fill
    dir_down = None
    row, col = 0, 0

    # First, mark the positions to fill with True
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        elif row == key - 1:
            dir_down = False

        # Place the marker
        rail[row][col] = True  # Mark positions to be filled
        col += 1

        # Move to the next row
        if dir_down:
            row += 1
        else:
            row -= 1

    # Now, fill the rail matrix with the ciphertext
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if rail[i][j] == True:
                rail[i][j] = ciphertext[index]
                index += 1

    # Finally, read the matrix in zig-zag manner to reconstruct the plaintext
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        elif row == key - 1:
            dir_down = False

        # Append the character
        if rail[row][col] is not None:
            result.append(rail[row][col])
            col += 1

        # Move to the next row
        if dir_down:
            row += 1
        else:
            row -= 1

    return ''.join(result)

def rail_fence_brute_force(ciphertext, top_n=10):
    """Attempt to decrypt Rail Fence cipher without knowing the key, returning top N candidates."""
    potential_texts = []
    max_rails = min(20, len(ciphertext) // 2)  # Increased max rails for broader search
    for num_rails in range(2, max_rails + 1):
        decrypted_text = rail_fence_decrypt(ciphertext, num_rails)
        score = english_score(decrypted_text)
        potential_texts.append((score, num_rails, decrypted_text))
    # Sort by score in descending order and return top N candidates
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]

def combined_encrypt(text, shift, num_rails):
    """Encrypt text using Caesar Cipher followed by Rail Fence Cipher."""
    shifted_text = caesar_encrypt(text, shift)
    return rail_fence_encrypt(shifted_text, num_rails)

def combined_decrypt(cipher, shift, num_rails):
    """Decrypt text using Rail Fence Cipher followed by Caesar Cipher."""
    rail_decrypted = rail_fence_decrypt(cipher, num_rails)
    return caesar_decrypt(rail_decrypted, shift)

def combined_brute_force(ciphertext, top_n=10):
    """Attempt to decrypt Combined cipher without knowing the keys, returning top N candidates."""
    potential_texts = []
    for shift in range(26):
        for num_rails in range(2, 30):  # Limit the number of rails to keep computation feasible
            try:
                decrypted_rail = rail_fence_decrypt(ciphertext, num_rails)
                decrypted_text = caesar_decrypt(decrypted_rail, shift)
                score = english_score(decrypted_text)
                potential_texts.append((score, shift, num_rails, decrypted_text))
            except:
                continue
    # Sort by score in descending order and return top N candidates
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]

# Define a comprehensive set of common English words
common_words = set([
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
    'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
    'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
    'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
    'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
    'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
    'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
    'give', 'day', 'most', 'us'
    # You can add more words or use a dictionary file
])

def english_score(text):
    """Score text based on English letter frequency and common words."""
    # Letter frequency scoring
    frequencies = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
        'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
        'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
        'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
        'Q': 0.10, 'Z': 0.07
    }
    text_upper = text.upper()
    text_letters = [c for c in text_upper if c in string.ascii_uppercase]
    if not text_letters:
        letter_score = 0
    else:
        letter_counts = {char: text_letters.count(char) for char in string.ascii_uppercase}
        letter_score = sum(frequencies.get(char, 0) * count for char, count in letter_counts.items())
        letter_score /= len(text_letters)
    
    # Word-based scoring
    words_in_text = re.findall(r'\b\w+\b', text.lower())
    if not words_in_text:
        word_score = 0
    else:
        valid_words = sum(1 for word in words_in_text if word in common_words)
        word_score = valid_words / len(words_in_text)
    
    # Combine the scores
    combined_score = (letter_score * 0.3) + (word_score * 70)  # Adjust weights as needed
    return combined_score

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Application")

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Create frames for better layout
        method_frame = ttk.LabelFrame(self.root, text='Method')
        method_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        options_frame = ttk.LabelFrame(self.root, text='Options')
        options_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        input_frame = ttk.LabelFrame(self.root, text='Input Text')
        input_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        output_frame = ttk.LabelFrame(self.root, text='Output Text')
        output_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        # Method selection
        self.method = tk.StringVar(value='caesar')
        methods = [('Caesar Cipher', 'caesar'), ('Rail Fence Cipher', 'railfence'), ('Combined Cipher', 'combined')]
        for idx, (text, value) in enumerate(methods):
            ttk.Radiobutton(method_frame, text=text, variable=self.method, value=value, command=self.update_options).grid(row=0, column=idx, padx=5, pady=5)

        # Operation selection
        self.operation = tk.StringVar(value='encrypt')
        ttk.Radiobutton(options_frame, text='Encrypt', variable=self.operation, value='encrypt', command=self.update_options).grid(row=0, column=0, padx=5, pady=5)
        ttk.Radiobutton(options_frame, text='Decrypt', variable=self.operation, value='decrypt', command=self.update_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(options_frame, text='Cryptanalysis', variable=self.operation, value='cryptanalysis', command=self.update_options).grid(row=0, column=2, padx=5, pady=5)

        # Parameters
        self.shift_label = ttk.Label(options_frame, text='Shift:')
        self.shift_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.shift_entry = ttk.Entry(options_frame)
        self.shift_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.shift_entry.insert(0, '3')

        self.rails_label = ttk.Label(options_frame, text='Rails:')
        self.rails_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.rails_entry = ttk.Entry(options_frame)
        self.rails_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.rails_entry.insert(0, '3')

        # Input Text
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=80, height=10)
        self.input_text.grid(row=0, column=0, padx=5, pady=5)

        # Output Text (using Notebook for multiple tabs)
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.grid(row=0, column=0, padx=5, pady=5)

        # Action Buttons
        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=4, column=0, padx=10, pady=10)
        self.run_button = ttk.Button(action_frame, text='Run', command=self.run_cipher)
        self.run_button.grid(row=0, column=0, padx=5)
        self.clear_button = ttk.Button(action_frame, text='Clear', command=self.clear_text)
        self.clear_button.grid(row=0, column=1, padx=5)
        self.quit_button = ttk.Button(action_frame, text='Quit', command=self.root.quit)
        self.quit_button.grid(row=0, column=2, padx=5)

        # Adjust options based on selected method and operation
        self.update_options()

    def update_options(self):
        method = self.method.get()
        operation = self.operation.get()
        if operation == 'cryptanalysis':
            # Disable shift and rails input
            self.shift_label.config(state='disabled')
            self.shift_entry.config(state='disabled')
            self.rails_label.config(state='disabled')
            self.rails_entry.config(state='disabled')
        else:
            # Enable/disable based on method
            if method == 'caesar':
                # Enable shift, disable rails
                self.shift_label.config(state='normal')
                self.shift_entry.config(state='normal')
                self.rails_label.config(state='disabled')
                self.rails_entry.config(state='disabled')
            elif method == 'railfence':
                # Disable shift, enable rails
                self.shift_label.config(state='disabled')
                self.shift_entry.config(state='disabled')
                self.rails_label.config(state='normal')
                self.rails_entry.config(state='normal')
            elif method == 'combined':
                # Enable both shift and rails
                self.shift_label.config(state='normal')
                self.shift_entry.config(state='normal')
                self.rails_label.config(state='normal')
                self.rails_entry.config(state='normal')

    def run_cipher(self):
        method = self.method.get()
        operation = self.operation.get()
        input_text = self.input_text.get('1.0', tk.END).strip()

        if not input_text:
            messagebox.showwarning('Input Required', 'Please enter some text.')
            return

        # Enforce minimum length for plaintext in encryption
        if operation == 'encrypt' and len(input_text) < 1000:
            messagebox.showwarning('Input Too Short', 'Please enter at least 1000 characters for encryption.')
            return

        # Default values
        shift = 3
        rails = 3

        # Get shift and rails values
        if operation != 'cryptanalysis':
            if method in ['caesar', 'combined']:
                try:
                    shift = int(self.shift_entry.get())
                except ValueError:
                    messagebox.showerror('Invalid Shift Value', 'Please enter a valid integer for shift.')
                    return
            if method in ['railfence', 'combined']:
                try:
                    rails = int(self.rails_entry.get())
                except ValueError:
                    messagebox.showerror('Invalid Rails Value', 'Please enter a valid integer for rails.')
                    return

        # Perform operation
        try:
            if operation == 'encrypt':
                if method == 'caesar':
                    result = caesar_encrypt(input_text, shift)
                elif method == 'railfence':
                    result = rail_fence_encrypt(input_text, rails)
                elif method == 'combined':
                    result = combined_encrypt(input_text, shift, rails)
                # Display the result in a single tab
                self.display_single_result(result)
            elif operation == 'decrypt':
                if method == 'caesar':
                    result = caesar_decrypt(input_text, shift)
                elif method == 'railfence':
                    result = rail_fence_decrypt(input_text, rails)
                elif method == 'combined':
                    result = combined_decrypt(input_text, shift, rails)
                # Display the result in a single tab
                self.display_single_result(result)
            elif operation == 'cryptanalysis':
                if method == 'caesar':
                    candidates = caesar_brute_force(input_text, top_n=10)
                    self.display_multiple_results(candidates, method)
                elif method == 'railfence':
                    candidates = rail_fence_brute_force(input_text, top_n=10)
                    self.display_multiple_results(candidates, method)
                elif method == 'combined':
                    candidates = combined_brute_force(input_text, top_n=10)
                    self.display_multiple_results(candidates, method)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

    def display_single_result(self, result):
        # Clear previous tabs
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)
        # Create a new tab for the result
        tab = ttk.Frame(self.output_notebook)
        self.output_notebook.add(tab, text='Result')
        output_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=80, height=10)
        output_text.pack(fill='both', expand=True)
        output_text.insert(tk.END, result)

    def display_multiple_results(self, candidates, method):
        # Clear previous tabs
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)
        # Create tabs for each candidate
        for idx, candidate in enumerate(candidates):
            tab = ttk.Frame(self.output_notebook)
            if method == 'caesar':
                score, shift, decrypted_text = candidate
                title = f'Key: Shift={shift}'
            elif method == 'railfence':
                score, rails, decrypted_text = candidate
                title = f'Key: Rails={rails}'
            elif method == 'combined':
                score, shift, rails, decrypted_text = candidate
                title = f'Keys: Shift={shift}, Rails={rails}'
            else:
                title = f'Candidate {idx+1}'
            self.output_notebook.add(tab, text=title)
            output_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=80, height=10)
            output_text.pack(fill='both', expand=True)
            output_text.insert(tk.END, decrypted_text)

    def clear_text(self):
        self.input_text.delete('1.0', tk.END)
        # Clear output tabs
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)

if __name__ == '__main__':
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
