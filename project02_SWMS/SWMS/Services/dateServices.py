from datetime import datetime


def get_time_now():
    """
    Get current date/time
    :return: current date/time
    """
    now = datetime.now()
    formatted = now.strftime("%d/%m/%y %H:%M:%S")
    return formatted
