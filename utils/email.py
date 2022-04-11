"""Handles any related email tasks."""
import os
from smtplib import SMTP_SSL, SMTPException
import ssl


def send_mail(reciever: str, msg: str) -> bool:
    """
    Send mail.

    @param reciever `str`: email to send to.
    @param msg `str`: msg to be sent.
    @return True if sent false if failed.
    """
    try:
        from_addr: str = "noameammo@gmail.com"
        context = ssl.create_default_context()
        with SMTP_SSL("smtp.gmail.com", 465, context=context) as mail_server:
            mail_server.ehlo()
            mail_server.login(from_addr, os.getenv("APP_PASS"))
            mail_server.sendmail(from_addr, reciever, msg)
            return True
    except SMTPException as err:
        return False, err
