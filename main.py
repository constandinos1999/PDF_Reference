import tkinter as tk
from tkinter import filedialog, messagebox
from extractor import process_pdf
from gui import launch_gui

if __name__ == "__main__":
    launch_gui()  # Start the GUI

class PDFReferenceExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reference Extractor")
        self.root.geometry("500x300")

        self.label = tk.Label(root, text="Select a PDF File:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Browse", command=self.select_pdf, font=("Arial", 10))
        self.select_button.pack(pady=5)

        self.play_button = tk.Button(root, text="Play ▶", command=self.run_extraction, font=("Arial", 12, "bold"), bg="green", fg="white")
        self.play_button.pack(pady=10)

        self.result_text = tk.Text(root, height=8, width=50, wrap="word")
        self.result_text.pack(pady=10)

        self.pdf_path = None

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path = file_path
            self.label.config(text=f"Selected: {file_path.split('/')[-1]}")

    def run_extraction(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        self.result_text.delete("1.0", tk.END)  # Clear previous results
        self.result_text.insert(tk.END, "Extracting references...\n")

        results = process_pdf(self.pdf_path)

        if not results:
            self.result_text.insert(tk.END, "No references found.\n")
        else:
            for ref, data in results.items():
                status = data.get("status", "N/A")
                service = data.get("service", "Unknown")
                self.result_text.insert(tk.END, f"{ref} - {service} ({status})\n")

        messagebox.showinfo("Done", "Extraction Completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReferenceExtractorApp(root)
    root.mainloop()
