

from payment import add_payment, view_payments, search_payment
from invoice import view_invoice_status
from dashboard import show_dashboard
from reports import monthly_report


def main():

    while True:

        print("\n")
        print("======================================")
        print("  SUBSCRIPTION MANAGEMENT SYSTEM")
        print("       MEMBER 4 - PAYMENTS")
        print("======================================")

        print("1. Add Payment")
        print("2. View Payment History")
        print("3. Search Payment")
        print("4. Invoice Payment Tracking")
        print("5. Revenue Dashboard")
        print("6. Monthly Revenue Report")
        print("7. Exit")

        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_payment()

        elif choice == "2":
            view_payments()

        elif choice == "3":
            search_payment()

        elif choice == "4":
            view_invoice_status()

        elif choice == "5":
            show_dashboard()

        elif choice == "6":
            monthly_report()

        elif choice == "7":
            print("Thank you for using the application!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
