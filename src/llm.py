
import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

client = Client(host=OLLAMA_HOST)

DATABASE_SCHEMA = """
Table: customers
Columns: customer_id, customer_name, city

Table: products
Columns: product_id, product_name, category, price

Table: orders
Columns: order_item_id, order_id, customer_id, product_id,
quantity, unit_price, order_date, status

Relationships:
orders.customer_id = customers.customer_id
orders.product_id = products.product_id

Business rule:
Revenue = SUM(quantity * unit_price)
Only orders with status = 'Completed' count as revenue.
"""


def generate_sql(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a MySQL analytics assistant. "
                    "Generate exactly one read-only SELECT query "
                    "using only the provided schema. "
                    "Use explicit JOIN conditions. "
                    "Only completed orders count as revenue. "
                    "Never generate INSERT, UPDATE, DELETE, DROP, "
                    "ALTER, CREATE, or other modification statements. "
                    "Return only SQL without Markdown fences."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Schema:\n{DATABASE_SCHEMA}\n\n"
                    f"Business question: {question}"
                ),
            },
        ],
        options={"temperature": 0},
    )

    return response.message.content.strip()
