import os

MAX_EXPENSES = 100
EXPENSES_FILE = "expenses.txt"

ADD_EXPENSE_OPTION = 1
VIEW_EXPENSES_OPTION = 2
TOTAL_EXPENSES_OPTION = 3
EDIT_EXPENSE_OPTION = 4
EXIT_OPTION = 5


class ExpenseStore:
    """Stores expense records in memory and manages file-based persistence."""

    def __init__(self, max_expenses=MAX_EXPENSES, filename=EXPENSES_FILE):
        self.max_expenses = max_expenses
        self.filename = filename
        self.descriptions = []
        self.amounts = []

    def is_full(self):
        return len(self.descriptions) >= self.max_expenses

    def is_empty(self):
        return len(self.descriptions) == 0

    def count(self):
        return len(self.descriptions)

    def add(self, description, amount):
        if self.is_full():
            return False

        self.descriptions.append(description)
        self.amounts.append(amount)
        return True

    def get_entry(self, index):
        return self.descriptions[index], self.amounts[index]

    def update(self, index, description, amount):
        self.descriptions[index] = description
        self.amounts[index] = amount

    def total(self):
        return sum(self.amounts)

    def save_to_file(self):
        try:
            with open(self.filename, "w") as file:
                for index in range(self.count()):
                    file.write(f"{self.descriptions[index]},{self.amounts[index]}\n")
            print("Expenses saved to the record file successfully.")
        except IOError as ex:
            print("Error saving expenses to the record file:", ex)

    def load_from_file(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r") as file:
                for line in file:
                    expense_record = line.strip().split(",")

                    if len(expense_record) == 2 and not self.is_full():
                        self.descriptions.append(expense_record[0])
                        self.amounts.append(float(expense_record[1]))

            print("Expenses loaded from the record file successfully.")
        except ValueError as ex:
            print("Error reading expense amount from the record file:", ex)
        except IOError as ex:
            print("Error loading expenses from the record file:", ex)


class ExpenseTracker:
    """Handles the menu-driven interaction for the expense tracker."""

    def __init__(self, store=None):
        self.store = store if store is not None else ExpenseStore()

    def add_expense(self):
        if self.store.is_full():
            print("Expense limit reached! Cannot add more expenses.")
            return

        description = input("Enter expense description: ")

        try:
            amount = float(input("Enter expense amount: "))
        except ValueError:
            print("Invalid amount. Expense not added.")
            return

        if self.store.add(description, amount):
            print("Expense added successfully!")

    def view_expenses(self):
        if self.store.is_empty():
            print("No expenses to display.")
            return

        print("\nExpenses:")
        for index in range(self.store.count()):
            description, amount = self.store.get_entry(index)
            print(f"{index + 1}. {description} - {amount}")

    def calculate_total(self):
        return self.store.total()

    def edit_expense(self, index):
        description, current_amount = self.store.get_entry(index)
        print(f"Editing Expense: {description} - {current_amount}")

        new_description = input("Enter new description: ")

        try:
            new_amount = float(input("Enter new amount: "))
        except ValueError:
            print("Invalid amount. Edit not saved.")
            return

        self.store.update(index, new_description, new_amount)
        print("Expense updated successfully!")

    def edit_selected_expense(self):
        try:
            index = int(
                input(f"Enter the expense index to edit (1 to {self.store.count()}): ")
            )
            if index < 1 or index > self.store.count():
                print("Invalid index. Please try again.")
                return

            self.edit_expense(index - 1)
        except ValueError:
            print("Invalid input. Please enter a valid index.")

    def process_choice(self, choice):
        if choice == ADD_EXPENSE_OPTION:
            self.add_expense()
        elif choice == VIEW_EXPENSES_OPTION:
            self.view_expenses()
        elif choice == TOTAL_EXPENSES_OPTION:
            print("Total Expenses:", self.calculate_total())
        elif choice == EDIT_EXPENSE_OPTION:
            self.edit_selected_expense()
        elif choice == EXIT_OPTION:
            print("Exiting... Goodbye!")
        else:
            print("Invalid choice. Please try again.")

    def save_expenses_to_file(self):
        self.store.save_to_file()

    def load_expenses_from_file(self):
        self.store.load_from_file()


def display_menu():
    print("\nExpense Tracker Menu")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total Expenses")
    print("4. Edit Expense")
    print("5. Exit")


def get_user_choice():
    try:
        return int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        return -1


def process_choice(choice, tracker):
    tracker.process_choice(choice)


def main():
    tracker = ExpenseTracker()
    tracker.load_expenses_from_file()

    choice = 0
    while choice != EXIT_OPTION:
        display_menu()
        choice = get_user_choice()
        process_choice(choice, tracker)

    tracker.save_expenses_to_file()


if __name__ == "__main__":
    main()
