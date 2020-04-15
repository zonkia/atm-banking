import json
import os
from enum import IntEnum
import time
import webbrowser
from getPerformance import get_performance

os.chdir(os.path.dirname(__file__))


class BankAccount:

    def __init__(self, balance: float, id: int):
        self.id = id
        self.balance = balance


class LoginAccount:

    def __init__(self):
        SignMenu = IntEnum("SignMenu", "UP IN")
        while True:
            try:
                signChoice = int(input("""Please choose an option:
1. Sign up
2. Sign in
"""))
                if signChoice == SignMenu.UP or signChoice == SignMenu.IN:
                    if signChoice == SignMenu.UP:
                        LoginAccount.sign_up(self)
                        break

                    elif signChoice == SignMenu.IN:
                        LoginAccount.sign_in(self)
                        break

                else:
                    print("Wrong choice, please try again")
                    continue
            except:
                print("Wrong choice, please try again")
                continue

    def save_file(self, accountsFile, fileName):
        with open(str(fileName) + ".json", "w", encoding="UTF-8-sig") as newAccount:
            json.dump(accountsFile, newAccount,
                      ensure_ascii=False, indent=4)

    def read_file(self, fileName):
        with open(str(fileName) + ".json", "r", encoding="UTF-8-sig") as credentialsJson:
            return json.load(credentialsJson)

    def sign_in(self):
        credentialsFile = LoginAccount.read_file(
            self, "credentials")
        while True:
            try:
                login = str(
                    input("Please enter your UserID: "))
            except:
                print("Wrong ID, please try again")
                continue
            if login not in credentialsFile:
                print("Wrong ID, please try again")
                continue
            password = input(
                "Please enter your password: ")
            if password != credentialsFile[login]:
                print("Wrong password, please try again")
                continue
            else:
                accountsFile = LoginAccount.read_file(
                    self, "Accounts")
                accountBalance = accountsFile[login]
                self.user = BankAccount(
                    accountBalance, login)
            break

    def sign_up(self):
        # opening credentials file
        credentialsFile = LoginAccount.read_file(
            self, "credentials")
        while True:
            try:
                balance = float(
                    input("Please give your starting balance: "))
                break
            except:
                print("Wrong balance, please try again")
                continue
        if credentialsFile == {}:
            newId = 1
        else:
            newId = int(
                list(credentialsFile.keys())[-1]) + 1
        self.user = BankAccount(balance, newId)
        print("Your UserID is: ", self.user.id)
        password = input("Please enter your password: ")
        credentialsFile[self.user.id] = password
        LoginAccount.save_file(
            self, credentialsFile, "credentials")

        # opening accounts file and saving with new account
        accountsFile = LoginAccount.read_file(self, "Accounts")
        accountsFile[self.user.id] = balance
        LoginAccount.save_file(self, accountsFile, "Accounts")


