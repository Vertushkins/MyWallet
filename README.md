# My Wallet
## Description
A console application for accounting income and expenses. All records are stored in a text file in a specific format. The user can add, edit, delete, or search for the desired entries. You can also view only income or only expenses and wallet balance.
## Commands
1. **balance** - shows your balance.
```commandline
python main.py balance
```
2. **income** - shows your income.
```commandline
python main.py income
```
3. **expense** - shows your expenses
```commandline
python main.py expense
```
4. **add** - adds a new note.
```commandline
python main.py add 2000-02-14 expense 180 cola 
```
5. **edit** - edits specific note by date.
```commandline
python main.py edit 2000-02-14 category income
```
6. **search** - shows all relevant notes.
```commandline
python main.py search sum 180
```
7. **delete** - deletes specific note by date.
```commandline
python main.py delete 2000-02-14
```
## Testing
1. **test_format** - testing *incorrect_format* function.
```commandline
python -m unittest tests.test_wallet.TestWallet.test_format
```
2. **test_add** - testing *add* function.
```commandline
python -m unittest tests.test_wallet.TestWallet.test_add
```
3. **test_edit** - testing *edit* function.
```commandline
python -m unittest tests.test_wallet.TestWallet.test_edit
```