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
            if float(amount) < 0.0:
                total_expenses += abs(float(amount))

    return [date[0:2], total_expenses]

def update_expenses(json_path, total_expenses):
    expense_data = {}
    if os.path.exists(json_path):
        with open(json_path, 'r') as json_file:
            expense_data = json.load(json_file)
            month = int(total_expenses[0])
    expense_data[month] = total_expenses[1]
    with open(json_path, 'w') as json_file:
        json.dump(expense_data, json_file, indent = 4)
        

if __name__ == '__main__':
    json_file_path = "/Users/arhan.sheth/Documents/Codes/Projects/Personal_Finance_Tracker/Yearly_Expenses/2024.json"
    question = input("Is your statement file in PDF or CSV format? : ")
    if question.lower() == 'pdf':
        pdf_file = input("Input path of statement pdf file: ")
        transactions = pdf2csv_converter.extract_transactions_from_pdf(pdf_file)
        csv_path = pdf2csv_converter.write_to_csv(transactions, pdf_file)
        expense = monthly_expenses(csv_path)
        print(expense)
        update_expenses(json_file_path, expense)
    elif question.lower() == 'csv':
        csv_file = input("Input path of statement csv file: ")
        expense = monthly_expenses(csv_file)
        update_expenses(json_file_path, expense)
    else: 
        print("Wrong Input, Try Again.")