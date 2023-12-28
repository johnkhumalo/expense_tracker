# expense_tracker
expense_tracker
#select option 1-10 to use the app.
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Create necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL,
                    date TEXT
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS incomes (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL,
                    date TEXT
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY,
                    category_id INTEGER,
                    amount REAL,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                    )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
                    id INTEGER PRIMARY KEY,
                    goal_name TEXT,
                    goal_amount REAL
                    )''')

# Functions to handle operations like add expense, view expenses, add income, set budget
def add_expense(category, amount, date):
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, amount, date))
    conn.commit()

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(row)
            
def view_budgets():
    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()
    for row in rows:
        print("Category: {}, Budget: {}".format(row[0], row[1]))



# Calculate remaining funds
def calculate_remaining_funds():
    cursor.execute("SELECT SUM(amount) FROM incomes")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0] or 0

    remaining_funds = total_income - total_expense
    return remaining_funds

# Function to set budget for a category
def set_budget(category_name, budget_amount):
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()

    cursor.execute("SELECT id FROM categories WHERE name=?", (category_name,))
    category_id = cursor.fetchone()
    if category_id:
        cursor.execute("INSERT INTO budgets (category_id, amount) VALUES (?, ?)", (category_id[0], budget_amount))
        conn.commit()
        print("Budget set successfully for {}.".format(category_name))
    else:
        print("Category not found.")

def view_budgets():
    cursor.execute("SELECT categories.name, budgets.amount FROM categories INNER JOIN budgets ON categories.id = budgets.category_id")
    rows = cursor.fetchall()
    if not rows:
        print("No budgets found.")
    else:
        for row in rows:
            print(f"Category: {row[0]}, Budget: {row[1]}")


def set_financial_goal():
    goal_name = input("Enter the name of the financial goal: ")
    goal_amount = float(input("Enter the target amount for this goal: "))
    cursor.execute("INSERT INTO financial_goals (goal_name, goal_amount) VALUES (?, ?)", (goal_name, goal_amount))
    conn.commit()
    print("Financial goal '{}' set successfully.".format(goal_name))


# Function to view progress towards financial goals
def view_progress_towards_goals():
    cursor.execute("SELECT SUM(goal_amount) FROM financial_goals")
    total_goals_amount = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0] or 0

    progress = (total_expense / total_goals_amount) * 100 if total_goals_amount > 0 else 0
    print("Progress towards financial goals: {:.2f}%".format(progress))

def add_income():
    income_category = input("Enter income category: ")
    income_amount = float(input("Enter income amount: "))
    income_date = input("Enter income date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO incomes (category, amount, date) VALUES (?, ?, ?)",
                   (income_category, income_amount, income_date))
    conn.commit()
    print("Income added successfully.")    
def view_incomes():
    cursor.execute("SELECT * FROM incomes")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Income ID: {row[0]}, Category: {row[1]}, Amount: R{row[2]}, Date: {row[3]}")
        
    


def main():
    while True:
        print("\nExpense and Budget Tracking App")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Add Income")
        print("4. View Incomes")
        print("5. Set Budget for a Category")
        print("6. View Budget for a Category")
        print("7. Set Financial Goals")
        print("8. View Progress Towards Financial Goals")
        print("9. Calculate Remaining Funds")
        print("10. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("Enter expense category: ")
            amount = float(input("Enter expense amount: "))
            date = input("Enter expense date (YYYY-MM-DD): ")
            add_expense(category, amount, date)

        elif choice == "2":
            # View Expenses
            view_expenses()
        elif choice == "3":
            # Add Income
            add_income()
        elif choice == "4":
            # View Incomes
            view_incomes()
        elif choice == "5":
            # Set Budget for a Category
            category_name = input("Enter category name to set budget: ")
            budget_amount = float(input("Enter budget amount: "))
            set_budget(category_name, budget_amount)
        elif choice == "6":
            # View Budget for a Category
            view_budgets()
        elif choice == "7":
            # Set Financial Goals
            set_financial_goal()
        elif choice == "8":
            # View Progress Towards Financial Goals
            view_progress_towards_goals()
        elif choice == "9":
            # Calculate Remaining Funds
            remaining_funds = calculate_remaining_funds()
            print(f"Remaining funds: R{remaining_funds}")
        elif choice == "10":
            # Quit
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

# Close database connection
conn.close()
