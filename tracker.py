import os
import csv
import json
import pdf2csv_converter

def monthly_expenses(csv_file_path):
    total_expenses = 0.0
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            date, description, amount, balance = row
            if amount < 0:
                total_expenses += abs(float(amount))

    return total_expenses


print("Is your statement in CSV or PDF format?")
question = input("Click 1 for CSV and 2 for PDF")
if question == 1:
    pdf_file = input("Input path of statement pdf file: ")
    transactions = pdf2csv_converter.extract_transactions_from_pdf(pdf_file)
    csv_path = pdf2csv_converter.write_to_csv(transactions, pdf_file)
    monthly_expenses(csv_path)
elif question == 2:
    csv_file = input("Input path of statement csv file: ")
    monthly_expenses(csv_file)
else: 
    print("Wrong Input, Try Again.")