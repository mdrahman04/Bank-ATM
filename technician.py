import tkinter as tk
from tkinter import ttk
import json


def show_technician_view(root):
    def verify_password():
        entered_password = password_entry.get()
        if entered_password == "67890":
            password_prompt_frame.pack_forget()
            display_technician_view(root)
        else:
            password_entry.delete(0, tk.END)
            password_entry.focus()
            message_label.config(text="Incorrect password", foreground="red")

    password_prompt_frame = ttk.Frame(root)
    password_prompt_frame.pack(padx=20, pady=0)

    ttk.Label(password_prompt_frame, text="Enter Technician Password: # 67890", font=("", 9, "bold"),
              foreground="orange").pack(pady=10)
    password_entry = ttk.Entry(password_prompt_frame, show="*")
    password_entry.pack(pady=5)

    submit_button = ttk.Button(password_prompt_frame, text="Submit", command=verify_password)
    submit_button.pack(pady=10)
    submit_button.bind("<Return>", lambda event=None: submit_button.invoke())

    message_label = ttk.Label(password_prompt_frame, text="")
    message_label.pack()


def display_technician_view(root):
    def update_ink_count():
        try:
            amount = float(ink_count_entry.get())
            current_ink = system_data.get("ink_available", 0.00)

            total_ink = current_ink + amount

            if total_ink <= 500:
                system_data["ink_available"] = total_ink
                with open("system.json", "w") as system_file:
                    json.dump(system_data, system_file, indent=4)

                available_ink_label.config(text=f"Ink Available: {total_ink:.2f} ml")
                ink_count_entry.set("")
            else:
                message_label.config(text="Ink capacity exceeded (500 ml).")
        except ValueError:
            message_label.config(text="Invalid input. Please enter a valid number.")

    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=0)

    label = ttk.Label(frame, text="Technician View", font=("", 10, "bold"), foreground="orange")
    label.pack()

    try:
        with open("system.json", "r") as system_file:
            system_data = json.load(system_file)
    except FileNotFoundError:
        system_data = {"money_count": 0.00, "ink_available": 0.00}

    ink_count_entry = tk.StringVar()
    available_ink_label = ttk.Label(frame, text=f"Ink Available: {system_data.get('ink_available', 0.00):.2f} ml",
                                    foreground="red", font=("", 10, "bold"))
    available_ink_label.pack(pady=10)

    ttk.Label(frame, text="Enter Ink Count (ml):").pack()
    ink_count_entry_field = ttk.Entry(frame, textvariable=ink_count_entry)
    ink_count_entry_field.pack()

    add_ink_button = ttk.Button(frame, text="Add Ink", command=update_ink_count)
    add_ink_button.pack(pady=5)
    add_ink_button.bind("<Return>", lambda event=None: add_ink_button.invoke())

    def show_available_ink():
        total_ink = system_data.get("ink_available", 0.00)
        available_ink_label.config(text=f"Ink Available: {total_ink:.2f} ml")

    show_ink_button = ttk.Button(frame, text="Show Available Ink", command=show_available_ink)
    show_ink_button.pack(pady=(5, 10))
    show_ink_button.bind("<Return>", lambda event=None: show_ink_button.invoke())

    money_count_entry = tk.StringVar()
    available_money_label = ttk.Label(frame, text=f"Available Money: ${system_data.get('money_count', 0.00):.2f}",
                                      foreground="red", font=("", 10, "bold"))
    available_money_label.pack(pady=10)

    def add_money_count():
        try:
            amount = float(money_count_entry.get())
            current_money = system_data.get("money_count", 0.00)

            total_money = current_money + amount
            system_data["money_count"] = total_money

            with open("system.json", "w") as system_file:
                json.dump(system_data, system_file, indent=4)

            available_money_label.config(text=f"Available Money: ${total_money:.2f}")
            money_count_entry.set("")

        except ValueError:
            message_label.config(text="Invalid amount")

    ttk.Label(frame, text="Enter Money Count:").pack()
    money_count_entry_field = ttk.Entry(frame, textvariable=money_count_entry)
    money_count_entry_field.pack()

    add_money_button = ttk.Button(frame, text="Add Money Count", command=add_money_count)
    add_money_button.pack(pady=5)
    add_money_button.bind("<Return>", lambda event=None: add_money_button.invoke())

    def show_available_money():
        total_money = system_data.get("money_count", 0.00)
        available_money_label.config(text=f"Available Money: ${total_money:.2f}")

    show_money_button = ttk.Button(frame, text="Show Available Money", command=show_available_money)
    show_money_button.pack(pady=(5, 20))
    show_money_button.bind("<Return>", lambda event=None: show_money_button.invoke())

    message_label = ttk.Label(frame, text="Message Box", font=("Arial", 8, "bold"), background="orange",
                              foreground="black", width=70, padding=6, anchor="center", justify="center")
    message_label.pack()
