from datetime import datetime
def parse_future_datetime(value):
    try: result = datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except (TypeError, ValueError): raise ValueError("Enter a valid date and time.")
    if result <= datetime.now(): raise ValueError("Appointment must be in the future.")
    return result
