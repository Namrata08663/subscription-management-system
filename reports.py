
from database import get_connection


def monthly_report():

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            YEAR(payment_date) AS year,
            MONTH(payment_date) AS month,
            SUM(amount) AS revenue,
            COUNT(*) AS total_payments
        FROM payments
        GROUP BY YEAR(payment_date),
                 MONTH(payment_date)
        ORDER BY year DESC, month DESC
    """)

    records = cursor.fetchall()

    print("\n========== MONTHLY REVENUE REPORT ==========")

    if not records:
        print("No revenue records found.")

    for row in records:

        print("\nYear:", row[0])
        print("Month:", row[1])
        print("Revenue: ₹", row[2])
        print("Total Payments:", row[3])

    cursor.close()
    conn.close()
