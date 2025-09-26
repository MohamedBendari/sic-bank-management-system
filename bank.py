import json
import sys

### ---------------------- Load Data()----------------------
with open("data.json") as f:
    data = json.load(f)
# ---------------------- Save Data() ----------------------
def save_data():
    with open('data.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)

user_id = None


# ---------------------- Login Page ()----------------------
def login_page():
    global user_id
    print('<-------- Welcome to Login Page -------->')

    while True:
        try:
            user_id = int(input('Please Enter Your ID: '))
        except ValueError:
            print("✘ Error: Please enter a valid number for ID.")
            continue

        if user_id > len(data):
            print("You don't have an Account")
            register_page()
            break

        password = input('Please Enter Your Password: ')

        if data[user_id - 1]["password"] == password:
            user_page()
            break
        else:
            print('✘ Invalid Password ✘')
            print('[0] Try Again\n[1] Forget Password:')
            choice = input()

            if choice == '0':
                continue
            elif choice == '1':
                try:
                    user_id = int(input('Please Enter Your ID: '))
                except ValueError:
                    print("✘ Error: Please enter a valid number for ID.")
                    continue

                email = input('Please Enter Your Email: ')
                if data[user_id - 1]["email"] == email:
                    print("Your password is:", data[user_id - 1]["password"], "Don't Forget !!")
                    user_page()
                else:
                    print('Invalid email ✘, login again 🔄')
                    continue


# ---------------------- Register Page() ----------------------
def register_page():
    global user_id
    print('<------ Welcome to Sign Up Page ------>')

    name = input('Please enter your name: ')
    password = input('Please enter your password: ')
    phone = input('Please enter your phone number: ')
    mail = input('Please enter your email: ')
    gender = input('Please enter your gender: ')
    age = input('Please enter your age: ')
    city = input('Please enter your city: ')

    try:
        user_id = data[-1]['id'] + 1
    except IndexError:
        user_id = 1

    data_dic = {
        "name": name,
        "password": password,
        "phone": phone,
        "email": mail,
        "gender": gender,
        "age": age,
        "city": city,
        "id": user_id,
        "balance": 0,
        "history": []
    }

    data.append(data_dic)
    save_data()



    print(f"Sign Up successfully ✔, your account ID: {user_id}")
    user_page()


# ---------------------- Deposit Page() ----------------------
def deposit_page():
    global user_id
    user_input = input("Enter the amount you want to deposit (Format '1 EGP'): ")

    parts = user_input.split()
    if len(parts) != 2:
        print("✘ Error: Please enter in the correct format, '5 EGP'")
        return deposit_page()

    try:
        amount = float(parts[0])
    except ValueError:
        print("✘ Error: Amount must be a number.")
        return deposit_page()

    currency = parts[1].upper()

    if currency == 'EGP':
        amount_egp = amount
    elif currency == 'USD':
        amount_egp = amount * 50
    elif currency == 'SAR':
        amount_egp = amount * 10
    else:
        print("✘ Error: Currency must be EGP, USD, or SAR.")
        return deposit_page()

    data[user_id - 1]["balance"] += amount_egp


    data[user_id - 1]["history"].append({
        "type": "deposit",
        "amount": amount,
        "currency": currency,
        "balance_after": data[user_id - 1]["balance"]
    })

    save_data()

    print(f"{user_input} Was Deposited Successfully!")
    print(f"Your Balance is {data[user_id - 1]['balance']} EGP")


# ---------------------- Withdraw Page() ----------------------
def withdraw_page():
    global user_id
    while True:
        user_input = input(f"Enter the amount to withdraw (Balance: {data[user_id - 1]['balance']}), Format '1 EGP': ")

        parts = user_input.split()
        if len(parts) != 2:
            print("✘ Error: Please enter in the correct format, '5 EGP'")
            continue

        try:
            amount = float(parts[0])
        except ValueError:
            print("✘ Error: Amount must be a number.")
            continue

        currency = parts[1].upper()

        if currency == 'EGP':
            amount_egp = amount
        elif currency == 'USD':
            amount_egp = amount * 50
        elif currency == 'SAR':
            amount_egp = amount * 10
        else:
            print("✘ Error: Currency must be EGP, USD, or SAR.")
            continue

        if amount_egp > data[user_id - 1]['balance']:
            print("*--- You don't have enough money ✘, Try Again ---*")
            return user_page()

        password = input("Enter password to confirm: ")
        if password != data[user_id - 1]['password']:
            print("Incorrect password.")
            return user_page()

        data[user_id - 1]["balance"] -= amount_egp


        data[user_id - 1]["history"].append({
            "type": "withdraw",
            "amount": amount,
            "currency": currency,
            "balance_after": data[user_id - 1]["balance"]
        })

        save_data()

        print(f"{user_input} Was Withdrawn Successfully ✔")
        print(f"Your Balance is {data[user_id - 1]['balance']} EGP")
        break


# ---------------------- Transfer Page() ----------------------
def Transfer_page():
    global user_id
    while True:
        user_input = input(f"Enter the amount to transfer (Balance: {data[user_id - 1]['balance']})EGP, Format '1 EGP': ")

        parts = user_input.split()
        if len(parts) != 2:
            print("✘ Error: Please enter in the correct format, '5 EGP'")
            continue

        try:
            amount = float(parts[0])
        except ValueError:
            print("✘ Error: Amount must be a number.")
            continue

        currency = parts[1].upper()

        transfer_id = input("Enter the Account ID: ")
        if not transfer_id.isdigit():
            print("✘ Error: Account ID must be a number.")
            continue

        transfer_id = int(transfer_id)
        if currency == 'EGP':
            amount = amount
        elif currency == 'USD':
            amount = amount * 50
        elif currency == 'SAR':
            amount = amount * 10
        else:
            print("✘ Error: Currency must be EGP, USD, or SAR.")
            continue

        if transfer_id > len(data) or transfer_id == user_id:
            print("Invalid ID, Try Again 🔄")
            continue

        if amount > data[user_id - 1]['balance']:
            print("*--- You don't have enough money ✘, Try Again ---*")
            return user_page()

        data[user_id - 1]["balance"] -= amount
        data[transfer_id - 1]["balance"] += amount


        data[user_id - 1]["history"].append({
            "type": "transfer",
            "amount": amount,
            "currency": currency,
            "balance_after": data[user_id - 1]["balance"],
            "target_account": transfer_id
        })

        save_data()

        print(f"{user_input} Was Transferred Successfully! to account_id: {transfer_id}")
        print(f"Your Balance is {data[user_id - 1]['balance']} EGP")
        break


# ---------------------- Info Page() ----------------------
def info_page():
    global user_id
    print('*------------- Your Info -----------------*')
    print('ID: ', data[user_id - 1]['id'])
    print('Name: ', data[user_id - 1]['name'])
    print('Phone: ', data[user_id - 1]['phone'])
    print('Email: ', data[user_id - 1]['email'])
    print('Gender: ', data[user_id - 1]['gender'])
    print('Age:', data[user_id - 1]['age'])
    print('City: ', data[user_id - 1]['city'])
    print('Balance: ', data[user_id - 1]['balance'])
    user_page()


# ---------------------- History Page() ----------------------
def history_page():
    global user_id
    if "history" not in data[user_id - 1] or len(data[user_id - 1]["history"]) == 0:
        print("No transactions found.")
        return user_page()

    print("\n<---------------- Transaction History ---------------->")
    print(f"{'Type':<15} {'Amount':<10} {'Currency':<8} {'Balance After':<15} {'Target':<10}")
    print("-" * 65)

    for transaction in data[user_id - 1]["history"]:
        t_type = transaction.get("type", "")
        amount = transaction.get("amount", 0)
        currency = transaction.get("currency", "")
        balance = transaction.get("balance_after", 0)
        target = transaction.get("target_account", "--")
        print(f"{t_type:<15} {amount:<10} {currency:<8} {balance:<15} {target}")

    print("-" * 65)
    user_page()


# ---------------------- User Page() ----------------------
def user_page():
    while True:
        print(f'<------ Welcome {data[user_id - 1]["name"]} id:{user_id} ------>')
        print('[0] Deposit')
        print('[1] Withdraw')
        print('[2] Transfer')
        print('[3] Check balance & personal info')
        print('[4] Show history')
        print('[5] Log Out')
        print('[6] Exit')

        choice = input()
        match choice:
            case '0':
                deposit_page()
            case '1':
                withdraw_page()
            case '2':
                Transfer_page()
            case '3':
                info_page()
            case '4':
                history_page()
            case '5':
                login_page()
            case '6':
                sys.exit()


# ---------------------- Program Start(Ahmad) ----------------------
print('\n************************* Welcome to SIC Bank Management System ***********************************\n')
print('If you already have an account please enter: "login" 🔑')
print('If you don\'t have an account enter: "register" 📝')

while True:
    choice = input('▶️').lower()
    if choice == 'login':
        login_page()
    elif choice == 'register':
        register_page()
    else:
        print("Invalid Choice ✘, Try Again:")
