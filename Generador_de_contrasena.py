import random
import tkinter as tk
from tkinter import messagebox


# Character pools (letters, numbers, symbols)
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# Store the last valid setting for Regenerate
last_settings = {"letters": None, "numbers": None, "symbols": None}

def build_password(nr_letters, nr_numbers, nr_symbols):
    """Build a password using the given counts"""
    # Create a list of random characters
    password_list = []

    # Add random letters
    for _ in range(nr_letters):
        password_list.append(random.choice(letters))

    # Add random numbers
    for _ in range(nr_numbers):
        password_list.append(random.choice(numbers))

    # Add random symbols
    for _ in range(nr_symbols):
        password_list.append(random.choice(symbols))

    # Shuffle to mix all characters
    random.shuffle(password_list)

    # Convert list into a string
    return "".join(password_list)

def read_inputs():
    """Read and validate the input fields. Return (letters, numbers, symbols) or none if invalid"""
    try:
        nr_letters = int(entry_letters.get())
        nr_symbols = int(entry_symbols.get())
        nr_numbers = int(entry_numbers.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese solo números")
        return None

    # Enforce minimum 1 of each type
    if nr_letters < 1 or nr_numbers < 1 or nr_symbols < 1:
        messagebox.showerror("Error", "Debes poner mínimo 1 letra, un símbolo y un número.")
        return None
    return nr_letters, nr_numbers, nr_symbols

def generate_password():
    """Generate password using current input fields"""
    values = read_inputs()
    if values is None:
        return
    nr_letters, nr_numbers, nr_symbols = values

    #Save settings for Regenerate
    last_settings["letters"] = nr_letters
    last_settings["numbers"] = nr_numbers
    last_settings["symbols"] = nr_symbols

    password = build_password(nr_letters, nr_numbers, nr_symbols)
    result_var.set(password)


def regenerate_password():
    """Regenerate password using last valid settings (without rereading inputs)"""
    # If we don't have saved settings yet, just regenerate normally
    if last_settings["letters"] is None:
        generate_password()
        return

    password = build_password(
        last_settings["letters"],
        last_settings["numbers"],
        last_settings["symbols"]
    )
    result_var.set(password)


def copy_password():
    """Copy the generated password to clipboard"""
    pwd = result_var.get()
    if not pwd:
        messagebox.showinfo("Copiar", "Generar una contraseña primero.")
        return

    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copiar", "Contraseña copiada.")

# GUI setup
root = tk.Tk()
root.title("Generador de Contraseñas")
root.resizable(False, False)
root.geometry("460x270")

title = tk.Label(root, text="¡Bienvenido al Generador de Contraseñas!", font=("Arial", 12, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

# Inputs
tk.Label(frame, text= "Letras:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
entry_letters = tk.Entry(frame, width=10)
entry_letters.grid(row=0, column=1, padx=6, pady=6)
entry_letters.insert(0, "8")

tk.Label(frame, text="Símbolos:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
entry_symbols = tk.Entry(frame, width=10)
entry_symbols.grid(row=1, column=1, padx=6, pady=6)
entry_symbols.insert(0, "2")

tk.Label(frame, text="Números:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
entry_numbers = tk.Entry(frame, width=10)
entry_numbers.grid(row=2, column=1, padx=6, pady=6)
entry_numbers.insert(0, "2")

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Generar", width=14, command=generate_password).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Regenerar", width=14, command=regenerate_password).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Copiar", width=14, command=copy_password).grid(row=0, column=2, padx=6)

# Result field
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, width=50, justify="center")
result_entry.pack(pady=8)

info = tk.Label(root, text="(Mínimo: 1 letra, 1 símbolo y 1 número)", font=("Arial", 9))
info.pack(pady=3)

root.mainloop()
