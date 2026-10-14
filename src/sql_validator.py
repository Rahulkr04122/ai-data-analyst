
import re
import sqlglot
from sqlglot import exp

ALLOWED_TABLES = {"customers", "products", "orders"}

FORBIDDEN_PATTERNS = [
    r"\bINTO\s+OUTFILE\b",
    r"\bINTO\s+DUMPFILE\b",
    r"\bLOAD_FILE\s*\(",
    r"\bSLEEP\s*\(",
    r"\bBENCHMARK\s*\(",
]


def validate_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise ValueError("SQL query cannot be empty.")

    if len(sql) > 10000:
        raise ValueError("SQL query is too long.")

    if ";" in sql:
        raise ValueError("Semicolons are not allowed.")

    if "--" in sql or "/*" in sql or "*/" in sql or "#" in sql:
        raise ValueError("SQL comments are not allowed.")

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, sql, flags=re.IGNORECASE):
            raise ValueError("The query contains a forbidden operation.")

    try:
        statements = sqlglot.parse(sql, read="mysql")
    except sqlglot.errors.ParseError as error:
        raise ValueError("Invalid SQL syntax.") from error

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Exactly one SQL statement is allowed.")

    tree = statements[0]

    if not isinstance(tree, exp.Select):
        raise ValueError("Only SELECT queries are allowed.")

    for table in tree.find_all(exp.Table):
        if table.name.lower() not in ALLOWED_TABLES:
            raise ValueError(f"Table '{table.name}' is not allowed.")

        if table.db and table.db.lower() != "ai_analyst_db":
            raise ValueError("Access to other schemas is not allowed.")

        if table.catalog:
            raise ValueError("Catalog-qualified tables are not allowed.")

    for function in tree.find_all(exp.Func):
        function_name = function.sql_name().upper()
        if function_name in {"SLEEP", "BENCHMARK", "LOAD_FILE"}:
            raise ValueError(f"Function '{function_name}' is not allowed.")

    if tree.args.get("limit") is None:
        tree = tree.limit(100)

    return tree.sql(dialect="mysql")
