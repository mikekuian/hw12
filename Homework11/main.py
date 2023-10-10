from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.validate_phone(new_value):
            raise ValueError("Phone number must have 10 digits")
        self._value = new_value

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value=None):
        if value:
            self.value = self.validate_birthday(value)
        else:
            self.value = None

    @staticmethod
    def validate_birthday(value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            if birthday > datetime.now():
                raise ValueError("Birthday cannot be in the future")
            return birthday
        except ValueError:
            raise ValueError("Invalid date format. Expected DD.MM.YYYY")

    def __str__(self):
        if self.value:
            return self.value.strftime("%d.%m.%Y")
        return ""


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found")

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Name: {self.name.value}, Phones: {phones_str}, Birthday: {self.birthday}"

    def days_to_birthday(self):
        if self.birthday and self.birthday.value:
            now = datetime.now()
            next_birthday = self.birthday.value.replace(year=now.year)
            if now > next_birthday:
                next_birthday = next_birthday.replace(year=now.year + 1)
            return (next_birthday - now).days
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, N):
        if not isinstance(N, int) or N <= 0:
            raise ValueError("N should be a positive integer")

        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]

