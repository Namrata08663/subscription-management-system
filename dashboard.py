from database import get_connection


def show_dashboard():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    # Total revenue
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
    """)

    revenue = cursor.fetchone()[0]

    # Number of payments
    cursor.execute("""
        SELECT COUNT(*)
        FROM payments
    """)

    payment_count = cursor.fetchone()[0]

    # Pending invoices
    cursor.execute("""
        SELECT COUNT(*)
        FROM invoices
        WHERE paid_amount < total_amount
        AND due_date >= CURDATE()
    """)

    pending = cursor.fetchone()[0]

    # Overdue invoices
    cursor.execute("""
        SELECT COUNT(*)
        FROM invoices
        WHERE paid_amount < total_amount
        AND due_date < CURDATE()
    """)

    overdue = cursor.fetchone()[0]

    # Fully paid invoices
    cursor.execute("""
        SELECT COUNT(*)
        FROM invoices
        WHERE paid_amount = total_amount
    """)

    paid = cursor.fetchone()[0]

    print("\n================================")
    print("       REVENUE DASHBOARD")
    print("================================")

    print("Total Revenue: ₹", revenue)
    print("Total Payments:", payment_count)
    print("Pending Invoices:", pending)
    print("Overdue Invoices:", overdue)
    print("Paid Invoices:", paid)

    print("================================")

    cursor.close()
    conn.close()
