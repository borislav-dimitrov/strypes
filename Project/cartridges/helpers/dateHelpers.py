from datetime import datetime


def get_today():
    return datetime.today().strftime('%d/%m/%Y %H:%M:%S')
