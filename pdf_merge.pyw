import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfWriter, PdfReader
import os

# Create the Tkinter window
root = tk.Tk()
root.title("PDF Merger")
root.geometry("400x300")

def open_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    listbox.delete(0, tk.END)
    for path in file_paths:
        filename = os.path.basename(path)  # Extract the filename
        listbox.insert(tk.END, filename)

open_files_button = tk.Button(root, text="Select PDFs", command=open_files)
open_files_button.pack(pady=10)

# Frame for listbox and buttons
frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=10)
listbox.grid(row=0, column=0, rowspan=2)

scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.grid(row=0, column=1, rowspan=2, sticky='ns')
listbox['yscrollcommand'] = scrollbar.set

def move_up():
    pos = listbox.curselection()
    if pos and pos[0] > 0:
        text = listbox.get(pos[0])
        listbox.delete(pos[0])
        listbox.insert(pos[0] - 1, text)
        listbox.select_set(pos[0] - 1)

def move_down():
    pos = listbox.curselection()
    if pos and pos[0] < listbox.size() - 1:
        text = listbox.get(pos[0])
        listbox.delete(pos[0])
        listbox.insert(pos[0] + 1, text)
        listbox.select_set(pos[0] + 1)

up_button = tk.Button(frame, text="Up", command=move_up)
up_button.grid(row=0, column=2, padx=5, sticky='ew')

down_button = tk.Button(frame, text="Down", command=move_down)
down_button.grid(row=1, column=2, padx=5, sticky='ew')

def merge_pdfs():
    pdf_writer = PdfWriter()
    for file in listbox.get(0, tk.END):
        pdf_reader = PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    output_filename = "merged_document.pdf"
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)

    messagebox.showinfo("Done", f"PDFs merged! Saved as {output_filename}")

merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
merge_button.pack(pady=10)

root.mainloop()
