from datetime import datetime


def get_time_now():
    now = datetime.now()
    formatted = now.strftime("%d/%m/%y %H:%M:%S")
    return formatted
