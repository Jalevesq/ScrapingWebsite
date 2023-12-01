import datetime

def getDate() -> str:
    today_date: datetime.date = datetime.date.today()
    return today_date.strftime("%Y-%m-%d")

