# Smart Expense Tracker

A robust, terminal-based personal finance utility built entirely in Python. 

This application offers an lightweight approach to tracking expenses, managing monthly financial targets, and generating clean structural reports without the overhead of external database engines.

## Key Features

- **Granular Record Tracking:** Add, view, and search your transactions seamlessly.
- **Budgeting & Alert Engine:** Define a monthly spending limit. Get live alerts at the main menu and real-time warnings if you cross 80% or 100% of your threshold when logging an expense.
- **Aggregated Analytics:** Instantly view total expenditure alongside broken-down summaries sorted by structural categories or chronological months.
- **Fail-Safe Record Deletion:** Delete transactions accurately using unique, auto-incrementing transactional IDs rather than ambiguous matching parameters.
- **Robust IO Management:** Built with explicit UTF-8 character encoding handling and zero-data corruption safe-guards to manage uninitialized states gracefully.
- **Export Engine:** Generate clean, print-ready text formatting summaries containing your complete transaction histories.

## Technologies Used

- **Python 3.x**
- **CSV Module:** Structured relational flat-file data persistence.
- **Datetime Engine:** Localized calendar-month indexing and logging.

## Application Preview

```text
========================================
        SMART EXPENSE TRACKER
========================================
Status This Month: ₹4,200.00 / Budget: ₹10,000.00
----------------------------------------
1. Add Expense
2. View Expenses
3. Total Expense
4. Category Summary
5. Monthly Summary
6. Highest Expense
7. Search Category
8. Delete Expense
9. Export Report
B. Set Monthly Budget
0. Exit
## Why I Built This

I wanted to build a small project that uses file handling and basic data analysis concepts while keeping the application simple and easy to use. This project helped me practice working with CSV files, organizing code into functions, and creating a menu-driven application.

## Future Improvements

- GUI using Tkinter
- Charts using Matplotlib
- SQLite Database
- User Authentication
- Web Version using Flask
