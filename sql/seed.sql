
USE ai_analyst_db;

INSERT INTO customers
(customer_id, customer_name, city)
VALUES
(1, 'Aarav Sharma', 'Delhi'),
(2, 'Priya Verma', 'Mumbai'),
(3, 'Kabir Singh', 'Bengaluru'),
(4, 'Ananya Gupta', 'Delhi'),
(5, 'Rohan Patel', 'Pune');

INSERT INTO products
(product_id, product_name, category, price)
VALUES
(101, 'Laptop', 'Electronics', 55000.00),
(102, 'Headphones', 'Electronics', 2500.00),
(103, 'Office Chair', 'Furniture', 8000.00),
(104, 'Notebook Pack', 'Stationery', 300.00),
(105, 'Keyboard', 'Electronics', 1500.00);

INSERT INTO orders
(order_item_id, order_id, customer_id, product_id,
 quantity, unit_price, order_date, status)
VALUES
(1, 1001, 1, 101, 1, 55000.00, '2026-09-02', 'Completed'),
(2, 1002, 2, 102, 2, 2500.00, '2026-09-05', 'Completed'),
(3, 1003, 3, 103, 1, 8000.00, '2026-09-10', 'Completed'),
(4, 1004, 1, 105, 2, 1500.00, '2026-09-15', 'Cancelled'),
(5, 1005, 4, 104, 5, 300.00, '2026-10-01', 'Completed'),
(6, 1006, 5, 101, 1, 55000.00, '2026-10-03', 'Completed'),
(7, 1007, 2, 105, 1, 1500.00, '2026-10-05', 'Completed'),
(8, 1008, 3, 102, 1, 2500.00, '2026-10-08', 'Pending'),
(9, 1009, 4, 103, 2, 8000.00, '2026-10-10', 'Completed'),
(10, 1010, 5, 104, 3, 300.00, '2026-10-12', 'Completed');
