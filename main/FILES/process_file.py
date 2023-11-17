import os
import pandas as pd


def save_to_csv(date, time, credit_amount, creditor, credit_reason, debit_amount, debitor, debit_reason, debit_paid, debit_payer, debit_payer_reason, balance):
    data = {
        'DATE': [date],
        'TIME': [time],
        'CREDIT AMOUNT': [credit_amount],
        'CREDITOR': [creditor],
        'CREDIT REASON': [credit_reason],
        'DEBIT AMOUNT': [debit_amount],
        'DEBITOR': [debitor],
        'DEBIT REASON': [debit_reason],
        'DEBIT PAID': [debit_paid],
        'DEBIT PAYER': [debit_payer],
        'DEBIT PAYER REASON': [debit_payer_reason],
        'BALANCE': [balance]
    }
    
    filename = get_file_path()
    if not os.path.exists(filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', header=False, index=False)



def get_previous_balance():
    try:
        file_path = get_file_path()
        df = pd.read_csv(file_path)
        prev_balance = df['BALANCE'].iloc[-1]
        return prev_balance
    except FileNotFoundError:
        return None



def get_file_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_c_path = os.path.dirname(current_dir)
    file_path = os.path.join(folder_c_path, 'FILES', 'FUNSENSE.csv')

    return file_path