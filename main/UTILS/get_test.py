import random
import datetime
from ..FILES.process_file import get_previous_balance, get_file_path, save_to_csv
from ..VISUAL.view import Visualize, see_statement
from ..REPORTS.reports import view_weakly_monthly_yearly


def get_valid_date():
    while True:
        user_date = input("Enter the date in the format 'YYYY/MM/DD' (or 'q' to quit): ")
        if user_date.lower() == 'q':
            return 'q'
        
        try:
            date_obj = datetime.datetime.strptime(user_date, '%Y/%m/%d')
            if date_obj < datetime.datetime.now():
                return user_date
            else:
                print(f"Specified date is not in the past. Current date is {datetime.datetime.now().strftime('%Y/%m/%d')}")
        except ValueError:
            print("Invalid date format. Please enter the date in 'YYYY/MM/DD' format.")



def get_valid_time():
    while True:
        user_time = input("Enter the time in the format 'HH:MM:SS' (or 'q' to quit): ")
        if user_time.lower() == 'q':
            return 'q'
        
        try:
            datetime.datetime.strptime(user_time, '%H:%M:%S')
            return user_time
        except ValueError:
            print("Invalid time format. Please enter the time in 'HH:MM:SS' format.")


def get_valid_amount(prompt):
    while True:
        amount = input(prompt)
        if amount.lower() == 'q':
            return 'q'
        if not amount.isdigit():
            print("Please enter a valid amount (a positive integer) or 'q' to quit.")
        else:
            return float(amount)


def get_balance(transaction, credit_am, debit_am, debit_paid, how_much_should_remain = 100):
    if transaction == '1':  # If a user wants to withdraw.
        old_balance = get_previous_balance()

        if old_balance is None:
            return None

        if debit_am >= old_balance + how_much_should_remain:
            print(f"\nYour saving amount is {old_balance} RWF")
            return None
        else:
            print(f"You had {old_balance} RWF")
    else:
        old_balance = get_previous_balance()
        if old_balance:
            print(f"You had {old_balance} RWF")
        else:
            old_balance = 0
            print(f"You had {old_balance} RWF")
            
    remaining_balance = old_balance + credit_am - debit_am + debit_paid
    print(f"After this transaction, your new balance will be {remaining_balance} RWF.")
    return remaining_balance


def display_confirm(type_trnsctn, date, time, amount, name, reason):
    print("\n          TRANSACTION CONFIRMATION BOX")
    print("'''''''''''''''''''''''''''''''''''''''''''''''")
    transaction_types = { '1': 'DEBIT',
                         '2': 'CREDIT',
                         '3': 'DEBIT PAID'
    }
    
    print(f"TRANSACTION TYPE :{transaction_types[type_trnsctn]}")
    print(f"Date_____________:{date}")
    print(f"TIME_____________:{time}")
    print(f"AMOUNT___________:{amount} RWF")
    print(f"DEBITOR/CREDITOR :{name}")
    print(f"REASON___________:{reason}")
    
    confirmation = input("Is the information correct? ('yes' or 'no'): ").lower()
    
    if confirmation not in ('yes', 'no'):
        print("Incorrect choice. Confirm by entering 'YES' OR 'NO'.")
        return display_confirm(type_trnsctn, date, time, amount, name, reason)
    else:
        if confirmation == 'yes':
            return True
        else:
            return False


def human_verification():
    print("Verify you are not a robot.\n'''''''''''''''''''''''''''")
    attempts = 0
    while attempts < 3:
        random_numbers = [str(random.randint(25, 65)) for _ in range(3)]
        print(" | ".join(random_numbers))
        picked_number = random.choice(random_numbers)
        user_input = input(f"Enter {picked_number}: ")
        if user_input == picked_number:
            print("Correct! Access granted.")
            return True
        else:
            print("Invalid number. Try again.")
            attempts += 1
    print("Access denied. Too many incorrect attempts.")
    return False



def more_transaction():
    answer = input("Would you like to add more transaction? (yes or no) or 'q' to quit: ").lower()
    if answer not in ('yes', 'no', 'q'):
        return more_transaction()
    if answer == 'no' or answer == 'q':
        return False
    else:
        return True


