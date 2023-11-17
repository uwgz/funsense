import os
import pandas as pd


from ..REPORTS.reports import get_path_to_save_report


def calculate_debts(df, n_stars = 30, t_to_be_paid = 0):
    print('\n\n\n', '*'*n_stars)
    
    debts = {}

    for index, row in df.iterrows():
        debitor = row['DEBITOR']
        payer = row['DEBIT PAYER']
        amount = row['DEBIT AMOUNT']
        paid_amount = row['DEBIT PAID AMOUNT']

        if not pd.isnull(debitor):
            debts[debitor] = debts.get(debitor, 0) + amount
    
        if not pd.isnull(payer):
            debts[payer] = debts.get(payer, 0) - paid_amount

    # For someone who has paid without being debited
    for debtor, amount in debts.items():
        if amount < 0:
            print("Warning: {} has paid {} RWF without being debited.".format(debtor, abs(amount)))

    print('*'*n_stars)
    for key, value in debts.items():
        if value < 0:
            print("Warning: {} has paid {} RWF without being debited.".format(debtor, abs(amount)))
            t_to_be_paid += value
        else:
            if key == 'FUNSENSE':
                print(value, 'RWF have been used to pay employees\' salary')
                print('*'*n_stars)
            else:
                print(key, 'owes', value, 'RWF')
                print('*'*n_stars)
                t_to_be_paid += value
    print(f"\nTotal to be paid is {t_to_be_paid} RWF."), print("\nYour balance is ", df['BALANCE'].iloc[-1], "RWF")
    report_columns = ['DATE', 'CREDIT AMOUNT', 'DEBIT AMOUNT', 'DEBIT PAID AMOUNT', 'BALANCE']
    report_df = df[report_columns]
    print('*'*n_stars)

    path_to_save = get_path_to_save_report()
    report_df.to_csv(path_to_save, index=False)
    print("Refer to the a file with name 'FUNSENSE_REPORT.csv' in REPORTS Folder for more detail."), print()



def display_summary(df, credited_df, debited_df, debit_paid_df):
    print("\n                                               CREDIT SUMMARY:")
    for idx, row_credit in credited_df.iterrows():
        print(f"\n                        {row_credit['CREDITOR']} (CREDITED = {row_credit['CREDITED']})                        ")
        print("_________________________________________________________________________________________________")
        print("|    NO    |        DATE              |    AMOUNT          |   REASON                              |")
        print("-------------------------------------------------------------------------------------------------")
        for i, (date, amount, reason) in enumerate(zip(row_credit['DATES'], row_credit['AMOUNTS'], row_credit['REASONS']), 1):
            print(f"|  {i}.    |      {date}           |    {amount} RWF        |     {reason}                  |")
            print("-------------------------------------------------------------------------------------------------")


    print("\n                                               DEBIT SUMMARY:")
    for idx, row_debit in debited_df.iterrows():
        print(f"\n                         {row_debit['DEBITOR']} (DEBITED = {row_debit['DEBITED']})   ")
        print("_________________________________________________________________________________________________")
        print("|    NO    |        DATE              |    AMOUNT          |   REASON                              |")
        print("-------------------------------------------------------------------------------------------------")
        for i, (date, amount, reason) in enumerate(zip(row_debit['DATES'], row_debit['AMOUNTS'], row_debit['REASONS']), 1):
            print(f"|   {i}.  |      {date}                |    {amount} RWF            |     {reason}            |")
            print("-----------------------------------------------------------------------------------------------")
            
            
    print("\n                                               DEBIT PAID SUMMARY:")
    for idx, row_debit_paid in debit_paid_df.iterrows():
        print(f"\n                         {row_debit_paid['DEBIT PAYER']} (PAID = {row_debit_paid['DEBITED']})   ")
        print("_________________________________________________________________________________________________")
        print("|    NO    |        DATE              |    AMOUNT          |   REASON                              |")
        print("-------------------------------------------------------------------------------------------------")
        for i, (date, amount, reason) in enumerate(zip(row_debit_paid['DATES'], row_debit_paid['AMOUNTS'], row_debit_paid['REASONS']), 1):
            print(f"|   {i}.  |      {date}                |    {amount} RWF            |     {reason}            |")
            print("-----------------------------------------------------------------------------------------------")
    
    return calculate_debts(df)


def summarize_transactions(file_path):
    df = pd.read_csv(file_path, parse_dates=[0], infer_datetime_format=True)
    
    df['DATE'] = pd.to_datetime(df['DATE'])
    
    credited_df = df[df['CREDIT AMOUNT'] > 0].groupby(['CREDITOR']).agg(
        CREDITED=('CREDIT AMOUNT', 'sum'),
        CREDIT_COUNT=('CREDIT AMOUNT', 'count'),
        DATES=('DATE', lambda x: x.dt.strftime('%d/%m/%Y').tolist()),
        AMOUNTS=('CREDIT AMOUNT', lambda x: x.tolist()),
        REASONS=('CREDIT REASON', lambda x: x.tolist())
    ).reset_index()

    debited_df = df[df['DEBIT AMOUNT'] > 0].groupby(['DEBITOR']).agg(
        DEBITED=('DEBIT AMOUNT', 'sum'),
        DEBIT_COUNT=('DEBIT AMOUNT', 'count'),
        DATES=('DATE', lambda x: x.dt.strftime('%d/%m/%Y').tolist()),
        AMOUNTS=('DEBIT AMOUNT', lambda x: x.tolist()),
        REASONS=('DEBIT REASON', lambda x: x.tolist())
    ).reset_index()
    
    
    debited_paid_df = df[df['DEBIT PAID AMOUNT'] > 0].groupby(['DEBIT PAYER']).agg(
        DEBITED=('DEBIT PAID AMOUNT', 'sum'),
        DEBIT_COUNT=('DEBIT PAID AMOUNT', 'count'),
        DATES=('DATE', lambda x: x.dt.strftime('%d/%m/%Y').tolist()),
        AMOUNTS=('DEBIT PAID AMOUNT', lambda x: x.tolist()),
        REASONS=('DEBIT PAYER REASON', lambda x: x.tolist())
    ).reset_index()

    return display_summary(df, credited_df, debited_df, debited_paid_df)