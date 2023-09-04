from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):

    if len(users) == 0:
        return {}
    # Визначаємо поточну дату
    today = date.today()


    # Визначаємо поточний день тижня (0 - понеділок, 1 - вівторок, ..., 6 - неділя)
    current_weekday = today.weekday()

    # Формуємо словник для зберігання днів народжень
    birthdays_per_week = {}

    # Проходимося по користувачам і додаємо їх до відповідних днів тижня
    for user in users:
        birthday = user["birthday"]
        birthday = birthday.replace(year=today.year)
        # Визначаємо, чи є день народження наступного року
        next_year = birthday.replace(year=today.year+1)
        if (next_year - today).days < 7:
            birthday = next_year

        if (birthday - today).days <0:
            continue

        # Визначаємо день тижня для дня народження
        birthday_weekday = birthday.weekday()

        day_name = birthday.strftime("%A")
        if day_name == "Sunday" or day_name == "Saturday":
            day_name = "Monday"
        if day_name not in birthdays_per_week.keys():
            birthdays_per_week[day_name] = []
        birthdays_per_week[day_name].append(user["name"])

    return birthdays_per_week

if __name__ == "__main__":
    users = [
        {"name": "Jan Kim", "birthday": datetime(1976, 9, 5).date()},
        {"name": "Jan Gou", "birthday": datetime(1996, 9, 4).date()},
        {"name": "Jan Kerr", "birthday": datetime(1976, 9, 10).date()},
        {"name": "Jan Kum", "birthday": datetime(1976, 9, 6).date()}
    ]

    result = get_birthdays_per_week(users)
    print(result)
