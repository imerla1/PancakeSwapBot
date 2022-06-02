import smtplib
from email.message import EmailMessage
from datetime import datetime
import logging
import os
import sys
import traceback
from utils.logger import setup_logger


def send_mail(logger, message, receiver, **params):
    try:
        msg = EmailMessage()
        msg["Subject"] = params["subject"]
        msg["From"] = params["sender"]
        msg["To"] = receiver
        msg.set_content(message)
        server = smtplib.SMTP_SSL(params["smtp_server"], params['port'])
        server.login(params["sender"], "imerla1234")
        server.send_message(msg)
        logger.debug(f"Voting Alert sent to <{receiver}>\n\tMsg:{message}")
        print(f"Voting Alert sent to <{receiver}>\n\tMsg:{message}")
        server.quit()
    except:
        print("Critical Error In mail")
        error_logger = setup_logger("error_logger", "errors.log")
        error_logger.critical("Critical Error", exc_info=sys.exc_info())
        traceback.print_exc()


if __name__ == "__main__":
    from logger import setup_logger
    logger = setup_logger("alert_logger", "alert.log")
    cfg = {
        "subject": "Voting",
        "sender": "flaskapp90@gmail.com",
        "password": os.getenv("password"),
        "smtp_server": "smtp.gmail.com",
        "port": 465
    }

    send_mail(logger, "Hello Master", "wadedisley@gmail.com", **cfg)
    send_mail(logger, "Hello Master", "wadedisley@yahoo.co.uk", **cfg)
    send_mail(logger, "Hello Master", "malisauskas88@gmail.com", **cfg)

