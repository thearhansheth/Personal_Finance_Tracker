import pdfplumber
import csv
import re
import os
import pandas as pd

def extract_transactions_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    checking_start = text.find("CHECKING SUMMARY")
    savings_start = text.find("SAVINGS SUMMARY")

    if checking_start == -1 or savings_start == -1:
        raise ValueError("Could not find the Checking Summary or Savings Summary sections in the PDF")

    checking_text = text[checking_start:savings_start]
    balance = checking_text.find("TRANSACTION DETAIL")
    end_balance = checking_text.find("CHASE SAVINGS")

    transaction_text = checking_text[balance:end_balance]
    lines = transaction_text.split('\n')
    
    transactions = []
    for line in lines:
        match = re.match(r'(\d{2}/\d{2})\s+(.+?)\s+(-?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(-?\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)
        if match:
            date, description, amount, balance = match.groups()
            amount = amount.replace(',', '').replace('$', '')
            balance = balance.replace(',', '').replace('$', '')

            if '-' in amount:
                amount = '-' + amount.replace('-', '').strip()

            transactions.append([date, description.strip(), amount, balance])

    return transactions

def write_to_csv(transactions, pdf_path):
    csv_path = pdf_path.replace('Monthly_Statements', 'Monthly_Transactions').replace('.pdf', '.csv')
    header = ['Date', 'Description', 'Amount', 'Balance']
    df = pd.DataFrame(transactions, columns=header)
    df.to_csv(csv_path, index=False)
    print(f'Transactions have been successfully written to {csv_path}')
    return csv_path

    
