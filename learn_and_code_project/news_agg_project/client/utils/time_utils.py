from datetime import datetime

def current_time_info():
    now = datetime.now()
    date_str = now.strftime("%d-%b-%Y")
    time_str = now.strftime("%I:%M %p")
    return date_str, time_str
