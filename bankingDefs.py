import json
import os
from enum import IntEnum
import time
import webbrowser
import objcrypt
from cryptography.fernet import Fernet
import stdiomask

os.chdir(os.path.dirname(__file__))


class BankAccount:

    def __init__(self, balance: float, id: int):
        self.id = id
        self.balance = balance


class FileSupport:

    def save_file(self, dictToSave, fileName):
        with open(str(fileName) + ".json", "w", encoding="UTF-8-sig") as fileJson:
            json.dump(dictToSave, fileJson,
                      ensure_ascii=False, indent=4)

    def read_file(self, fileName):
        with open(str(fileName) + ".json", "r", encoding="UTF-8-sig") as fileJson:
            return json.load(fileJson)


class Encryption:

    def __init__(self):
        with open("key.key", "rb") as keyFile:
            self.key = keyFile.read()
        self.f = Fernet(self.key)

    def encrypt_dict(self, dictionary):
        f = Encryption().f
        encryptedDict = {str(f.encrypt(bytes(element, encoding="UTF-8"))):
                         str(f.encrypt(
                             bytes(dictionary[element], encoding="UTF-8")))
                         for element in dictionary
                         }
        return encryptedDict

    def decrypt_dict(self, dictionary):
        f = Encryption().f
        decryptedDict = {f.decrypt(bytes(element.strip("'").replace("b'", ""),
                                         encoding="UTF-8-sig")).decode(encoding="UTF-8-sig"):
                         f.decrypt(bytes(dictionary[element].strip("'").replace("b'", ""),
                                         encoding="UTF-8-sig")).decode(encoding="UTF-8-sig")
                         for element in dictionary
                         }
        return decryptedDict


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

    def sign_in(self):

        credentialsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "credentials"))
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
            password = stdiomask.getpass(
                prompt="Please enter your password: ", mask="*")
            if password != credentialsFile[login]:
                print("Wrong password, please try again")
                continue
            else:
                accountsFile = Encryption.decrypt_dict(
                    self, FileSupport.read_file(self, "Accounts"))
                accountBalance = accountsFile[login]
                self.user = BankAccount(
                    accountBalance, login)
            break

    def sign_up(self):
        # open and decrypt credentials file
        credentialsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "credentials"))
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
        credentialsFile[str(self.user.id)] = password
        FileSupport.save_file(self, Encryption.encrypt_dict(
            self, credentialsFile), "credentials")

        # open accounts file and save it with new account: balance
        accountsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "Accounts"))
        accountsFile[str(self.user.id)] = str(balance)
        FileSupport.save_file(self, Encryption.encrypt_dict(
            self, accountsFile), "Accounts")


