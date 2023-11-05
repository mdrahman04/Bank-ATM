import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk


def save_accounts_data(accounts_data):
    with open("accounts.json", "w") as accounts_file:
        json.dump(accounts_data, accounts_file, indent=4)


def show_customer_view(root):
    customer_frame = ttk.Frame(root)

    withdrawal_entry = tk.StringVar()
    deposit_entry = tk.StringVar()
    recipient_entry = tk.StringVar()
    transfer_entry = tk.StringVar()

    def load_accounts_data():
        try:
            with open("accounts.json", "r") as accounts_file:
                return json.load(accounts_file)
        except FileNotFoundError:
            return {}

    accounts_data = load_accounts_data()

    def load_system_data():
        try:
            with open("system.json", "r") as system_file:
                return json.load(system_file)
        except FileNotFoundError:
            return {}

    def save_system_data(system_data):
        with open("system.json", "w") as system_file:
            json.dump(system_data, system_file, indent=4)

    def clear_input_fields():
        id_entry.delete(0, tk.END)
        pin_entry.delete(0, tk.END)
        withdrawal_entry.set("")
        deposit_entry.set("")
        recipient_entry.set("")
        transfer_entry.set("")
        message_label.config(text="")

    def check_balance(unique_id, pin, accounts_data):
        if unique_id in accounts_data and accounts_data[unique_id]["pin"] == pin:
            balance = accounts_data[unique_id]["balance"]
            message_label.config(text=f"Your balance is ${balance:.2f}")
        else:
            message_label.config(text="Invalid Unique ID or PIN")

    def withdraw_cash(unique_id, pin, accounts_data, system_data):
        if unique_id in accounts_data and accounts_data[unique_id]["pin"] == pin:
            try:
                withdrawal_amount = float(withdrawal_entry.get())
                if withdrawal_amount <= accounts_data[unique_id]["balance"]:
                    if withdrawal_amount <= system_data["money_count"] and system_data["ink_available"] >= 1:
                        accounts_data[unique_id]["balance"] -= withdrawal_amount
                        system_data["money_count"] -= withdrawal_amount
                        system_data["ink_available"] -= 1
                        save_accounts_data(accounts_data)
                        save_system_data(system_data)
                        message_label.config(
                            text=f"Withdrew ${withdrawal_amount:.2f}. "
                                 f"Your new balance is ${accounts_data[unique_id]['balance']:.2f}")
                    else:
                        message_label.config(text="System error. Please contact technician.")
                else:
                    message_label.config(text="Insufficient balance")
            except ValueError:
                message_label.config(text="Invalid amount")
        else:
            message_label.config(text="Invalid Unique ID or PIN")

    def deposit(unique_id, pin, accounts_data, system_data):
        if unique_id in accounts_data and accounts_data[unique_id]["pin"] == pin:
            try:
                deposit_amount = float(deposit_entry.get())
                if deposit_amount > 0:
                    if system_data["ink_available"] >= 1:
                        accounts_data[unique_id]["balance"] += deposit_amount
                        system_data["money_count"] += deposit_amount
                        system_data["ink_available"] -= 1
                        save_accounts_data(accounts_data)
                        save_system_data(system_data)
                        message_label.config(
                            text=f"Deposited ${deposit_amount:.2f}. "
                                 f"Your new balance is ${accounts_data[unique_id]['balance']:.2f}")
                    else:
                        message_label.config(text="System error. Please contact technician.")
                else:
                    message_label.config(text="Invalid amount")
            except ValueError:
                message_label.config(text="Invalid amount")
        else:
            message_label.config(text="Invalid Unique ID or PIN")

    def transfer(unique_id, pin, accounts_data):
        if unique_id in accounts_data and accounts_data[unique_id]["pin"] == pin:
            recipient_id = recipient_entry.get()
            if recipient_id in accounts_data:
                try:
                    transfer_amount = float(transfer_entry.get())
                    if transfer_amount > 0 and transfer_amount <= accounts_data[unique_id]["balance"]:
                        accounts_data[unique_id]["balance"] -= transfer_amount
                        accounts_data[recipient_id]["balance"] += transfer_amount
                        system_data["ink_available"] -= 1
                        save_accounts_data(accounts_data)
                        message_label.config(text=f"Transferred ${transfer_amount:.2f} to "
                                                  f"{accounts_data[recipient_id]['name']}. "
                                                  f"Your new balance is ${accounts_data[unique_id]['balance']:.2f}")
                    else:
                        message_label.config(text="Invalid amount or insufficient balance")
                except ValueError:
                    message_label.config(text="Invalid amount")
            else:
                message_label.config(text="Recipient not found")

    label = ttk.Label(root, text="Customer Panel", font=("Arial", 10, "bold"), foreground="orange")
    label.pack(pady=(0, 15))

    id_label = ttk.Label(root, text="Unique ID (8 digits):", font=("", 9, "bold"))
    id_entry = ttk.Entry(root)
    pin_label = ttk.Label(root, text="PIN (4 digits):", font=("", 9, "bold"))
    pin_entry = ttk.Entry(root, show="*")

    id_label.pack()
    id_entry.pack(pady=(0, 15))
    pin_label.pack()
    pin_entry.pack(pady=(0, 15))

    message_label = ttk.Label(root, text="Message Box", font=("Arial", 8, "bold"), background="orange",
                              foreground="black", width=90, padding=8, anchor="center", justify="center")
    message_label.pack(padx=10, pady=10)

    system_data = load_system_data()

    top_frame = ttk.Frame(root)
    top_frame.pack(side=tk.TOP)

    def update_signal_images():
        nonlocal signal_label_money, signal_label_ink
        system_data = load_system_data()

        if system_data.get("money_count", 0) >= 100:
            img_money = Image.open("img/green_signal.png")
        else:
            img_money = Image.open("img/red_signal.png")

        img_money = img_money.resize((30, 30))
        signal_icon_money = ImageTk.PhotoImage(img_money)
        signal_label_money.config(image=signal_icon_money)
        signal_label_money.image = signal_icon_money

        if system_data.get("ink_available", 0) > 100:
            img_ink = Image.open("img/green_signal_1.png")
        else:
            img_ink = Image.open("img/red_signal_1.png")

        img_ink = img_ink.resize((30, 30))
        signal_icon_ink = ImageTk.PhotoImage(img_ink)
        signal_label_ink.config(image=signal_icon_ink)
        signal_label_ink.image = signal_icon_ink

        root.after(1000, update_signal_images)

    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=0)

    img_money = Image.open("img/green_signal.png")
    img_money = img_money.resize((30, 30))
    signal_icon_money = ImageTk.PhotoImage(img_money)
    signal_label_money = ttk.Label(top_frame, image=signal_icon_money)
    signal_label_money.image = signal_icon_money
    signal_label_money.pack(side=tk.LEFT, padx=310)

    img_ink = Image.open("img/green_signal_1.png")
    img_ink = img_ink.resize((30, 30))
    signal_icon_ink = ImageTk.PhotoImage(img_ink)
    signal_label_ink = ttk.Label(top_frame, image=signal_icon_ink)
    signal_label_ink.image = signal_icon_ink
    signal_label_ink.pack(side=tk.RIGHT, padx=310)

    update_signal_images()

    action_frame = ttk.Frame(root)
    action_frame.pack(padx=20, pady=0)

    ttk.Label(action_frame, text="Actions:", font=("", 9, "bold")).grid(row=0, column=0, columnspan=3)

    ttk.Label(action_frame, text="1. Check Balance:", font=("", 10, "bold")).grid(row=1, column=0, sticky="w",
                                                                                  pady=(15, 10))
    check_balance_button = ttk.Button(action_frame, text="Check Balance",
                                      command=lambda: check_balance(id_entry.get(), pin_entry.get(), accounts_data))
    check_balance_button.grid(row=1, column=1, sticky="w", padx=5, pady=(15, 10))
    check_balance_button.bind("<Return>", lambda event=None: check_balance_button.invoke())

    ttk.Label(action_frame, text="2. Withdraw Cash:", font=("", 10, "bold")).grid(row=2, column=0, sticky="w", pady=10)
    withdrawal_entry_widget = ttk.Entry(action_frame, textvariable=withdrawal_entry)
    withdrawal_entry_widget.grid(row=2, column=1, sticky="w", padx=5)
    withdraw_cash_button = ttk.Button(action_frame, text="Withdraw",
                                      command=lambda: withdraw_cash(id_entry.get(), pin_entry.get(),
                                                                    accounts_data, system_data))
    withdraw_cash_button.grid(row=2, column=2, sticky="w")
    withdraw_cash_button.bind("<Return>", lambda event=None: withdraw_cash_button.invoke())

    ttk.Label(action_frame, text="3. Deposit:", font=("", 10, "bold")).grid(row=3, column=0, sticky="w", pady=10)
    deposit_entry_widget = ttk.Entry(action_frame, textvariable=deposit_entry)
    deposit_entry_widget.grid(row=3, column=1, sticky="w", padx=5)
    deposit_button = ttk.Button(action_frame, text="Deposit",
                                command=lambda: deposit(id_entry.get(), pin_entry.get(), accounts_data, system_data))
    deposit_button.grid(row=3, column=2, sticky="w")
    deposit_button.bind("<Return>", lambda event=None: deposit_button.invoke())

    ttk.Label(action_frame, text="4. Transfer:", font=("", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 0))
    recipient_id_label = ttk.Label(action_frame, text="Recipient's Unique ID:")
    recipient_id_label.grid(row=5, column=0, sticky="w")
    recipient_entry_widget = ttk.Entry(action_frame, textvariable=recipient_entry, width=20)
    recipient_entry_widget.grid(row=5, column=1, sticky="w", padx=5)
    transfer_amount_label = ttk.Label(action_frame, text="Transfer Amount:")
    transfer_amount_label.grid(row=6, column=0, sticky="w")
    transfer_entry_widget = ttk.Entry(action_frame, textvariable=transfer_entry, width=20)
    transfer_entry_widget.grid(row=6, column=1, sticky="w", padx=5)
    transfer_button = ttk.Button(action_frame, text="Transfer",
                                 command=lambda: transfer(id_entry.get(), pin_entry.get(), accounts_data))
    transfer_button.grid(row=6, column=2, sticky="w")
    transfer_button.bind("<Return>", lambda event=None: transfer_button.invoke())

    back_button = ttk.Button(action_frame, text="Clear & Exit", command=clear_input_fields)
    back_button.grid(row=7, column=0, columnspan=3, pady=(20, 0))
    back_button.bind("<Return>", lambda event=None: back_button.invoke())