def create_visual():
    file_path = get_file_path()
    visualizer = Visualize(file_path)
    
    visualizer.visualize_credits()
    
    visualizer.compare_debit_with_debit_paid()
    
    view_weakly_monthly_yearly()




def request_user():
    enough_fund = True
    if human_verification(): # Check whether the user is not a robot.
#======================================================================================================================================================================================================
        while True:
            if enough_fund:
                print("\nSelect an option:"), print("1: To add TODAY'S transaction"), print("2: To add OLD transaction "), print("V: Visualize transactions over time."), print("S: For summary (statement)."), print("Enter 'q' to quit.")
                when = input("Enter your choice: ").upper()

                if when.lower() == 'q':
                    break
                else:
                    if when not in ('1', '2', 'V', 'S'):
                        print("\nPlease enter 1, 2, V, S, or 'q' to quit.")
                        continue
                    if when == '1': # Recording to days's transaction.
                        print("\nProceeding to recording to days's transaction...")
                        current_datetime = datetime.datetime.now()
                        date = current_datetime.strftime('%Y/%m/%d')
                        time = current_datetime.strftime('%H:%M:%S')
                    elif when == 'V':
                        create_visual()
                        enough_fund = more_transaction()
                        break
                    elif when == 'S':
                        see_statement()
                        enough_fund = more_transaction()
                        break
                    else: # recording old transaction

                        # Get valid date and time from the user
                        date = get_valid_date()
                        if date == 'q':
                            break

                        time = get_valid_time()
                        if time == 'q':
                            break
#======================================================================================================================================================================================================
                    while True:
                        print("Select an option:"), print("1. Debit Account"), print("2. Credit Account"), print("3. Record Debit Paid"), print("Press 'q' to quit.")

                        user_choice = input("Enter your choice: ")

                        if user_choice.lower() == 'q':
                            print("Thank you for using our service.")
                            break
                        else:
                            if user_choice not in ('1', '2', '3'):
                                print("\nPlease enter 1, 2, 3, or 'q' to quit.")
                                continue

                            if user_choice == '1':                                                      # Debitting Account
                                debit_amount = get_valid_amount("Enter debit amount (or 'q' to quit): ")
                                if debit_amount == 'q':
                                    break

                                debitor = input("Who's the debitor: ").upper()
                                debit_reason = input("Enter debit reason: ").upper()
                                if display_confirm('1', date, time, debit_amount, debitor, debit_reason):
                                    credit_amount, creditor, credit_reason, debit_paid, debit_payer, debit_paid_reason = 0, '', '', 0, '', ''
                                else:
                                    continue

                            elif user_choice == '2':                                                    # Creditting Account
                                credit_amount = get_valid_amount("Enter credit amount (or 'q' to quit): ")
                                if credit_amount == 'q':
                                    break
                                creditor = input("Who's the creditor: ").upper()
                                credit_reason = input("Enter credit reason: ").upper()
                                if display_confirm('2', date, time, credit_amount, creditor, credit_reason):
                                    debit_amount, debitor, debit_reason, debit_paid, debit_payer, debit_paid_reason = 0, '', '', 0, '', ''
                                else:
                                    continue
                            else:  # user_choice == '3'  # Record Debit Paid
                                debit_paid = get_valid_amount("Enter debit paid amount (or 'q' to quit): ")
                                if debit_paid == 'q':
                                    break
                                debit_payer = input("Who pays back?: ").upper()
                                debit_paid_reason = "PAYBACK"

                                if display_confirm('3', date, time, debit_paid, debit_payer, debit_paid_reason):
                                    debit_amount, debitor, debit_reason, credit_amount, creditor, credit_reason = 0, '', '', 0, '', ''
                                else:
                                    continue
#======================================================================================================================================================================================================
                            balance = get_balance(user_choice, credit_amount, debit_amount, debit_paid)
                            if balance: # If balance is not none
                                save_to_csv(date, time, credit_amount, creditor, credit_reason, debit_amount, debitor, debit_reason, debit_paid, debit_payer, debit_paid_reason, balance)
                                enough_fund = more_transaction()
                                break # Exit the inner loop after saving the transaction.
                            else: 
                                print("\nYou don't have enough balance to perform this transaction.")
                                enough_fund = False
                                break
            else:
                break