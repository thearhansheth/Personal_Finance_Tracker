import PyPDF2
import csv
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def parse_transactions(text):
    transactions = re.findall(r'(\d{2}/\d{2})\s+(.+?)\s+(-?\$?\d+,\d+\.\d+)\s+(-?\$?\d+,\d+\.\d+)', text, re.DOTALL)
    parsed_transactions = []
    for date, description, amount, balance in transactions:
        amount = amount.replace(',', '').replace('$', '')
        balance = balance.replace(',', '').replace('$', '')
        description = re.sub(r'\s+', ' ', description.strip())
        parsed_transactions.append([date, description, amount, balance])
    return parsed_transactions

def write_to_csv(transactions, csv_path):
    csv_path = pdf_path.replace('Monthly_Statements', 'Monthly_Transactions').replace('.pdf', '.csv')
    header = ['Date', 'Description', 'Amount', 'Balance']
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(transactions)
    print(f'Transactions have been successfully written to {csv_path}')

# Path to statement pdf
pdf_path = input("Please enter file path to your statement pdf file: ")

# Process
text = extract_text_from_pdf(pdf_path)
transactions = parse_transactions(text)
write_to_csv(transactions, pdf_path)
