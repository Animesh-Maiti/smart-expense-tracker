import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])


def add_expense():
    print("\n--- Add Expense ---")

    category = input("Category: ")
    amount = input("Amount: ")
    description = input("Description: ")

    date = datetime.now().strftime("%Y-%m-%d")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount!")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("Expense added successfully.")


def view_expenses():
    print("\n--- All Expenses ---")

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        rows = list(reader)

        if len(rows) <= 1:
            print("No expenses found.")
            return

        print(
            f"\n{'Date':<12} {'Category':<15} {'Amount':<10} Description"
        )
        print("-" * 60)

        for row in rows[1:]:
            print(
                f"{row[0]:<12} {row[1]:<15} ₹{row[2]:<9} {row[3]}"
            )


def total_expense():
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += float(row["Amount"])

    print(f"\nTotal Expense: ₹{total:.2f}")


def category_summary():
    summary = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["Category"]
            amount = float(row["Amount"])

            if category in summary:
                summary[category] += amount
            else:
                summary[category] = amount

    if not summary:
        print("No data available.")
        return

    print("\n--- Category Summary ---")

    for category, amount in summary.items():
        print(f"{category:<20} ₹{amount:.2f}")


def monthly_summary():
    monthly = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            month = row["Date"][:7]
            amount = float(row["Amount"])

            if month in monthly:
                monthly[month] += amount
            else:
                monthly[month] = amount

    if not monthly:
        print("No data available.")
        return

    print("\n--- Monthly Summary ---")

    for month, amount in monthly.items():
        print(f"{month:<10} ₹{amount:.2f}")


def highest_expense():
    highest = None

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if highest is None:
                highest = row
            elif float(row["Amount"]) > float(highest["Amount"]):
                highest = row

    if highest:
        print("\n--- Highest Expense ---")
        print(f"Date       : {highest['Date']}")
        print(f"Category   : {highest['Category']}")
        print(f"Amount     : ₹{highest['Amount']}")
        print(f"Description: {highest['Description']}")
    else:
        print("No expenses available.")


def search_category():
    category_name = input("\nEnter category to search: ")

    found = False

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        print("\nResults:")
        print("-" * 50)

        for row in reader:
            if row["Category"].lower() == category_name.lower():
                found = True
                print(
                    f"{row['Date']} | "
                    f"{row['Category']} | "
                    f"₹{row['Amount']} | "
                    f"{row['Description']}"
                )

    if not found:
        print("No records found.")


def delete_expense():
    view_expenses()

    date = input(
        "\nEnter date of expense to delete (YYYY-MM-DD): "
    )

    rows = []

    deleted = False

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        header = next(reader)
        rows.append(header)

        for row in reader:
            if row[0] == date and not deleted:
                deleted = True
                continue

            rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    if deleted:
        print("Expense deleted.")
    else:
        print("Expense not found.")


def export_report():
    report_name = "expense_report.txt"

    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)

        data = list(reader)

        for row in data:
            total += float(row["Amount"])

    with open(report_name, "w") as report:
        report.write("SMART EXPENSE TRACKER REPORT\n")
        report.write("=" * 35 + "\n\n")

        for row in data:
            report.write(
                f"{row['Date']} | "
                f"{row['Category']} | "
                f"₹{row['Amount']} | "
                f"{row['Description']}\n"
            )

        report.write("\n")
        report.write(f"TOTAL EXPENSE = ₹{total:.2f}\n")

    print(f"Report exported as {report_name}")


def menu():
    while True:
        print("\n")
        print("=" * 40)
        print("SMART EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Category Summary")
        print("5. Monthly Summary")
        print("6. Highest Expense")
        print("7. Search Category")
        print("8. Delete Expense")
        print("9. Export Report")
        print("0. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            total_expense()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            highest_expense()

        elif choice == "7":
            search_category()

        elif choice == "8":
            delete_expense()

        elif choice == "9":
            export_report()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


initialize_file()
menu()
