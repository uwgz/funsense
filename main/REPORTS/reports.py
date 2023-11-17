import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime


from ..FILES.process_file import get_file_path


def view_weakly_monthly_yearly():
    file_path = get_file_path()
    df = pd.read_csv(file_path, parse_dates=[0], infer_datetime_format=True)
    df["MONTH"] = pd.to_datetime(df["DATE"]).dt.month
    df["YEAR"] = pd.to_datetime(df["DATE"]).dt.year

#==========================================================================================
    print("\n")
    print("Monthly Report:")
    print("*"*100)
    grouped_by_month = df.groupby('MONTH')
    monthly_report = grouped_by_month[["CREDIT AMOUNT", "DEBIT AMOUNT"]].sum()
    print(monthly_report.to_string(header=True, index=True))
    #********************************************************************************
    # FOR MONTHLY. (credit)
    plt.bar(monthly_report.index, monthly_report['CREDIT AMOUNT'])
    plt.xlabel('Months')
    plt.ylabel('Credit Amount')
    plt.title('Credit Amount by Month (Histogram)')
    plt.show()
    #********************************************************************************
    # HISTOGRAM FOR MONTHLY. (credit)
    plt.bar(monthly_report.index, monthly_report['DEBIT AMOUNT'])
    plt.xlabel('Months')
    plt.ylabel('Debit Amount')
    plt.title('Debit Amount by Month (Histogram)')
    plt.show()
#==========================================================================================
    print("\nYearly Report:")
    print("*"*100)
    grouped_by_year = df.groupby('YEAR')
    year_report = grouped_by_year[["CREDIT AMOUNT", "DEBIT AMOUNT"]].sum()
    print(year_report.to_string(header=True, index=True))
    print("*"*100)
    
#==========================================================================================
    df["DATE"] = pd.to_datetime(df["DATE"])
    current_week_number = datetime.datetime.now().isocalendar()[1]
    this_week_data = df[df["DATE"].dt.isocalendar().week == current_week_number]
    print("\nWeekly Report:")
    print("*"*100)
    this_week_report = this_week_data[["CREDIT AMOUNT", "DEBIT AMOUNT"]].sum()
    print(this_week_report.to_string(header=True, index=True))
#==========================================================================================



def get_path_to_save_report():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_c_path = os.path.dirname(current_dir)
    file_path = os.path.join(folder_c_path, 'REPORTS', 'FUNSENSE_REPORT.csv')

    return file_path