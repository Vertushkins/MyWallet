import unittest
from main import Wallet


class TestWallet(unittest.TestCase):
    # Testing incorrect_format
    def test_format(self):
        # Correct formats
        self.assertFalse(Wallet.incorrect_format(date="2004-04-27", category="income", amount="12345"))
        self.assertFalse(Wallet.incorrect_format(date="1902-12-15", category="expense", amount="0002"))

        # Incorrect date formats
        self.assertTrue(Wallet.incorrect_format(date="0000-03-01"))
        self.assertTrue(Wallet.incorrect_format(date="1997-31-01"))
        self.assertTrue(Wallet.incorrect_format(date="1997-01-91"))

        # Incorrect category formats
        self.assertTrue(Wallet.incorrect_format(category="income123"))
        self.assertTrue(Wallet.incorrect_format(category="55555expense"))

        # Incorrect amount formats
        self.assertTrue(Wallet.incorrect_format(amount="10a"))
        self.assertTrue(Wallet.incorrect_format(amount="abc"))

    # Testing add
    def test_add(self):
        note = Wallet.add("2004-04-27", "income", "12345", "text")

        # Correct adding
        self.assertTrue(Wallet.find(date=note.date, category=note.category, amount=note.amount))
        Wallet.delete(note.date)

        # Incorrect formats
        self.assertFalse(Wallet.add("2005-13-27", "income", "12345", "text"))
        self.assertFalse(Wallet.add("2005-12-27", "invomr", "12345", "text"))
        self.assertFalse(Wallet.add("2005-12-27", "income", "gg11", "text"))

    # Testing edit
    def test_edit(self):
        note = Wallet.add("2004-04-27", "income", "12345", "text")
        Wallet.edit(note.date, "category", "expense")
        Wallet.edit(note.date, "sum", "9999")

        # Correct editing
        self.assertTrue(Wallet.find(date="2004-04-27", category="expense", amount="9999"))

        # Incorrect formats
        self.assertFalse(Wallet.edit("0645-03-29", "category", "expense"))
        self.assertFalse(Wallet.edit("0645-53-29", "category", "expense"))
        self.assertFalse(Wallet.edit("2004-04-27", "category", "12345income"))
        self.assertFalse(Wallet.edit("2004-04-27", "cottegry", "income"))
        self.assertFalse(Wallet.edit("2004-04-27", "sum", "d39adf"))

        Wallet.delete(note.date)