class OperationsAccount:

    def __init__(self):

        session = LoginAccount()

        print()
        print("Welcome User No.", session.user.id,
              ", your current balance is:", session.user.balance)

        OperationsMenu = IntEnum(
            "OperationsMenu", "Add Show Transfer Withdraw Logout")

        while True:
            try:
                operationChoice = int(input("""Please choose an option:
1. Add funds
2. Show balance
3. Make transfer
4. Withdraw
5. Logout
"""))
                if operationChoice == OperationsMenu.Add or \
                        operationChoice == OperationsMenu.Show or \
                        operationChoice == OperationsMenu.Transfer or \
                        operationChoice == OperationsMenu.Withdraw or \
                        operationChoice == OperationsMenu.Logout:

                    if operationChoice == OperationsMenu.Add:
                        OperationsAccount.add_funds(self, session)
                        continue

                    if operationChoice == OperationsMenu.Show:
                        OperationsAccount.show_balance(self, session)
                        continue

                    if operationChoice == OperationsMenu.Transfer:
                        OperationsAccount.transfer_funds(self, session)
                        continue

                    if operationChoice == OperationsMenu.Withdraw:
                        OperationsAccount.withdraw_funds(self, session)
                        continue

                    if operationChoice == OperationsMenu.Logout:
                        OperationsAccount.log_out(self)
                        continue
                else:
                    print("Wrong choice, please try again")
                    continue
            except:
                print("Wrong choice, please try again")
                continue

    def save_file(self, accountsFile):
        with open("Accounts.json", "w", encoding="UTF-8-sig") as accountUpdate:
            json.dump(accountsFile, accountUpdate,
                      ensure_ascii=False, indent=4)

    def read_file(self):
        with open("Accounts.json", "r", encoding="UTF-8-sig") as accountsJson:
            return json.load(accountsJson)

    def add_funds(self, session):
        while True:
            try:
                fundsToAdd = float(
                    input("Please enter amount to transfer: "))
                break
            except:
                print("Wrong amount, please try again")
                continue
        accountsFile = OperationsAccount.read_file(self)
        session.user.balance += fundsToAdd
        accountsFile[session.user.id] = session.user.balance
        # save file
        OperationsAccount.save_file(self, accountsFile)
        print("Transfer successful, your current balance:",
              session.user.balance)
        _ = input("Please press enter to return to menu")
        print()

    def show_balance(self, session):
        print("User No.", session.user.id,
              "your current balance is:", session.user.balance)
        _ = input("Press enter to return to menu")
        print()

    def transfer_funds(self, session):
        accountsFile = OperationsAccount.read_file(self)
        balance = session.user.balance
        while True:
            try:
                amountToTransfer = float(input(
                    "Please enter amount to transfer: "))
                if amountToTransfer > balance:
                    print("Not enough funds, please try again")
                    continue
                receiverId = str(input(
                    "Please enter destination account ID number: "))
                if receiverId not in accountsFile:
                    print("Wrong ID, please try again")
                    continue
                break
            except:
                print("Wrong amount to transfer, please try again")
                continue
        session.user.balance -= amountToTransfer
        accountsFile[session.user.id] = session.user.balance
        accountsFile[receiverId] += amountToTransfer
        # saving to file
        OperationsAccount.save_file(self, accountsFile)
        print("Transfer successful, your current balance:",
              session.user.balance)
        _ = input("Press enter to return to menu")
        print()

    def withdraw_funds(self, session):
        accountsFile = OperationsAccount.read_file(self)
        while True:
            try:
                amountToWithdraw = float(
                    input("Please enter amount to withdraw: "))
                if amountToWithdraw > session.user.balance:
                    print("Not enough funds, please try again")
                break
            except:
                print("Wrong amount, please try again")
                continue
        session.user.balance -= amountToWithdraw
        accountsFile[session.user.id] = session.user.balance
        # saving to file
        OperationsAccount.save_file(self, accountsFile)
        print("Withdrawal successful, your current balance:",
              session.user.balance)
        print(
            "Please collect your money from ATM within next 10 seconds, or else the amount will return to your account")
        time.sleep(2)
        start = time.perf_counter()
        webbrowser.open_new_tab(
            "https://assets.nigerianchannel.com/wp-content/uploads/2018/12/05111607/Earn-Interest-like-the-banks1.jpg")
        _ = input(
            "Please press enter to confirm that you have collected your money")
        end = time.perf_counter()
        if end - start < 10:
            print("Withdrawal complete, it took you just", round(
                end - start, 2), "seconds to collect you money")
            _ = input(
                "Please press enter to return to menu")
            print()
        else:
            print(
                "Too slow. Withdrawal has been canceled, and your money is back on your account")
            print()
            session.user.balance += amountToWithdraw
            accountsFile = OperationsAccount.read_file(self)
            accountsFile[session.user.id] = session.user.balance
            # saving to file
            OperationsAccount.save_file(self, accountsFile)

    def log_out(self):
        print("Goodbye")
        time.sleep(2)
        print()
        OperationsAccount()
        print()
