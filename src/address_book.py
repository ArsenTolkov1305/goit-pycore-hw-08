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
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        if parsed_date > datetime.now():
            raise ValueError("Birthday cannot be in the future.")

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)

        if phone_obj is None:
            raise ValueError("Phone number not found.")

        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            raise ValueError("Phone number not found.")

        new_phone_obj = Phone(new_phone)
        phone_obj.value = new_phone_obj.value

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        birthday = ""
        if self.birthday:
            birthday = f", birthday: {self.birthday.value}"

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
            f"{birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = datetime.strptime(
                record.birthday.value, "%d.%m.%Y"
            ).date()

            try:
                birthday_this_year = birthday.replace(year=today.year)
            except ValueError:
                # 29.02 у невисокосному році
                birthday_this_year = birthday.replace(
                    year=today.year,
                    day=28
                )

            if birthday_this_year < today:
                try:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1
                    )
                except ValueError:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1,
                        day=28
                    )

            days_until = (birthday_this_year - today).days

            if 0 <= days_until <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date += timedelta(days=2)

                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "No contacts saved."

        return "\n".join(str(record) for record in self.data.values())
