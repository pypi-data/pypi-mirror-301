from datetime import datetime;

def now() -> datetime: 
    return datetime.now();

def CalculateTimePassed(start: datetime = 0):
    return datetime.now() - start;

def TimeToString(time: datetime) -> str:
    seconds = time.total_seconds();
    minutes = seconds // 60;
    hours = minutes // 60;
    days = hours // 24;
    return f"{round(days)} Days = {round(hours)} Hours = {round(minutes)} Minutes = {round(seconds, 2)} Seconds";