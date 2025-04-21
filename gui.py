import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from extractor import process_pdf

class PDFReferenceExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 PDF Reference Extractor")
        self.root.geometry("700x550")
        self.root.minsize(500, 400)

        # Theme colors
        self.dark_mode = False
        self.light_bg = "#E3F2FD"  # Light Blue
        self.dark_bg = "#263238"  # Dark Gray-Blue
        self.light_fg = "#000000"
        self.dark_fg = "#FFFFFF"
        self.primary_color = "#0277BD"  # Deep Blue
        self.accent_color = "#FF7043"  # Orange Accent

        self.root.configure(bg=self.light_bg)

        # Header Frame with Gradient
        self.header_frame = tk.Frame(root, bg=self.primary_color, height=80)
        self.header_frame.pack(fill="x")

        self.label_title = tk.Label(
            root, text="📄 PDF Reference Extractor", font=("Arial", 20, "bold"),
            fg="white", bg=self.primary_color
        )
        self.label_title.place(x=200, y=20)

        # Dark Mode Toggle
        self.toggle_button = ttk.Button(root, text="🌙 Dark Mode", command=self.toggle_theme)
        self.toggle_button.place(x=600, y=30)

        # File Selection Button
        self.select_button = ttk.Button(root, text="📂 Browse PDF", command=self.select_pdf, style="Custom.TButton")
        self.select_button.pack(pady=20)

        # File Label (Ensure text is visible)
        self.file_label = tk.Label(root, text="No file selected", font=("Arial", 11), bg=self.light_bg, fg=self.light_fg)
        self.file_label.pack()

        # Extract Button (Ensure it is enabled and text is visible)
        self.extract_button = ttk.Button(root, text="🔍 Extract References", command=self.run_extraction, style="Accent.TButton")
        self.extract_button.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
        self.progress.pack(pady=10)

        # Results Box with Scroll (Ensure text is visible)
        self.result_frame = ttk.Frame(root, relief="groove", borderwidth=2)
        self.result_frame.pack(pady=10, fill="both", expand=True)

        self.result_scroll = ttk.Scrollbar(self.result_frame)
        self.result_scroll.pack(side="right", fill="y")

        self.result_text = tk.Text(self.result_frame, height=10, width=70, wrap="word", state="disabled",
                                   font=("Arial", 11), bg="white", fg="black", yscrollcommand=self.result_scroll.set)
        self.result_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.result_scroll.config(command=self.result_text.yview)

        self.pdf_path = None

        # Apply Styles
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", font=("Arial", 12), padding=6, foreground="black", background=self.primary_color)
        self.style.map("Custom.TButton", background=[("active", "#01579B")])

        self.style.configure("Accent.TButton", font=("Arial", 12), padding=6, foreground="black", background=self.accent_color)
        self.style.map("Accent.TButton", background=[("active", "#E64A19")])

    def toggle_theme(self):
        """Switch between Dark and Light mode"""
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.root.configure(bg=self.dark_bg)
            self.label_title.config(bg=self.dark_bg, fg=self.dark_fg)
            self.file_label.config(bg=self.dark_bg, fg=self.dark_fg)
            self.result_text.config(bg="#37474F", fg="white")
            self.toggle_button.config(text="☀️ Light Mode", foreground="white")
        else:
            self.root.configure(bg=self.light_bg)
            self.label_title.config(bg=self.primary_color, fg="white")
            self.file_label.config(bg=self.light_bg, fg=self.light_fg)
            self.result_text.config(bg="white", fg="black")
            self.toggle_button.config(text="🌙 Dark Mode", foreground="black")

    def select_pdf(self):
        """Opens a file dialog to select a PDF file."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path = file_path
            self.file_label.config(text=f"📄 Selected: {file_path.split('/')[-1]}")

    def run_extraction(self):
        """Handles extraction in a separate thread."""
        if not self.pdf_path:
            messagebox.showerror("⚠️ Error", "Please select a PDF file first.")
            return

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "🔄 Extracting references...\n")
        self.result_text.config(state="disabled")

        self.progress.start()
        threading.Thread(target=self.process_extraction, daemon=True).start()

    def process_extraction(self):
        """Extracts references and updates the UI."""
        results = process_pdf(self.pdf_path)
        self.progress.stop()

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        if not results:
            self.result_text.insert(tk.END, "⚠️ No references found.\n")
        else:
            for ref, data in results.items():
                status = data.get("status", "N/A")
                service = data.get("service", "Unknown")
                self.result_text.insert(tk.END, f"✅ {ref} - {service} ({status})\n")

        self.result_text.config(state="disabled")
        messagebox.showinfo("✅ Done", "Extraction Completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReferenceExtractorApp(root)
    root.mainloop()
