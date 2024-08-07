import PyPDF2
import csv
import re
import os
import pandas as pd

def extract_transactions_from_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Extracting transactions from the Checking Summary section
    transactions = re.findall(
        r'(\d{2}/\d{2})\s+(.+?)\s+(-?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(-?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        text
    )

    parsed_transactions = []
    for date, description, amount, balance in transactions:
        # Cleaning up the amount and balance
        amount = amount.replace(',', '').replace('$', '')
        balance = balance.replace(',', '').replace('$', '')

        # Handling the negative sign in amount
        if '-' in description:
            description = description.replace('-', '').strip()
            amount = '-' + amount

        parsed_transactions.append([date, description, amount, balance])

    return parsed_transactions

def write_to_csv(transactions, csv_path):
    csv_path = pdf_path.replace('Monthly_Statements', 'Monthly_Transactions').replace('.pdf', '.csv')
    header = ['Date', 'Description', 'Amount', 'Balance']
    df = pd.DataFrame(transactions, columns=header)
    df.to_csv(csv_path, index=False)
    print(f'Transactions have been successfully written to {csv_path}')

# Path to statement pdf
pdf_path = input("Please enter file path to your statement pdf file: ")

# Process
transactions = extract_transactions_from_pdf(pdf_path)
write_to_csv(transactions, pdf_path)
