from datetime import datetime


def get_time_now():
    now = datetime.now()
    formatted = now.strftime("%y/%m/%d %H:%M:%S")
    return formatted
