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
    calcs = checking_text[balance:end_balance]
    print(calcs)

    # Extracting transactions from the Checking Summary section
    transactions = re.findall(
        r'(\d{2}/\d{2})\s+(.+?)\s+(-?\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s+(-?\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        calcs
    )

    parsed_transactions = []
    for date, description, amount, balance in transactions:
        # Cleaning up the amount and balance
        amount = amount.replace(',', '').replace('$', '')
        balance = balance.replace(',', '').replace('$', '')

        if '-' in description:
            description = description.replace('-', '').strip()
            amount = '-' + amount

        parsed_transactions.append([date, description.strip(), amount, balance])

    return parsed_transactions

def write_to_csv(transactions, csv_path):
    csv_path = pdf_path.replace('Monthly_Statements', 'Monthly_Transactions').replace('.pdf', '.csv')
    header = ['Date', 'Description', 'Amount', 'Balance']
    df = pd.DataFrame(transactions, columns=header)
    df.to_csv(csv_path, index=False)
    print(f'Transactions have been successfully written to {csv_path}')


if __name__ == "__main__":
    pdf_path = input("Please enter file path to your statement pdf file: ")
    transactions = extract_transactions_from_pdf(pdf_path)
    write_to_csv(transactions, pdf_path)
