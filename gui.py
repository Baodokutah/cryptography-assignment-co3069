import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

from ciphers import CaesarCipher, RailFenceCipher, CombinedCipher
from cryptanalysis import caesar_brute_force, rail_fence_brute_force, combined_brute_force

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crytool69")

        self.create_widgets()

    def create_widgets(self):
        method_frame = ttk.LabelFrame(self.root, text='Method')
        method_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        options_frame = ttk.LabelFrame(self.root, text='Options')
        options_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        input_frame = ttk.LabelFrame(self.root, text='Input Text')
        input_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        output_frame = ttk.LabelFrame(self.root, text='Output Text')
        output_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        self.method = tk.StringVar(value='caesar')
        methods = [
            ('Caesar Cipher', 'caesar'),
            ('Rail Fence Cipher', 'railfence'),
            ('Combined Cipher', 'combined')
        ]
        for idx, (text, value) in enumerate(methods):
            ttk.Radiobutton(
                method_frame,
                text=text,
                variable=self.method,
                value=value,
                command=self.update_options
            ).grid(row=0, column=idx, padx=5, pady=5)

        self.operation = tk.StringVar(value='encrypt')
        ttk.Radiobutton(
            options_frame,
            text='Encrypt',
            variable=self.operation,
            value='encrypt',
            command=self.update_options
        ).grid(row=0, column=0, padx=5, pady=5)
        ttk.Radiobutton(
            options_frame,
            text='Decrypt',
            variable=self.operation,
            value='decrypt',
            command=self.update_options
        ).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(
            options_frame,
            text='Cryptanalysis',
            variable=self.operation,
            value='cryptanalysis',
            command=self.update_options
        ).grid(row=0, column=2, padx=5, pady=5)

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

        self.input_text = scrolledtext.ScrolledText(
            input_frame, wrap=tk.WORD, width=80, height=10
        )
        self.input_text.grid(row=0, column=0, padx=5, pady=5)

        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.grid(row=0, column=0, padx=5, pady=5)

        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=4, column=0, padx=10, pady=10)
        self.run_button = ttk.Button(
            action_frame, text='Run', command=self.run_cipher
        )
        self.run_button.grid(row=0, column=0, padx=5)
        self.clear_button = ttk.Button(
            action_frame, text='Clear', command=self.clear_text
        )
        self.clear_button.grid(row=0, column=1, padx=5)
        self.quit_button = ttk.Button(
            action_frame, text='Quit', command=self.root.quit
        )
        self.quit_button.grid(row=0, column=2, padx=5)

        self.update_options()

    def update_options(self):
        method = self.method.get()
        operation = self.operation.get()
        if operation == 'cryptanalysis':
            self.shift_label.config(state='disabled')
            self.shift_entry.config(state='disabled')
            self.rails_label.config(state='disabled')
            self.rails_entry.config(state='disabled')
        else:
            if method == 'caesar':
                self.shift_label.config(state='normal')
                self.shift_entry.config(state='normal')
                self.rails_label.config(state='disabled')
                self.rails_entry.config(state='disabled')
            elif method == 'railfence':
                self.shift_label.config(state='disabled')
                self.shift_entry.config(state='disabled')
                self.rails_label.config(state='normal')
                self.rails_entry.config(state='normal')
            elif method == 'combined':
                self.shift_label.config(state='normal')
                self.shift_entry.config(state='normal')
                self.rails_label.config(state='normal')
                self.rails_entry.config(state='normal')

    def run_cipher(self):
        method = self.method.get()
        operation = self.operation.get()
        input_text = self.input_text.get('1.0', tk.END).strip('\n')

        if not input_text:
            messagebox.showwarning('Input Required', 'Please enter some text.')
            return

        if operation == 'encrypt' and len(input_text) < 1000:
            messagebox.showwarning(
                'Input Too Short',
                'Please enter at least 1000 characters for encryption.'
            )
            return

        shift = 3
        rails = 3

        if operation != 'cryptanalysis':
            if method in ['caesar', 'combined']:
                try:
                    shift = int(self.shift_entry.get())
                except ValueError:
                    messagebox.showerror(
                        'Invalid Shift Value',
                        'Please enter a valid integer for shift.'
                    )
                    return
            if method in ['railfence', 'combined']:
                try:
                    rails = int(self.rails_entry.get())
                except ValueError:
                    messagebox.showerror(
                        'Invalid Rails Value',
                        'Please enter a valid integer for rails.'
                    )
                    return

        try:
            if operation == 'encrypt':
                if method == 'caesar':
                    cipher = CaesarCipher(shift)
                elif method == 'railfence':
                    cipher = RailFenceCipher(rails)
                elif method == 'combined':
                    cipher = CombinedCipher(shift, rails)
                result = cipher.encrypt(input_text)
                self.display_single_result(result)
            elif operation == 'decrypt':
                if method == 'caesar':
                    cipher = CaesarCipher(shift)
                elif method == 'railfence':
                    cipher = RailFenceCipher(rails)
                elif method == 'combined':
                    cipher = CombinedCipher(shift, rails)
                result = cipher.decrypt(input_text)
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
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)
        tab = ttk.Frame(self.output_notebook)
        self.output_notebook.add(tab, text='Result')
        output_text = scrolledtext.ScrolledText(
            tab, wrap=tk.WORD, width=80, height=10
        )
        output_text.pack(fill='both', expand=True)
        output_text.insert(tk.END, result)

    def display_multiple_results(self, candidates, method):
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)
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
            output_text = scrolledtext.ScrolledText(
                tab, wrap=tk.WORD, width=80, height=10
            )
            output_text.pack(fill='both', expand=True)
            output_text.insert(tk.END, decrypted_text)

    def clear_text(self):
        self.input_text.delete('1.0', tk.END)
        for tab in self.output_notebook.tabs():
            self.output_notebook.forget(tab)
