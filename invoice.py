
from database import get_connection


def view_invoice_status():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        SELECT invoice_id, customer_id,
               total_amount, paid_amount,
               total_amount - paid_amount AS balance,
               status, due_date
        FROM invoices
        ORDER BY invoice_id
    """)

    records = cursor.fetchall()

    print("\n========== INVOICE TRACKING ==========")

    if not records:
        print("No invoices found.")

    for row in records:

        print("\nInvoice ID:", row[0])
        print("Customer ID:", row[1])
        print("Total Amount: ₹", row[2])
        print("Paid Amount: ₹", row[3])
        print("Remaining Balance: ₹", row[4])
        print("Status:", row[5])
        print("Due Date:", row[6])

    cursor.close()
    conn.close()

