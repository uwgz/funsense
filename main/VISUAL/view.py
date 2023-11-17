import pandas as pd
import matplotlib.pyplot as plt
import os

from ..FILES.process_file import get_file_path
from ..SUMMARY.summarize import summarize_transactions


import pandas as pd

def convert_to_datetime(date_column):
    # Define a list of possible date formats
    date_formats = ["%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d"]
    
    # Try to convert the date column to datetime using each format in turn
    for fmt in date_formats:
        try:
            return pd.to_datetime(date_column, format=fmt)
        except ValueError:
            continue
    
    raise ValueError("Unable to convert date column to datetime format")

class Visualize:
    def __init__(self, file_path):
        df = pd.read_csv(file_path, parse_dates=[0])
        df['DATE'] = convert_to_datetime(df['DATE'])
        self.df = df

    def visualize_credits(self):
        self._plot_non_empty_dates('DATE', 'CREDIT AMOUNT', 'Credit Amount over Time')

    def compare_debit_with_debit_paid(self):
        self._visualize_two_cols('DEBIT AMOUNT', 'DEBIT PAID AMOUNT', 'Comparing DEBIT with DEBIT PAID', 'd_dp')
        self._visualize_two_cols('CREDIT AMOUNT', 'DEBIT PAID AMOUNT', 'Comparing CREDIT with DEBIT', 'd_c')

    def _plot_non_empty_dates(self, x_column, y_column, title, kind='line'):
        non_empty_df = self.df.dropna(subset=[x_column, y_column])
        plt.figure(figsize=(10, 6))

        plt.plot(non_empty_df[x_column], non_empty_df[y_column], marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Amount in RWF')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    def _visualize_two_cols(self, column1_name, column2_name, title, what):
        plt.figure(figsize=(12, 6))
        if what == 'd_dp':
            selected_data = self.df.iloc[18:]
            index = selected_data['DATE'].dropna().sort_values().reset_index(drop=True)

            formatted_dates = [date.strftime('%Y-%m-%d') for date in index]

            column1_data = selected_data[column1_name].fillna(0)
            column2_data = selected_data[column2_name].fillna(0)

            data_dict = {
                'DATE': formatted_dates,
                column1_name: column1_data.iloc[:len(formatted_dates)],
                column2_name: column2_data.iloc[:len(formatted_dates)]
            }
            df_plot = pd.DataFrame(data_dict)

            bar_width = 0.6
            plt.bar(df_plot['DATE'], df_plot[column1_name], label=f'{column1_name}', alpha=1, width=bar_width, color='black')
            plt.bar(df_plot['DATE'], df_plot[column2_name], label=f'{column2_name}', alpha=0.7, width=bar_width, color='red', align='edge')
        else:
            self.df['DATE'] = pd.to_datetime(self.df['DATE'])

            # Remove the typo 'self.' from the following line
            self.df = self.df[(self.df['CREDIT AMOUNT'] > 0) | (self.df['DEBIT AMOUNT'] > 0)]
            self.df.set_index('DATE', inplace=True)

            credit_df = self.df[self.df['CREDIT AMOUNT'] > 0]['CREDIT AMOUNT'].sort_index()
            debit_df = self.df[self.df['DEBIT AMOUNT'] > 0]['DEBIT AMOUNT'].sort_index()

            plt.plot(credit_df.index, credit_df.values, label='Credit Amount', marker='o')
            plt.plot(debit_df.index, debit_df.values, label='Debit Amount', marker='o')

        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title(title)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()



def see_statement():
    file_path = get_file_path()
    summarize_transactions(file_path)