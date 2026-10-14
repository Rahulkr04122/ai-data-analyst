
from src.database import get_connection
from src.sql_validator import validate_sql


def get_sales_summary():
    """Return revenue and completed order-line count."""
    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                COUNT(*) AS completed_order_items,
                COALESCE(
                    SUM(quantity * unit_price), 0
                ) AS total_revenue
            FROM orders
            WHERE status = %s
        """

        cursor.execute(query, ("Completed",))
        result = cursor.fetchone()

        return {
            "completed_order_items": result["completed_order_items"],
            "total_revenue": float(result["total_revenue"]),
        }

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def get_top_products(limit=5):
    """Return products ranked by completed sales revenue."""
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("limit must be an integer")

    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.category,
                SUM(o.quantity * o.unit_price) AS revenue
            FROM orders AS o
            JOIN products AS p
                ON o.product_id = p.product_id
            WHERE o.status = %s
            GROUP BY
                p.product_id,
                p.product_name,
                p.category
            ORDER BY revenue DESC
            LIMIT %s
        """

        cursor.execute(query, ("Completed", limit))
        rows = cursor.fetchall()

        return [
            {
                **row,
                "revenue": float(row["revenue"]),
            }
            for row in rows
        ]

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def run_read_query(sql: str):
    """Validate and execute a read-only analytics query."""
    safe_sql = validate_sql(sql)
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(safe_sql)
        rows = cursor.fetchall()

        return {
            "sql": safe_sql,
            "row_count": len(rows),
            "rows": rows,
        }

    finally:
        if connection is not None and connection.is_connected():
            connection.close()



if __name__ == "__main__":
    print("Sales summary:")
    print(get_sales_summary())

    print("\nTop products:")
    for product in get_top_products():
        print(product)
