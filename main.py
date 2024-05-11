import typer
import re
from datetime import datetime


class Wallet:
    # Object for note
    def __init__(self, date='0000-00-00', category='income', amount=0, description='-'):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    # Method for returning a string with a description of the note
    def write(self) -> str:
        return f"Date: {self.date}\nCategory: {self.category}\nSum: {self.amount}\nDescription: {self.description}\n\n"

    # Function that reads a text file and returns a list with Wallet class objects
    @staticmethod
    def wallet_list() -> list:
        try:
            # We read the file line by line
            with open("data.txt", "r") as file:
                wallet_list: list[Wallet] = []
                line = file.readline()

                # If we find a non-empty string, then create a Wallet object and write all the parameters to it
                while line and line != '\n':
                    note = Wallet()
                    while line != '\n':
                        if "Date" in line:
                            note.date = line[6:-1]
                        elif "Category" in line:
                            note.category = line[10:-1]
                        elif "Sum" in line:
                            note.amount = int(line[5:-1])
                        elif "Description" in line:
                            note.description = line[13:-1]
                        line = file.readline()
                    wallet_list.append(note)
                    line = file.readline()

                return wallet_list

        except FileNotFoundError:
            print("File not found")

    # Function that shows your balance
    @staticmethod
    def balance() -> None:
        wallet = Wallet.wallet_list()
        result = 0
        # We refer to each note and, depending on its category, we add or minus the amount
        for note in wallet:
            if note.category == "income":
                result += note.amount
            elif note.category == "expense":
                result -= note.amount
        print(f"Your balance: {result}")

    # Function that shows your income
    @staticmethod
    def income() -> None:
        wallet = Wallet.wallet_list()
        result = 0
        # We refer to each note with category="income" and increase the result
        for note in wallet:
            if note.category == "income":
                result += note.amount
                print(note.write())
        print(f"Total income: {result}")

    # Function that shows your expense
    @staticmethod
    def expense() -> None:
        wallet = Wallet.wallet_list()
        result = 0
        # We refer to each note with category="expense" and increase the result
        for note in wallet:
            if note.category == "expense":
                result += note.amount
                print(note.write())
        print(f"Total expense: {result}")

    # Function that adds a new note to your wallet
    @staticmethod
    def add(date, category, amount, description):
        # Check the correctness of the input
        if Wallet.incorrect_format(date=date, category=category, amount=amount):
            return
        # Check for duplicate notes by date
        for note in Wallet.wallet_list():
            if note.date == date:
                print("Such note already exists")
                return
        # If there are no duplicate notes or incorrect input, then we add a note
        with open("data.txt", "a") as file:
            file.write(f"Date: {date}\nCategory: {category}\nSum: {amount}\nDescription: {description}\n\n")
            print("Success!")
        return Wallet(date=date, category=category, amount=amount, description=description)

    # Function that returns a list of objects that match the requested data
    @staticmethod
    def find(date=r"^(\d{4})-(\d{2})-(\d{2})$", category=r"income|expense", amount=r"\d+", description=r".*") -> list:
        wallet = Wallet.wallet_list()
        result = []
        # We check each note for compliance with the template or the entered data
        for note in wallet:
            if re.match(date, note.date)\
                    and re.match(category, note.category)\
                    and re.fullmatch(amount, str(note.amount))\
                    and re.match(description, note.description):
                result.append(note)
        return result

    # Function that outputs notes by criteria and value
    @staticmethod
    def search(criteria: str, value: str) -> None:
        # Checking what is this criteria
        if criteria == "date":
            # Check the correctness of the input
            if Wallet.incorrect_format(date=value):
                return
            result = Wallet.find(date=value)
        elif criteria == "category":
            if Wallet.incorrect_format(category=value):
                return
            result = Wallet.find(category=value)
        elif criteria == "sum":
            if Wallet.incorrect_format(amount=value):
                return
            result = Wallet.find(amount=value)
        elif criteria == "description":
            result = Wallet.find(description=value)
        else:
            print("Incorrect format")
            return

        # And output of result
        if result:
            for note in result:
                print(note.write())
        else:
            print("Nothing was found")

    # Function that edits a certain note according to certain criteria
    @staticmethod
    def edit(date: str, criteria: str, value: str) -> None:
        criteria = criteria
        value = value
        wallet = Wallet.wallet_list()

        # We check the correctness of the input and existence of the note
        if Wallet.incorrect_format(date=date):
            return
        exist = False
        for note in wallet:
            if note.date == date:
                exist = True
                break
        if not exist:
            print("Such note doesn't exist")
            return

        # We overwrite all the records in the file, but if we find a record that needs to be changed, then we change it
        with open("data.txt", "w") as file:
            for note in wallet:
                if note.date == date:
                    # Checking what is this criteria
                    if criteria == "category":
                        # Check the correctness of the input
                        if not Wallet.incorrect_format(category=value):
                            # Changing
                            note.category = value
                            print("Success!")
                    elif criteria == "sum":
                        if not Wallet.incorrect_format(amount=value):
                            note.amount = value
                            print("Success!")
                    elif criteria == "description":
                        note.description = value
                    else:
                        print("Incorrect format")
                # Writing a note in file
                file.writelines(note.write())

    # Function that deletes a certain note according to date
    @staticmethod
    def delete(date: str) -> None:
        wallet = Wallet.wallet_list()

        # We check the correctness of the input and existence of the note
        if Wallet.incorrect_format(date=date):
            return
        exist = False
        for note in wallet:
            if note.date == date:
                exist = True
                break
        if not exist:
            print("Such note doesn't exist")
            return

        # We write all notes to file except for a note with certain date
        with open("data.txt", "w") as file:
            for note in wallet:
                if note.date == date:
                    print("Success!")
                    continue
                # Writing a note in file
                file.writelines(note.write())

    # Function that checks the correctness of the input
    @staticmethod
    def incorrect_format(date="2000-01-01", category="income", amount="10") -> bool:
        # Checking the correctness of the date
        if date != "2000-01-01":
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("Incorrect date format")
                return True

        # Checking the correctness of the category
        if not re.fullmatch(r"income|expense", category):
            print("Incorrect category format")
            return True

        # Checking the correctness of the amount
        if not re.fullmatch(r"\d+", str(amount)):
            print("Incorrect sum format")
            return True

        return False


def main():
    app = typer.Typer()

    # The function shows income. Syntax:"python main.py income"
    @app.command()
    def income():
        Wallet.income()

    # The function shows expense. Syntax:"python main.py expense"
    @app.command()
    def expense():
        Wallet.expense()

    # The function shows balance. Syntax:"python main.py balance"
    @app.command()
    def balance():
        Wallet.balance()

    # The function adds a note. Syntax:"python main.py add [yyyy-mm-dd] [income|expense] [amount] [text]"
    @app.command()
    def add(date, category, amount, description):
        Wallet.add(date, category, amount, description)

    # The function searches notes. Syntax:"python main.py search [date|category|sum|description] [value]"
    @app.command()
    def search(criteria, value):
        Wallet.search(criteria, value)

    # The function edits the note. Syntax:"python main.py edit [yyyy-mm-dd] [category|amount|description] [value]"
    @app.command()
    def edit(date, criteria, value):
        Wallet.edit(date, criteria, value)

    # The function deletes the note. Syntax:"python main.py delete [yyyy-mm-dd]"
    @app.command()
    def delete(date):
        Wallet.delete(date)

    app()


if __name__ == '__main__':
    main()
