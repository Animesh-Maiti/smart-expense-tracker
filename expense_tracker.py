import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
BUDGET_FILE = "budget.txt"
FIELDS = ["ID", "Date", "Category", "Amount", "Description"]

APP_STATE = {
    "expenses": [],
    "budget": 0.0,
    "month_spent": 0.0
}

def update_app_state():
    """Helper to refresh the in-memory cache when files change."""
    APP_STATE["expenses"] = _load_expenses()
    APP_STATE["budget"] = _get_budget()
    
    current_month = datetime.now().strftime("%Y-%m")
    APP_STATE["month_spent"] = sum(
        float(row["Amount"])
        for row in APP_STATE["expenses"]
        if row["Date"].startswith(current_month)
    )


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)


def _load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (IOError, csv.Error):
        print("Error reading the data file.")
        return []


def _save_expenses(rows):
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    except IOError:
        print("Error writing to the data file.")


def _get_budget():
    if not os.path.exists(BUDGET_FILE):
        return 0.0
    try:
        with open(BUDGET_FILE, "r") as file:
            return float(file.read().strip())
    except (ValueError, IOError):
        return 0.0


def set_budget():
    print("\n--- Set Monthly Budget ---")
    try:
        budget = float(input("Enter monthly budget limit (₹): "))
        if budget <= 0:
            print("Budget must be greater than zero!")
            return
        with open(BUDGET_FILE, "w") as file:
            file.write(f"{budget:.2f}")
        print(f"Monthly budget set to ₹{budget:.2f}")
    except ValueError:
        print("Invalid input! Please enter a numeric value.")


def _check_budget_alerts(data, new_amount=0.0):
    """Modified to accept pre-loaded data instead of reading the file again."""
    budget = _get_budget()
    if budget == 0.0:
        return

    current_month = datetime.now().strftime("%Y-%m")

    spent = sum(
        float(row["Amount"])
        for row in data
        if row["Date"].startswith(current_month)
    )
    total_projected = spent + new_amount

    if total_projected > budget:
        print(
            f"\nALERT: You have EXCEEDED your budget! (Spent: ₹{total_projected:.2f} / Budget: ₹{budget:.2f})"
        )
    elif total_projected >= (budget * 0.8):
        print(
            f"\nWARNING: You have used {((total_projected/budget)*100):.1f}% of your budget! (Spent: ₹{total_projected:.2f} / Budget: ₹{budget:.2f})"
        )


def add_expense():
    print("\n--- Add Expense ---")

    category = input("Category: ").strip()
    if not category:
        print("Category cannot be empty!")
        return

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return

    description = input("Description: ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    # Optimization: Load the data ONCE right here
    existing_data = _load_expenses()

    # Pass the already loaded data into the alert check
    _check_budget_alerts(existing_data, amount)

    # Reuse the same loaded data to find the next ID
    next_id = int(existing_data[-1]["ID"]) + 1 if existing_data else 1

    new_expense = {
        "ID": str(next_id),
        "Date": date,
        "Category": category,
        "Amount": f"{amount:.2f}",
        "Description": description,
    }

    try:
        with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writerow(new_expense)
        print("Expense added successfully.")
    except IOError:
        print("Could not save expense.")

def view_expenses():
    print("\n--- All Expenses ---")
    data = _load_expenses()

    if not data:
        print("No expenses found.")
        return

    print(
        f"\n{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} Description"
    )
    print("-" * 65)
    for row in data:
        print(
            f"{row['ID']:<5} {row['Date']:<12} {row['Category']:<15} ₹{float(row['Amount']):<9.2f} {row['Description']}"
        )


def total_expense():
    data = _load_expenses()
    total = sum(float(row["Amount"]) for row in data)
    print(f"\nTotal Expense: ₹{total:.2f}")


def category_summary():
    data = _load_expenses()
    if not data:
        print("No data available.")
        return

    summary = {}
    for row in data:
        cat = row["Category"]
        summary[cat] = summary.get(cat, 0.0) + float(row["Amount"])

    print("\n--- Category Summary ---")
    for category, amount in summary.items():
        print(f"{category:<20} ₹{amount:.2f}")


def monthly_summary():
    data = _load_expenses()
    if not data:
        print("No data available.")
        return

    monthly = {}
    for row in data:
        month = row["Date"][:7]
        monthly[month] = monthly.get(month, 0.0) + float(row["Amount"])

    print("\n--- Monthly Summary ---")
    for month, amount in sorted(monthly.items()):
        print(f"{month:<10} ₹{amount:.2f}")


def highest_expense():
    data = _load_expenses()
    if not data:
        print("No expenses available.")
        return

    highest = max(data, key=lambda x: float(x["Amount"]))

    print("\n--- Highest Expense ---")
    print(f"ID         : {highest['ID']}")
    print(f"Date       : {highest['Date']}")
    print(f"Category   : {highest['Category']}")
    print(f"Amount     : ₹{float(highest['Amount']):.2f}")
    print(f"Description: {highest['Description']}")


def search_category():
    category_name = input("\nEnter category to search: ").strip().lower()
    data = _load_expenses()

    results = [
        r for r in data if r["Category"].lower() == category_name
    ]

    if not results:
        print("No records found.")
        return

    print("\nResults:")
    print("-" * 60)
    for row in results:
        print(
            f"{row['Date']} | {row['Category']} | ₹{float(row['Amount']):.2f} | {row['Description']}"
        )


def delete_expense():
    view_expenses()
    data = _load_expenses()
    if not data:
        return

    target_id = input("\nEnter ID of expense to delete: ").strip()
    updated_data = [row for row in data if row["ID"] != target_id]

    if len(updated_data) == len(data):
        print("Expense ID not found.")
    else:
        _save_expenses(updated_data)
        print("Expense deleted successfully.")


def export_report():
    report_name = "expense_report.txt"
    data = _load_expenses()

    if not data:
        print("No data to export.")
        return

    total = sum(float(row["Amount"]) for row in data)

    try:
        with open(report_name, "w", encoding="utf-8") as report:
            report.write("SMART EXPENSE TRACKER REPORT\n")
            report.write("=" * 45 + "\n\n")
            report.write(
                f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | Description\n"
            )
            report.write("-" * 55 + "\n")

            for row in data:
                report.write(
                    f"{row['Date']:<12} | {row['Category']:<15} | ₹{float(row['Amount']):<9.2f} | {row['Description']}\n"
                )

            report.write("\n" + "=" * 45 + "\n")
            report.write(f"TOTAL EXPENSE = ₹{total:.2f}\n")

        print(f"Report exported successfully as {report_name}")
    except IOError:
        print("Failed to write report file.")


def menu():
    while True:
        budget = _get_budget()
        current_month = datetime.now().strftime("%Y-%m")
        data = _load_expenses()
        month_spent = sum(
            float(row["Amount"])
            for row in data
            if row["Date"].startswith(current_month)
        )

        print("\n" + "=" * 40)
        print("        SMART EXPENSE TRACKER")
        print("=" * 40)
        if budget > 0:
            print(
                f"Status This Month: ₹{month_spent:.2f} / Budget: ₹{budget:.2f}"
            )
            print("-" * 40)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Category Summary")
        print("5. Monthly Summary")
        print("6. Highest Expense")
        print("7. Search Category")
        print("8. Delete Expense")
        print("9. Export Report")
        print("B. Set Monthly Budget")
        print("0. Exit")

        choice = input("\nEnter choice: ").strip().upper()

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
        elif choice == "B":
            set_budget()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    initialize_file()
    update_app_state() 
    menu()