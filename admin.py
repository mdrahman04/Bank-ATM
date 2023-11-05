import tkinter as tk
from tkinter import ttk
import json


def show_admin_view(root):
    admin_pin_entry = tk.StringVar()
    customer_pin_entry = tk.StringVar()
    name_var = tk.StringVar()
    pin_var = tk.StringVar()
    balance_var = tk.StringVar()

    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=0)

    account_listbox = None

    def load_accounts_data():
        try:
            with open("accounts.json", "r") as accounts_file:
                return json.load(accounts_file)
        except FileNotFoundError:
            return {}

    def save_accounts_data(accounts_data):
        with open("accounts.json", "w") as accounts_file:
            json.dump(accounts_data, accounts_file, indent=4)

    def verify_admin_pin(admin_pin):
        return admin_pin == "12345"

    def verify_customer_pin(customer_pin):
        return len(customer_pin) == 4 and customer_pin.isdigit()

    def add_account():
        name = name_var.get()
        pin = pin_var.get()
        balance = balance_var.get()

        if not name or not pin or not balance:
            message_label.config(text="All fields must be filled")
        elif not verify_customer_pin(pin):
            message_label.config(text="Invalid PIN. Please enter exactly 4 digits.")
        else:
            new_account = {
                "name": name,
                "pin": pin,
                "balance": float(balance)
            }

            accounts_data = load_accounts_data()
            unique_id = str(abs(hash(name)))[:8].rjust(8, '0')
            new_account["unique_id"] = unique_id

            accounts_data[unique_id] = new_account
            save_accounts_data(accounts_data)
            message_label.config(text="Account added successfully")
            clear_account_fields()
            populate_account_list()

    def clear_account_fields():
        name_var.set("")
        pin_var.set("")
        balance_var.set("")

    def delete_accounts():
        if account_listbox:
            selected_indices = account_listbox.curselection()
            if selected_indices:
                selected_indices = list(map(int, selected_indices))
                accounts_data = load_accounts_data()
                for index in selected_indices[::-1]:
                    account_data = account_listbox.get(index)
                    unique_id = account_data.split(",")[0].split(":")[1].strip()
                    del accounts_data[unique_id]
                save_accounts_data(accounts_data)
                message_label.config(text="Selected accounts deleted")
                populate_account_list()

    def populate_account_list():
        nonlocal account_listbox
        if not account_listbox:
            account_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=40, width=70)
            account_listbox.pack(pady=10, padx=5)
        accounts_data = load_accounts_data()
        account_listbox.delete(0, tk.END)
        for unique_id, account in accounts_data.items():
            account_listbox.insert(tk.END, f"ID: {unique_id}, Name: {account['name']}, PIN: {account['pin']},"
                                           f" Balance: {account['balance']}")

    ttk.Label(frame, text="Enter Admin PIN (5 digits):  # 12345", font=("", 9, "bold"),
              foreground="orange").pack(pady=10)
    admin_pin_entry_field = ttk.Entry(frame, textvariable=admin_pin_entry, show="*")
    admin_pin_entry_field.pack()

    def verify_admin_and_show_actions():
        admin_pin = admin_pin_entry.get()
        if verify_admin_pin(admin_pin):
            admin_pin_entry_field.config(state="disabled")
            verify_button.config(state="disabled")

            account_details_frame = ttk.Frame(frame)
            account_details_frame.pack()

            ttk.Label(account_details_frame, text="Account Details:",
                      font=("", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
            ttk.Label(account_details_frame, text="Name:",
                      font=("", 9, "bold")).grid(row=1, column=0, sticky="e", padx=10, pady=10)
            name_entry = ttk.Entry(account_details_frame, textvariable=name_var)
            name_entry.grid(row=1, column=1)

            ttk.Label(account_details_frame, text="PIN (4 digits):",
                      font=("", 9, "bold")).grid(row=2, column=0, sticky="e", padx=10, pady=10)
            pin_entry = ttk.Entry(account_details_frame, textvariable=pin_var)
            pin_entry.grid(row=2, column=1)

            ttk.Label(account_details_frame, text="Initial Balance:",
                      font=("", 9, "bold")).grid(row=3, column=0, sticky="e", padx=10, pady=10)
            balance_entry = ttk.Entry(account_details_frame, textvariable=balance_var)
            balance_entry.grid(row=3, column=1)

            add_account_button = ttk.Button(account_details_frame, text="Add Account", command=add_account)
            add_account_button.grid(row=4, column=0, columnspan=2, pady=5)
            add_account_button.bind("<Return>", lambda event=None: add_account_button.invoke())

            clear_button = ttk.Button(account_details_frame, text="Clear", command=clear_account_fields)
            clear_button.grid(row=5, column=0, columnspan=2, pady=3)
            clear_button.bind("<Return>", lambda event=None: clear_button.invoke())

            update_button = ttk.Button(frame, text="Show List", command=populate_account_list)
            update_button.pack(side=tk.LEFT)
            update_button.bind("<Return>", lambda event=None: update_button.invoke())

            delete_button = ttk.Button(frame, text="Delete", command=delete_accounts)
            delete_button.pack(side=tk.RIGHT)
            update_button.bind("<Return>", lambda event=None: update_button.invoke())
        else:
            admin_pin_entry_field.focus()
            message_label.config(text="Invalid Admin PIN")

    verify_button = ttk.Button(frame, text="Verify Admin PIN", command=verify_admin_and_show_actions)
    verify_button.pack(pady=10)
    verify_button.bind("<Return>", lambda event=None: verify_button.invoke())

    message_label = ttk.Label(frame, text="Message Box",
                              font=("Arial", 8, "bold"), background="orange",
                              foreground="black", width=70, padding=6, anchor="center", justify="center")
    message_label.pack(padx=7, pady=7)
