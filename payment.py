from database import get_connection
from decimal import Decimal


def add_payment():

    try:
        invoice_id = int(input("Enter Invoice ID: "))
        amount = Decimal(input("Enter Payment Amount: "))

        if not amount.is_finite() or amount <= 0:
            print("Invalid payment amount.")
            return

        method = input("Enter Payment Method: ").strip()
        reference = input("Enter Transaction Reference (optional): ").strip()

        if not method:
            print("Payment method cannot be empty.")
            return

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor(dictionary=True)

        conn.start_transaction()

        cursor.execute("""
            SELECT total_amount, paid_amount, due_date
            FROM invoices
            WHERE invoice_id = %s
            FOR UPDATE
        """, (invoice_id,))

        invoice = cursor.fetchone()

        if invoice is None:
            raise ValueError("Invoice not found.")

        total = Decimal(str(invoice["total_amount"]))
        paid = Decimal(str(invoice["paid_amount"] or 0))

        balance = total - paid

        if balance <= 0:
            raise ValueError("Invoice is already fully paid.")

        if amount > balance:
            raise ValueError("Payment exceeds outstanding balance.")

        cursor.execute("""
            INSERT INTO payments
            (invoice_id, amount, payment_method,
             transaction_reference)
            VALUES (%s, %s, %s, %s)
        """, (
            invoice_id,
            amount,
            method,
            reference or None
        ))

        new_paid = paid + amount

        if new_paid == total:
            status = "Paid"
        elif invoice["due_date"] < __import__("datetime").date.today():
            status = "Overdue"
        else:
            status = "Partially Paid"

        cursor.execute("""
            UPDATE invoices
            SET paid_amount = %s, status = %s
            WHERE invoice_id = %s
        """, (new_paid, status, invoice_id))

        conn.commit()

        print("\nPayment recorded successfully!")
        print("Payment Amount:", amount)
        print("New Invoice Status:", status)

    except ValueError as error:
        if 'conn' in locals() and conn is not None and conn.is_connected():
            conn.rollback()
        print("Error:", error)

    except Exception as error:
        if 'conn' in locals() and conn is not None and conn.is_connected():
            conn.rollback()
        print("Payment could not be recorded:", error)

    finally:
        if 'conn' in locals() and conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


def view_payments():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_id, invoice_id, amount,
               payment_date, payment_method,
               transaction_reference
        FROM payments
        ORDER BY payment_date DESC
    """)

    records = cursor.fetchall()

    print("\n========== PAYMENT HISTORY ==========")

    if not records:
        print("No payments found.")

    for record in records:
        print("\nPayment ID:", record[0])
        print("Invoice ID:", record[1])
        print("Amount: ₹", record[2])
        print("Date:", record[3])
        print("Method:", record[4])
        print("Reference:", record[5] or "-")

    cursor.close()
    conn.close()


def search_payment():

    try:
        payment_id = int(input("Enter Payment ID: "))

        conn = get_connection()

        if conn is None:
            return

        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM payments
            WHERE payment_id = %s
        """, (payment_id,))

        record = cursor.fetchone()

        if record:
            print("\nPayment Found")
            print("Payment ID:", record[0])
            print("Invoice ID:", record[1])
            print("Amount:", record[2])
            print("Payment Date:", record[3])
            print("Payment Method:", record[4])
            print("Reference:", record[5] or "-")
        else:
            print("Payment not found.")

        cursor.close()
        conn.close()

    except ValueError:
        print("Please enter a valid payment ID.")
