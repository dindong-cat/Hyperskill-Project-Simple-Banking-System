# Write your code here
import random
import sqlite3
card_pool = {}
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

if len(card_pool) == 0:
    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')

def menu():
    x = input("""1. Create an account
2. Log into account
0. Exit
""")
    while x:
        if x == "0":
            print("\nBye!")
            break
        elif x == "1":
            create_acc()
            break
        elif x == "2":
            login()
            break
        else:
            print("wrong input!")
            x = input("""1. Create an account
2. Log into account
0. Exit
""")




def create_acc():
    customer_account_number = str(random.randrange(0, 1000000000))
    customer_account_number = ("0" * (9 - len(customer_account_number))) + customer_account_number
    card_number = f"400000{customer_account_number}{random.randrange(0, 9)}"
    y = card_number[:-1]
    y = [2 * int(y[i]) if i==0 or i%2==0 else int(y[i]) for i in range(len(y))]
    y = [(i - 9) if i > 9 else i for i in y]
    z = sum(y) + int(card_number[-1:])
    if z % 10 == 0:
        while card_number not in card_pool:
            print("\nYour card has been created")
            print("Your card number:")
            print(card_number)
            pin = random.randrange(0, 10000)
            pin = ("0" * (4 - len(str(pin)))) + str(pin)
            print("Your card PIN:")
            print(f"{pin}\n")
            card_pool[card_number] = {"pin":pin, "balance":0}
            cur.execute('INSERT INTO card (id, number, pin) VALUES (?, ?, ?);', (len(card_pool), card_number, pin))
            conn.commit()
            menu()
    else:
        create_acc()


def login():
    login = input("\nEnter your card number:")
    pin = input("Enter your PIN:")
    if login in card_pool.keys():
        if card_pool[login]["pin"] == pin:
            print("\nYou have successfully logged in!")
            menu_2(login)
        else:
            print("\nWrong card number or PIN!\n")
            menu()
    else:
        print("\nWrong card number or PIN!\n")
        menu()


def menu_2(login):
    x = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
    while x:
        if x == "0":
            print("\nBye!")
            break
        elif x == "1":
            print(f'\nBalance: {card_pool[login]["balance"]}\n')
            x = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
        elif x == "2":
            income = int(input("\nEnter income:\n"))
            card_pool[login]["balance"] += income
            cur.execute('UPDATE card SET balance=? WHERE number=?;', (card_pool[login]["balance"], login,))
            conn.commit()
            print("Income was added!\n")
            x = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
        elif x == "3":
            print("\nTransfer")
            transfer_target = input("Enter card number:\n")
            checking = transfer_target[:-1]
            checking = [2 * int(checking[i]) if i==0 or i%2==0 else int(checking[i]) for i in range(len(checking))]
            checking = [(i - 9) if i > 9 else i for i in checking]
            checking = sum(checking) + int(transfer_target[-1:])
            if checking % 10 != 0:
                print("Probably you made a mistake in the card number. Please try again!\n")
            else:
                if transfer_target not in card_pool.keys():
                    print("Such a card does not exist.\n")
                else:
                    wanna_transfer = int(input("Enter how much money you want to transfer:\n"))
                    if wanna_transfer > card_pool[login]["balance"]:
                        print("Not enough money!\n")
                    else:
                        cur.execute('UPDATE card SET balance=balance-? WHERE number=?', (wanna_transfer, login,))
                        conn.commit()
                        cur.execute('UPDATE card SET balance=balance+? WHERE number=?', (wanna_transfer, transfer_target,))
                        conn.commit()
                        card_pool[login]["balance"] -= wanna_transfer
                        card_pool[transfer_target]["balance"] += wanna_transfer
                        print("Success!\n")
            x = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
        elif x == "4":
            print("The account has been closed!\n")
            cur.execute('DELETE FROM card WHERE number=?', (login,))
            conn.commit()
            #del card_pool[str(login)]
            menu()
            break
        elif x == "5":
            print("\nYou have successfully logged out!\n")
            menu()
            break



menu()
conn.close()
