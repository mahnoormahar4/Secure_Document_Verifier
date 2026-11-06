import tkinter as tk
from tkinter import filedialog, messagebox
import os

from hashing import generate_hash
from database import (
    save_hash,
    get_hash,
    save_history,
    get_history,
    clear_history
)

# -----------------------------
# Supported File Types
# -----------------------------
SUPPORTED_FILE_TYPES = [
    ("Supported Files", "*.txt *.pdf *.docx *.png *.jpg *.jpeg"),
    ("Text Files", "*.txt"),
    ("PDF Files", "*.pdf"),
    ("Word Files", "*.docx"),
    ("PNG Images", "*.png"),
    ("JPG Images", "*.jpg"),
    ("JPEG Images", "*.jpeg"),
    ("All Files", "*.*")
]


# -----------------------------
# Validate File Type
# -----------------------------
def is_valid_file(file_path):
    valid_extensions = (".txt", ".pdf", ".docx", ".png", ".jpg", ".jpeg")
    return file_path.lower().endswith(valid_extensions)


# -----------------------------
# Upload Original File
# -----------------------------
def upload_original():

    file_path = filedialog.askopenfilename(filetypes=SUPPORTED_FILE_TYPES)

    if not file_path:
        return

    if not is_valid_file(file_path):
        messagebox.showerror("Invalid File", "Unsupported file type selected.")
        return

    file_name = os.path.basename(file_path)

    hash_value = generate_hash(file_path)

    save_hash(file_name, hash_value)

    file_size = os.path.getsize(file_path)

    file_name_value.config(text=file_name)
    file_size_value.config(text=f"{file_size} bytes")
    hash_value_label.config(text=hash_value)

    status_label.config(
        text="Original file hash saved successfully ✔",
        fg="green"
    )


# -----------------------------
# Verify File
# -----------------------------
def verify_file():

    file_path = filedialog.askopenfilename(filetypes=SUPPORTED_FILE_TYPES)

    if not file_path:
        return

    if not is_valid_file(file_path):
        messagebox.showerror("Invalid File", "Unsupported file type selected.")
        return

    file_name = os.path.basename(file_path)

    new_hash = generate_hash(file_path)
    stored_hash = get_hash(file_name)

    file_size = os.path.getsize(file_path)

    file_name_value.config(text=file_name)
    file_size_value.config(text=f"{file_size} bytes")
    hash_value_label.config(text=new_hash)

    if stored_hash is None:

        messagebox.showwarning("Not Found", "No original hash found for this file.")

        status_label.config(text="No stored hash found ⚠", fg="orange")

        return

    if new_hash == stored_hash:

        save_history(file_name, "ORIGINAL")

        messagebox.showinfo("Verification Result", "File is ORIGINAL ✔")

        status_label.config(text="Verification Successful ✔", fg="green")

    else:

        save_history(file_name, "MODIFIED")

        messagebox.showerror("Verification Result", "File has been MODIFIED ❌")

        status_label.config(text="File Integrity Compromised ❌", fg="red")

    update_history_box()


# -----------------------------
# Update History Box
# -----------------------------
def update_history_box():

    history_box.delete(0, tk.END)

    for record in get_history():
        file_name, result, timestamp = record
        history_box.insert(tk.END, f"{timestamp} | {file_name} | {result}")


# -----------------------------
# Clear History
# -----------------------------
def clear_history_box():

    confirm = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to clear verification history?"
    )

    if confirm:
        clear_history()
        update_history_box()
        status_label.config(text="Verification history cleared", fg="blue")


# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Secure Document Verification")
root.geometry("750x650")
root.configure(bg="#f4f4f4")


# Title
tk.Label(
    root,
    text="Secure Document Verification using SHA-256",
    font=("Arial", 18, "bold"),
    bg="#f4f4f4",
    fg="#222"
).pack(pady=20)


# Buttons Frame
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Upload Original File",
    width=22,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=upload_original
).grid(row=0, column=0, padx=10)


tk.Button(
    button_frame,
    text="Verify File",
    width=22,
    height=2,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold"),
    command=verify_file
).grid(row=0, column=1, padx=10)


# File Details Section
details_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
details_frame.pack(pady=20, padx=20, fill="both")


tk.Label(details_frame, text="File Details",
         font=("Arial", 14, "bold"), bg="white").pack(pady=10)


tk.Label(details_frame, text="File Name:",
         font=("Arial", 11, "bold"), bg="white").pack(anchor="w", padx=20)

file_name_value = tk.Label(details_frame, text="No file selected",
                           font=("Arial", 11), bg="white")
file_name_value.pack(anchor="w", padx=40, pady=5)


tk.Label(details_frame, text="File Size:",
         font=("Arial", 11, "bold"), bg="white").pack(anchor="w", padx=20)

file_size_value = tk.Label(details_frame, text="-",
                           font=("Arial", 11), bg="white")
file_size_value.pack(anchor="w", padx=40, pady=5)


tk.Label(details_frame, text="SHA-256 Hash:",
         font=("Arial", 11, "bold"), bg="white").pack(anchor="w", padx=20)

hash_value_label = tk.Label(
    details_frame,
    text="-",
    font=("Arial", 9),
    bg="white",
    wraplength=650,
    justify="left"
)
hash_value_label.pack(anchor="w", padx=40, pady=5)


# History Section
history_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
history_frame.pack(pady=10, padx=20, fill="both", expand=True)


tk.Label(history_frame, text="Verification History",
         font=("Arial", 13, "bold"), bg="white").pack(pady=10)


history_container = tk.Frame(history_frame, bg="white")
history_container.pack(fill="both", expand=True, padx=10, pady=10)


scrollbar = tk.Scrollbar(history_container)
scrollbar.pack(side="right", fill="y")


history_box = tk.Listbox(
    history_container,
    font=("Arial", 10),
    yscrollcommand=scrollbar.set
)

history_box.pack(side="left", fill="both", expand=True)

scrollbar.config(command=history_box.yview)


tk.Button(
    history_frame,
    text="Clear History",
    bg="#E53935",
    fg="white",
    font=("Arial", 10, "bold"),
    command=clear_history_box
).pack(pady=5)


update_history_box()


# Status Label
status_label = tk.Label(
    root,
    text="Waiting for file upload...",
    font=("Arial", 12, "bold"),
    bg="#f4f4f4"
)
status_label.pack(pady=15)


# Run App
root.mainloop()