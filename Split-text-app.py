import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pyperclip
import re
import os


# ctk.set_appearance_mode("dark")

class TextProcessor:
    @staticmethod
    def split_text_into_chunks(text, max_tokens):
        sentences = re.split(r'(?<=[.])\s+', text)
        chunks, chunk, token_count = [], [], 0
        for sentence in sentences:
            tokens = sentence.split()
            if token_count + len(tokens) > max_tokens:
                chunks.append(' '.join(chunk))
                chunk, token_count = [sentence], len(tokens)
            else:
                chunk.append(sentence)
                token_count += len(tokens)
        chunks.append(' '.join(chunk))
        return chunks


class TextFileReader(tk.Tk):
    # blue_highlight_nightowl = "#084d81"



    def __init__(self, blue_highlight_nightowl="#084d81", canvas_color="#011627", light_cream="#e8dcb6"):
        super().__init__()
        self.title("Text File Reader")
        self.geometry("700x1600")
        self.configure(bg=canvas_color)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.select_and_copy_button = ctk.CTkButton(self, text="Select and Copy Text", command=self.select_and_copy_text, fg_color=blue_highlight_nightowl, text_color="white")
        self.select_and_copy_button.grid(row=2, column=0, pady=10)
        # self.copy_button = ctk.CTkButton(self, text="Copy Selected Text", command=self.copy_text, fg_color=blue_highlight_nightowl, text_color="white")
        # self.copy_button.grid(row=2, column=0, pady=10)
        self.open_file_button = ctk.CTkButton(self, text="Open File", command=self.open_file, fg_color= blue_highlight_nightowl, text_color="white")
        self.open_file_button.grid(row=0, column=2, pady=10)
        # self.select_all_button = ctk.CTkButton(self, text="Select All Text", command=self.select_all_text, fg_color= blue_highlight_nightowl, text_color="white")
        # self.select_all_button.grid(row=1, column=0, pady=10)

        self.max_tokens = 2000  # Default value
        self.max_tokens_entry = ctk.CTkEntry(self)
        self.max_tokens_entry.insert(0, str(self.max_tokens))
        self.max_tokens_entry.grid(row=1, column=1, pady=10)
        self.save_max_tokens_button = ctk.CTkButton(self, text="Save Max Tokens", command=self.save_max_tokens, fg_color= blue_highlight_nightowl, text_color="white")
        self.save_max_tokens_button.grid(row=2, column=1, pady=10)

        self.file_label = ctk.CTkLabel(self, text="No file selected", text_color="white")
        self.file_label.grid(row=1, column=2, columnspan=1, pady=10)
        self.token_count_label = ctk.CTkLabel(self, text="Token count: 0", text_color="white")
        self.token_count_label.grid(row=2, column=2, columnspan=1, pady=10)

        self.scroll_frame = tk.Frame(self, bg=light_cream)
        self.scroll_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.scroll_frame.grid_rowconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scrollbar = tk.Scrollbar(self.scroll_frame, bg=light_cream)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(self.scroll_frame, yscrollcommand=self.scrollbar.set, bg= canvas_color)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)
        self.text_frame = tk.Frame(self.canvas, bg=canvas_color)
        self.canvas.create_window((0, 0), window=self.text_frame, anchor="nw")
        self.text_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.text_fields = []

        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(1, weight=1)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def save_max_tokens(self):
        try:
            self.max_tokens = int(self.max_tokens_entry.get())
            messagebox.showinfo("Success", "Max tokens value saved")
        except ValueError:
            messagebox.showerror("Error", "Invalid max tokens value")

    def open_file(self, yellow_text="#ecc48d", text_field_color="#011627"):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            filename = os.path.basename(file_path)
            self.file_label.configure(text=filename)
            try:
                with open(file_path, "r", encoding='utf-8') as file:
                    text = file.read()
                    chunks = TextProcessor.split_text_into_chunks(text, self.max_tokens)
                    for text_field in self.text_fields:
                        text_field.destroy()
                    self.text_fields = []
                    for i, chunk in enumerate(chunks):
                        label = tk.Label(self.text_frame, text=f"Textbox {i + 1}", font=("Arial", 14))
                        label.grid(row=2 * i, column=0, sticky="w")

                        text_field = tk.Text(self.text_frame, bg= text_field_color, fg=yellow_text, font=("Sans Serif", 10))
                        scrollbar = tk.Scrollbar(self.text_frame, command=text_field.yview)
                        text_field['yscrollcommand'] = scrollbar.set

                        text_field.grid(row=2 * i + 1, column=0, pady=10, padx=10, sticky="nsew")  # Added padx for margin
                        text_field.insert(tk.END, chunk)
                        self.text_fields.append(text_field)
                        self.text_frame.grid_columnconfigure(0, weight=1)
                        self.text_frame.grid_rowconfigure(2 * i + 1, weight=1)
                        text_field.grid_propagate(False)

                        scrollbar.grid(row=2 * i + 1, column=1, pady=10, padx=10, sticky="nsew")

                    self.token_count_label.configure(text=f"Token count: {sum(len(chunk.split()) for chunk in chunks)}")
            except UnicodeDecodeError:
                messagebox.showerror("Error", "Unable to open file: unsupported character found")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def select_and_copy_text(self):
        focused_widget = self.focus_get()
        if isinstance(focused_widget, tk.Text):
            focused_widget.tag_add(tk.SEL, "1.0", tk.END)
            focused_widget.mark_set(tk.INSERT, "1.0")
            focused_widget.see(tk.INSERT)

            try:
                selected_text = focused_widget.selection_get()
                pyperclip.copy(selected_text)
                messagebox.showinfo("Success", "Text copied to clipboard")

            except tk.TclError:
                messagebox.showerror("Error", "No text selected")


if __name__ == "__main__":
    app = TextFileReader()
    app.mainloop()
