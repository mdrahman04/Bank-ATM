import tkinter as tk
from tkinter import ttk
from admin import show_admin_view
from customer import show_customer_view
from technician import show_technician_view


def main_menu():
    main_menu_window = tk.Tk()
    main_menu_window.title("Main Menu")

    style = ttk.Style()

    main_menu_window.state('zoomed')

    def show_view(view_function):
        for widget in main_frame.winfo_children():
            widget.destroy()

        view_function(main_frame)

    style.configure("Custom.TFrame",
                    background="#e6e1e1"
                    )

    button_frame = ttk.Frame(main_menu_window, style="Custom.TFrame")
    button_frame.pack(pady=(0, 10))

    label = ttk.Label(button_frame, text="# for switching buttons and fields use 'tab' and for entering use 'enter'",
                      font=("Arial", 10, ""), background="#e6e1e1", foreground="Black")
    label.pack(pady=(4, 0))

    admin_button = ttk.Button(button_frame, text="Admin", command=lambda: show_view(show_admin_view))
    technician_button = ttk.Button(button_frame, text="Technician", command=lambda: show_view(show_technician_view))
    customer_button = ttk.Button(button_frame, text="Customer", command=lambda: show_view(show_customer_view))

    admin_button.pack(side=tk.LEFT, padx=120)
    technician_button.pack(side=tk.RIGHT, padx=120)
    customer_button.pack(pady=(40, 10))

    admin_button.bind("<Return>", lambda event=None: admin_button.invoke())
    technician_button.bind("<Return>", lambda event=None: technician_button.invoke())
    customer_button.bind("<Return>", lambda event=None: customer_button.invoke())

    main_frame = ttk.Frame(main_menu_window)
    main_frame.pack(padx=20, pady=20)

    show_customer_view(main_frame)

    main_menu_window.mainloop()


if __name__ == "__main__":
    main_menu()
