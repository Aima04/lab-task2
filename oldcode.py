import java.io.*;
import java.util.Scanner;

public class ExpenseTracker {
    // Maximum number of expenses to track
    static final int CAPACITY = 100;
    static String[] descriptions = new String[CAPACITY];
    static double[] amounts = new double[CAPACITY];
    static int count = 0;

    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int choice;

            // Load data from the record file
            loadExpensesFromFile();

            do {
                displayMenu();
                choice = getUserChoice(sc);
                processChoice(choice, sc);
            } while (choice != 5);

            // Save data to the record file before exiting
            saveExpensesToFile();
        }
    }

    static void displayMenu() {
        System.out.println("\nExpense Tracker Menu");
        System.out.println("1. Add Expense");
        System.out.println("2. View Expenses");
        System.out.println("3. Calculate Total Expenses");
        System.out.println("4. Edit Expense");
        System.out.println("5. Exit");
        System.out.print("Enter your choice: ");
    }

    static int getUserChoice(Scanner sc) {
        int choice;
        try {
            choice = Integer.parseInt(sc.nextLine());
        } catch (NumberFormatException ex) {
            System.out.println("Invalid input. Please enter a number between 1 and 5.");
            return -1; // Return an invalid choice
        }
        return choice;
    }

    static void processChoice(int choice, Scanner sc) {
        switch (choice) {
            case 1:
                addExpense(sc);
                break;
            case 2:
                viewExpenses();
                break;
            case 3:
                double total = calculateTotal(0);
                System.out.println("Total Expenses: " + total);
                break;
            case 4:
                System.out.print("Enter the expense index to edit (1 to " + count + "): ");
                try {
                    int index = Integer.parseInt(sc.nextLine());
                    if (index < 1 || index > count) {
                        System.out.println("Invalid index. Please try again.");
                    } else {
                        editExpense(index - 1, sc); // Pass zero-based index
                    }
                } catch (NumberFormatException ex) {
                    System.out.println("Invalid input. Please enter a valid index.");
                }
                break;
            case 5:
                System.out.println("Exiting... Goodbye!");
                break;
            default:
                System.out.println("Invalid choice. Please try again.");
        }
    }

    static void addExpense(Scanner sc) {
        if (count >= CAPACITY) {
            System.out.println("Expense limit reached! Cannot add more expenses.");
            return;
        }

        System.out.print("Enter expense description: ");
        String description = sc.nextLine();
        System.out.print("Enter expense amount: ");

        double amount;
        try {
            amount = Double.parseDouble(sc.nextLine());
        } catch (NumberFormatException ex) {
            System.out.println("Invalid amount. Expense not added.");
            return;
        }

        descriptions[count] = description;
        amounts[count] = amount;
        count++;
        System.out.println("Expense added successfully!");
    }

    static void viewExpenses() {
        if (count == 0) {
            System.out.println("No expenses to display.");
            return;
        }

        System.out.println("\nExpenses:");
        for (int i = 0; i < count; i++) {
            System.out.println((i + 1) + ". " + descriptions[i] + " - " + amounts[i]);
        }
    }

    static double calculateTotal(int index) {
        if (index == count) {
            return 0;
        }
        return amounts[index] + calculateTotal(index + 1);
    }

    static void saveExpensesToFile() {
        try (FileWriter fw = new FileWriter("expenses.txt")) {
            for (int i = 0; i < count; i++) {
                fw.write(descriptions[i] + "," + amounts[i] + "\n");
            }
            System.out.println("Expenses saved to the record file successfully.");
        } catch (IOException ex) {
            System.out.println("Error saving expenses to the record file: " + ex.getMessage());
        }
    }

    static void editExpense(int index, Scanner sc) {
        System.out.println("Editing Expense: " + descriptions[index] + " - " + amounts[index]);
        System.out.print("Enter new description: ");
        String newDescription = sc.nextLine();
        System.out.print("Enter new amount: ");

        double newAmount;
        try {
            newAmount = Double.parseDouble(sc.nextLine());
        } catch (NumberFormatException ex) {
            System.out.println("Invalid amount. Edit not saved.");
            return;
        }

        descriptions[index] = newDescription;
        amounts[index] = newAmount;
        System.out.println("Expense updated successfully!");
    }

    static void loadExpensesFromFile() {
        try {
            File recordFile = new File("expenses.txt");
            if (!recordFile.exists()) {
                return; // No record file to load
            }

            try (Scanner fileScanner = new Scanner(recordFile)) {
                while (fileScanner.hasNextLine()) {
                    String line = fileScanner.nextLine();
                    String[] data = line.split(",");
                    if (data.length == 2) {
                        descriptions[count] = data[0];
                        amounts[count] = Double.parseDouble(data[1]);
                        count++;
                    }
                }
            }
            System.out.println("Expenses loaded from the record file successfully.");
        } catch (FileNotFoundException ex) {
            System.out.println("Error loading expenses from the record file: " + ex.getMessage());
        } catch (NumberFormatException ex) {
            System.out.println("Error reading expense amount from the record file: " + ex.getMessage());
        }
    }
}