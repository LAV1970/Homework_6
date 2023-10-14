from datetime import datetime
from some_module import Field
import re


class PhoneField(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not re.match(r"^\(\d{3}\) \d{3}-\d{4}$", new_value):
            raise ValueError("Phone number must be in the format (XXX) XXX-XXXX")
        self._value = new_value


class BirthdayField(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", new_value):
            raise ValueError("Birthday must be in the format YYYY-MM-DD")
        self._value = new_value


class Record:
    def __init__(self, name, phone, email, birthday=None):
        self.name = Field(name)
        self.phone = PhoneField(phone)
        self.email = Field(email)
        self.birthday = BirthdayField(birthday)

    def days_to_birthday(self):
        if self.birthday.value is None:
            return None

        try:
            birthdate = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        except ValueError:
            return None

        current_date = datetime.now()
        next_birthday = datetime(current_date.year, birthdate.month, birthdate.day)

        if current_date > next_birthday:
            next_birthday = next_birthday.replace(year=current_date.year + 1)

        days_until_birthday = (next_birthday - current_date).days
        return days_until_birthday


class AddressBook:
    def __init__(self):
        self.records = []

    def __iter__(self):
        return self.iterator()

    def iterator(self, chunk_size=10):
        current_index = 0
        while current_index < len(self.records):
            yield self.records[current_index : current_index + chunk_size]
            current_index += chunk_size
