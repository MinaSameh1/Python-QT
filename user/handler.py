"""Handles any user related ops."""

from random import randint
from tkinter import messagebox
from utils.email import send_mail


def register(name: str, email: str, password: str) -> bool:
    """Register user."""
    print("WORKING " + email)


def send_otp(otp, email) -> bool:
    """Register User."""
    otp = randint(100000, 999999)
    if send_mail(
        email,
        f"""
    Subject: OTP for program
    OTP is {otp}
    """,
    ):
        messagebox.showinfo("Sent OTP to mail!")
        return True
    messagebox.showerror(message="Email is not valid!")
    return False
