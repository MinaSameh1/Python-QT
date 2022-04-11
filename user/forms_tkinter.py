"""Any GUI form for user."""

from tkinter import Button, Entry, StringVar, Frame, Label
from .handler import register


def register_form(window):
    """Register Page GUI."""
    reg_form = Frame(window)
    reg_form.grid(row=0, column=0)
    Label(reg_form, text="Registeration Form", font="arial 25").pack(pady=50)
    Label(reg_form, text="Name:", font="23").place(x=100, y=150)
    Label(reg_form, text="Password:", font="23").place(x=100, y=200)
    Label(reg_form, text="Email:", font="23").place(x=100, y=250)
    name_value = StringVar()
    email_value = StringVar()
    password_value = StringVar()
    name_entry = Entry(
        reg_form, textvariable=name_value, width=30, bd=2, font="20"
    )
    name_entry.place(x=200, y=150)
    email_entry = Entry(
        reg_form, textvariable=email_value, width=30, bd=2, font="20"
    )
    email_entry.place(x=200, y=200)
    password_entry = Entry(
        reg_form, textvariable=password_value, width=30, bd=2, font="20"
    )
    password_entry.place(x=200, y=250)

    Button(
        text="register",
        font="20",
        width=11,
        height=2,
        command=lambda: register(
            name_value.get(), email_value.get(), password_value.get()
        ),
    ).place(x=250, y=380)
    return reg_form
