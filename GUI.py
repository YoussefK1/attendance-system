import tkinter as tk
from tkinter import ttk, messagebox
from capture_images import TakeImages
from train import trainImages
from recognize import TrackImages

# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("1100x800")
root.resizable(False, False)
root.configure(bg="#0f172a")  # dark blue background

# ---------------- Styles ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=12,
                background="#2563eb",
                foreground="white")

style.map("TButton",
          background=[("active", "#1d4ed8")])

style.configure("Title.TLabel",
                font=("Segoe UI", 22, "bold"),
                background="#0f172a",
                foreground="white")

style.configure("Section.TLabel",
                font=("Segoe UI", 14, "bold"),
                background="#ffffff",
                foreground="#0f172a")

style.configure("Card.TFrame",
                background="#ffffff",
                relief="flat")

# ---------------- Functions ----------------
def add_student():
    name = name_entry.get().strip()
    student_id = id_entry.get().strip()

    if not name or not student_id:
        messagebox.showerror("Error", "Please enter both Name and ID")
        return

    TakeImages(name, student_id)
    messagebox.showinfo("Success", f"Images captured for {name}")

    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)


def train_model():
    trainImages()
    messagebox.showinfo("Success", "Model trained successfully")


def recognize_faces():
    TrackImages()

# ---------------- Header ----------------
header = tk.Frame(root, bg="#0f172a")
header.pack(fill="x", pady=15)

# Left: Title
title_frame = tk.Frame(header, bg="#0f172a")
title_frame.pack(side="left", padx=30)

title = ttk.Label(title_frame,
                  text="Face Recognition Attendance System",
                  style="Title.TLabel")
title.pack(anchor="w")

subtitle = tk.Label(title_frame,
                    text="Université Française d’Égypte • Digital Image Processing ",
                    bg="#0f172a",
                    fg="#94a3b8",
                    font=("Segoe UI", 11))
subtitle.pack(anchor="w", pady=5)

# Right: Logo
from PIL import Image, ImageTk

logo_frame = tk.Frame(header, bg="#0f172a")
logo_frame.pack(side="right", padx=30)

try:
    logo_img = Image.open("UFE LOGO NEW.png")
    logo_img = logo_img.resize((240, 120))
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_frame, image=logo, bg="#0f172a")
    logo_label.image = logo
    logo_label.pack()
except Exception as e:
    pass

# ---------------- Main Card ----------------
card = ttk.Frame(root, style="Card.TFrame")
card.pack(padx=60, pady=20, fill="both", expand=True)

# ---- Add Student Section ----
add_frame = tk.Frame(card, bg="#ffffff")
add_frame.pack(pady=30)

section_label = ttk.Label(add_frame,
                          text="Add New Student",
                          style="Section.TLabel")
section_label.grid(row=0, column=0, columnspan=2, pady=15)

# Name
name_label = tk.Label(add_frame,
                      text="Student Name",
                      bg="#ffffff",
                      fg="#334155",
                      font=("Segoe UI", 11))
name_label.grid(row=1, column=0, sticky="e", padx=15, pady=8)

name_entry = ttk.Entry(add_frame, width=35)
name_entry.grid(row=1, column=1, pady=8)

# ID
id_label = tk.Label(add_frame,
                    text="Student ID",
                    bg="#ffffff",
                    fg="#334155",
                    font=("Segoe UI", 11))
id_label.grid(row=2, column=0, sticky="e", padx=15, pady=8)

id_entry = ttk.Entry(add_frame, width=35)
id_entry.grid(row=2, column=1, pady=8)

add_btn = ttk.Button(add_frame,
                     text="📷 Capture Images",
                     command=add_student)
add_btn.grid(row=3, column=0, columnspan=2, pady=20)

# ---- Divider ----
divider = tk.Frame(card, bg="#e5e7eb", height=1)
divider.pack(fill="x", padx=80, pady=10)

# ---- Action Buttons ----
action_frame = tk.Frame(card, bg="#ffffff")
action_frame.pack(pady=20)

train_btn = ttk.Button(action_frame,
                       text="🧠 Train Model",
                       width=30,
                       command=train_model)
train_btn.pack(pady=10)

recognize_btn = ttk.Button(action_frame,
                           text="🎯 Recognize / Take Attendance",
                           width=30,
                           command=recognize_faces)
recognize_btn.pack(pady=10)

# ---- Footer ----
footer = tk.Label(root,
                  text="Press 'q' to close camera windows",
                  bg="#0f172a",
                  fg="#94a3b8",
                  font=("Segoe UI", 10))
footer.pack(pady=10)

root.mainloop()
