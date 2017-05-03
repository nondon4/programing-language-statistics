import datetime


def add_months(date, months):
    month = date.month - 1 + months
    year = int(date.year + month / 12)
    month = month % 12 + 1
    day = 1
    return datetime.date(year, month, day)