class OperationsAccount:

    def __init__(self):

        session = LoginAccount()

        print()
        print("Welcome User No.", session.user.id,
              ", your current balance is:", session.user.balance)

        OperationsMenu = IntEnum(
            "OperationsMenu", "Add Show Transfer Withdraw Logout ChangePassword")

        while True:
            try:
                operationChoice = int(input("""Please choose an option:
1. Add funds
2. Show balance
3. Make transfer
4. Withdraw
5. Logout
6. Change password
"""))
                if operationChoice == OperationsMenu.Add or \
                        operationChoice == OperationsMenu.Show or \
                        operationChoice == OperationsMenu.Transfer or \
                        operationChoice == OperationsMenu.Withdraw or \
                        operationChoice == OperationsMenu.Logout or \
                        operationChoice == OperationsMenu.ChangePassword:

                    if operationChoice == OperationsMenu.Add:
                        OperationsAccount.add_funds(self, session)
                        continue

                    elif operationChoice == OperationsMenu.Show:
                        OperationsAccount.show_balance(self, session)
                        continue

                    elif operationChoice == OperationsMenu.Transfer:
                        OperationsAccount.transfer_funds(self, session)
                        continue

                    elif operationChoice == OperationsMenu.Withdraw:
                        OperationsAccount.withdraw_funds(self, session)
                        continue

                    elif operationChoice == OperationsMenu.Logout:
                        OperationsAccount.log_out(self)
                        continue

                    elif operationChoice == OperationsMenu.ChangePassword:
                        OperationsAccount.change_password(self, session)
                        continue

                else:
                    print("Wrong choice, please try again")
                    continue
            except:
                print("Wrong choice, please try again")
                continue

    def add_funds(self, session):
        while True:
            try:
                fundsToAdd = float(
                    input("Please enter amount to transfer: "))
                break
            except:
                print("Wrong amount, please try again")
                continue
        # read & decrypt file
        accountsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "Accounts"))
        session.user.balance = float(session.user.balance) + fundsToAdd
        accountsFile[session.user.id] = str(session.user.balance)
        # save & encrypt file
        FileSupport.save_file(self, Encryption.encrypt_dict(
            self, accountsFile), "Accounts")
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
        # read & decrypt file
        accountsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "Accounts"))
        balance = float(session.user.balance)
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
        session.user.balance = float(session.user.balance) - amountToTransfer
        accountsFile[str(session.user.id)] = str(session.user.balance)
        accountsFile[str(receiverId)] = str(
            float(accountsFile[str(receiverId)]) + amountToTransfer)
        # save & encrypt file
        FileSupport.save_file(self, Encryption.encrypt_dict(
            self, accountsFile), "Accounts")
        print("Transfer successful, your current balance:",
              session.user.balance)
        _ = input("Press enter to return to menu")
        print()

    def withdraw_funds(self, session):
        # read & decrypt file
        accountsFile = Encryption.decrypt_dict(
            self, FileSupport.read_file(self, "Accounts"))
        while True:
            try:
                amountToWithdraw = float(
                    input("Please enter amount to withdraw: "))
                if amountToWithdraw > float(session.user.balance):
                    print("Not enough funds, please try again")
                break
            except:
                print("Wrong amount, please try again")
                continue
        session.user.balance = float(session.user.balance) - amountToWithdraw
        accountsFile[session.user.id] = str(session.user.balance)
        print(
            "Please collect your money from ATM within next 10 seconds")
        time.sleep(2)
        start = time.perf_counter()
        webbrowser.open_new_tab(
            "https://assets.nigerianchannel.com/wp-content/uploads/2018/12/05111607/Earn-Interest-like-the-banks1.jpg")
        _ = input(
            "Please press enter to confirm")
        end = time.perf_counter()
        if end - start < 10:
            print()
            print("Withdrawal complete, it took you just", round(
                end - start, 2), "seconds to collect you money")
            print("Your balance after withdrawal:",
                  session.user.balance)
            _ = input(
                "Please press enter to return to menu")
            # save & encrypt file
            FileSupport.save_file(self, Encryption.encrypt_dict(
                self, accountsFile), "Accounts")
            print()
        else:
            print()
            print(
                "Too slow. Withdrawal has been canceled, and your money is back on your account")
            session.user.balance = float(
                session.user.balance) + amountToWithdraw
            accountsFile = Encryption.decrypt_dict(
                self, FileSupport.read_file(self, "Accounts"))
            accountsFile[str(session.user.id)] = str(session.user.balance)
            # save & encrypt file
            FileSupport.save_file(self, Encryption.encrypt_dict(
                self, accountsFile), "Accounts")
            print("Your current balance:",
                  session.user.balance)
            _ = input(
                "Please press enter to return to menu")

    def log_out(self):
        print("Goodbye")
        time.sleep(2)
        print()
        OperationsAccount()
        print()

    def change_password(self, session):
        while True:
            currentPassword = stdiomask.getpass(
                prompt="Please confirm your current password to proceed: ", mask="*")
            # read & decrypt file
            credentialsFile = Encryption.decrypt_dict(
                self, FileSupport.read_file(self, "credentials"))
            if credentialsFile[str(session.user.id)] != currentPassword:
                print("Wrong password, please try again")
                continue
            else:
                while True:
                    newPassword1 = stdiomask.getpass(
                        prompt="Please type your new password: ", mask="*")
                    newPassword2 = stdiomask.getpass(
                        prompt="Please type your new password again: ", mask="*")
                    if newPassword1 != newPassword2:
                        print("Passwords don't match, please try again")
                        print()
                        continue
                    else:
                        print(
                            "Passwords match. Your password has been successfully changed")
                        credentialsFile[session.user.id] = newPassword1
                        # save & encrypt file
                        FileSupport.save_file(self, Encryption.encrypt_dict(
                            self, credentialsFile), "credentials")
                        _ = input("Please press enter to return to menu")
                        print()
                        break
                break
