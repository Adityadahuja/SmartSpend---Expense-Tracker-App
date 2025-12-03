# SmartSpend

SmartSpend is a Python Flask-based expense tracker that demonstrates OOP principles and specific Data Structures and Algorithms (DSA) concepts.

## Features

- **User Authentication**: Secure login and registration.
- **Expense Management**: Add, edit, delete, and list expenses.
- **Dashboard**: Visual summary of spending.
- **Analysis**: DSA-powered insights (sorting, searching, aggregations).
- **Modern UI**: Responsive design with Dark Mode support.

## Tech Stack

- Python 3.x
- Flask
- SQLite (SQLAlchemy)
- HTML/CSS (Tailwind CSS via CDN)
- JavaScript (Chart.js)

## OOP & DSA Concepts

### OOP
- **Models**: `User`, `Expense`, `Category` classes inheriting from `db.Model`.
- **Services**: `AuthService` and `ExpenseService` classes encapsulating business logic.

### DSA
- **Merge Sort**: Used for sorting expenses by date or amount.
- **Binary Search**: Used for efficient date-based searching.
- **Hash Map**: Used for category-wise aggregation.
- **Prefix Sum**: Used for cumulative spending analysis.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python run.py
   ```

3. Open `http://127.0.0.1:5000` in your browser.
