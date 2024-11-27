# Transaction Tracker - JamilJamblungz

Welcome to **JamilJamblungz** — a simple yet powerful web application designed to help you track and manage your income and expenses effortlessly. This app allows you to upload your transactions in CSV format or manually input them, and it provides an overview of your financial status in real-time.

## Features

- **Track Transactions:** Upload your CSV file or add transactions manually.
- **Expense Categories:** Choose from various categories such as Rent, Groceries, Entertainment, etc.
- **Income Categories:** Track your salary, bonus, investment income, and more.
- **Rupiah Format:** Automatically formats amounts into the Indonesian Rupiah (Rp).
- **Financial Overview:** Displays your total income, expenses, and remaining balance.
- **Download CSV:** Easily download your updated transaction data.

## How to Use

### 1. Upload CSV File

1. Start by uploading your CSV file containing your transaction data. You can upload a file by clicking the **"Upload your transactions CSV"** button.
   
   - **CSV Format:** The file should contain at least the following columns:
     - `Category` - The category of the transaction (e.g., Salary, Rent, etc.)
     - `Amount` - The monetary value of the transaction (formatted as "Rp xxx.xxx").
     - `Date` - The date the transaction occurred.
     - `Type` - The type of transaction (Income or Expense).

### 2. Add New Transactions Manually

If you prefer to add transactions manually, follow these steps:

1. **Select the Type of Transaction:** Choose whether the transaction is an "Income" or "Expense."
   
2. **Select the Category:** Based on the type of transaction selected, pick a category from the list (e.g., Rent for Expenses, Salary for Income).

3. **Enter the Amount:** Enter the amount in **Rupiah (Rp)**. The app will automatically format the number as you type.

4. **Select the Date:** Choose the date when the transaction occurred.

5. Click **"Add Transaction 📝"** to add the transaction to your records.

### 3. View and Analyze Your Transactions

After uploading or adding transactions, you will see them displayed in a table format. The amount will be formatted in **Rupiah**.

- **Download CSV:** You can download the updated transaction list by clicking on the **"Download Transactions as CSV 📥"** button. The file will be downloaded as `transactions.csv`.
  
### 4. Financial Overview

The app will display a **real-time overview** of your finances, including:
- **Total Income**
- **Total Expenses**
- **Remaining Balance** (calculated as Income - Expenses)

This will help you understand how your finances are evolving over time.

## Technologies Used

- **Streamlit** - For creating the web application.
- **Pandas** - For data manipulation and CSV handling.
- **Python** - For the backend logic and processing.

## Local Setup Instructions

If you'd like to run the app locally, follow these steps:
