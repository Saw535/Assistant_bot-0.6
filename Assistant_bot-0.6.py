import pickle
from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone:
    def __init__(self, value):
        if isinstance(value, str) and value.isdigit() and len(value) == 10:
            self.value = value
        else:
            raise ValueError(f"Invalid phone number {value}. Please enter a 10-digit phone number.")
    
    def __str__(self):
        return self.value

#p = Phone('56323')
#p = Phone('jiewfi')
#p = Phone(6832)
#p = Phone(None)
#print(p)

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__()
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                datetime.strptime(new_value, "%Y-%m-%d")
                super(Birthday, Birthday).value.__set__(self, new_value)
            except ValueError:
                print(f"Invalid birthday format {new_value}. Please use the format: YYYY-MM-DD")
        else:
            super(Birthday, Birthday).value.__set__(self, None)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, index, new_phone):
        if 0 <= index < len(self.phones):
            self.phones[index].value = new_phone

    def delete_phone(self, index):
        if 0 <= index < len(self.phones):
            del self.phones[index]

    def days_to_birthday(self):
        if self.birthday.value is not None:
            today = date.today()
            birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            days_left = (birthday - today).days
            return days_left
        return None

    def birthday_str(self):
        if self.birthday.value:
            return f"Birthday: {self.birthday.value}"
        return ""

    def __str__(self):
        phones = "\n".join(str(phone) for phone in self.phones)
        return f"Name: {self.name}\nPhones:\n{phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=1):
        items = list(self.data.values())
        for i in range(0, len(items), n):
            yield items[i:i+n]

    def search(self, keyword):
        results = []
        for record in self.data.values():
            if keyword.lower() in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if keyword in phone.value:
                    results.append(record)
                    break
        return results

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Unable to load data.")

    def __str__(self):
        records = "\n".join(str(record) for record in self.data.values())
        return f"Address Book:\n{records}"


def hello():
    print("How can I help you?")


def add(name, phone, birthday=None):
    if name in address_book.data:
        record = address_book.data[name]
        try:
            if any(phone == p.value for p in record.phones):
                raise ValueError(f"{name}'s phone number ({phone[-10:]}) already exists in contacts.")
            record.add_phone(phone)
            if birthday is not None:
                record.birthday.value = birthday
            print(f"{name}'s phone number ({phone[-10:]}) has been updated in contacts.")
        except ValueError as e:
            print(str(e))
    else:
        try:
            record = Record(name, phone, birthday)
            address_book.add_record(record)
            print(f"{name}'s phone number ({phone[-10:]}) has been added to contacts.")
        except ValueError as e:
            print(str(e))


def change(name, phone):
    if name in address_book.data:
        record = address_book.data[name]
        try:
            if isinstance(phone, str) and phone.isdigit() and len(phone) == 10:
                record.edit_phone(0, phone)
                print(f"{name}'s phone number has been updated to {phone}.")
            else:
                raise ValueError(f"Invalid phone number {phone}. Please enter a 10-digit phone number.")
        except ValueError as e:
            print(str(e))
    else:
        print(f"{name} is not in contacts.")


def delete(name):
    if name in address_book.data:
        del address_book.data[name]
        print(f"{name} has been deleted from contacts.")
    else:
        print(f"{name} is not in contacts.")


def display_phone(name):
    if name in address_book.data:
        record = address_book.data[name]
        print(f"{record.name.value}:")
        for phone in record.phones:
            print(phone)
    else:
        print(f"{name} is not in contacts.")


def search(keyword):
    results = address_book.search(keyword)
    if results:
        print("Search Results:")
        for record in results:
            print(record)
            print()
    else:
        print("No matching contacts found.")


def show_all():
    if address_book.data:
        today = date.today()
        for record in address_book.data.values():
            print("Name:", record.name)
            print("Phones:")
            for phone in record.phones:
                print(phone)
            if record.birthday:
                print(f"Birthday: {record.birthday}")
                days_left = record.days_to_birthday()
                if days_left is not None:
                    print(f"Days to birthday: {days_left}")
            else:
                print("Birthday: None")
            print()
    else:
        print("No contacts to show.")


def save(filename):
    address_book.save(filename)
    print("Address book saved.")


def load(filename):
    address_book.load(filename)
    print("Address book loaded.")


def exit_program():
    print("Goodbye!")
    quit()


def parse_command(command):
    command = command.strip()
    parts = command.split(' ', 1)
    if parts[0].lower() == 'hello':
        hello()
    elif parts[0].lower() == 'add':
        if len(parts) < 2:
            print("Invalid command: add requires a name and phone number.")
            return
        params = parts[1].split(' ')
        if len(params) >= 2:
            name = params[0]
            phone = params[1]
            if len(params) == 3:
                birthday = params[2]
                add(name, phone, birthday)
            else:
                add(name, phone)
        else:
            print("Invalid command: add requires a name and phone number.")
    elif parts[0].lower() == 'delete':
        if len(parts) < 2:
            print("Invalid command: delete requires a name.")
            return
        delete(parts[1])
    elif parts[0].lower() == 'phone':
        if len(parts) < 2:
            print("Invalid command: phone requires a name.")
            return
        display_phone(parts[1])
    elif parts[0].lower() == 'change':
        if len(parts) < 2:
            print("Invalid command: change requires a name and phone number.")
            return
        params = parts[1].split(' ')
        if len(params) == 2:
            name = params[0]
            phone = params[1]
            change(name, phone)
        else:
            print("Invalid command: change requires a name and phone number.")
    elif parts[0].lower() == 'search':
        if len(parts) < 2:
            print("Invalid command: search requires a name.")
            return
        search(parts[1])
    elif parts[0].lower() == 'show':
        if len(parts) < 2 or parts[1].lower() != 'all':
            print("Invalid command: show requires an argument 'all'.")
            return
        show_all()
    elif parts[0].lower() == 'save':
        if len(parts) > 1:
            save(parts[1])
        else:
            print("Invalid command: save requires a filename.")
    elif parts[0].lower() == 'load':
        if len(parts) < 2:
            print("Invalid command: load requires a filename.")
            return
        load(parts[1])
    elif any(word in parts for word in ['goodbye', 'good', 'bye', 'close', 'exit']):
        exit_program()
    else:
        print(f"Invalid command: {command}")


def main():
    global address_book
    address_book = AddressBook()
    while True:
        command = input("Enter command: ")
        parse_command(command.strip())


if __name__ == '__main__':
    main()