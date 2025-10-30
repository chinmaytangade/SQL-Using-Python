# Import required libraries
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------
# Step 1: Create a database and sales table
# ------------------------------------------

# Connect to (or create) a database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Drop old table if it exists
cursor.execute("DROP TABLE IF EXISTS sales")

# Create a sales table
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    quantity_sold INTEGER,
    price_per_unit REAL,
    sale_date TEXT
)
""")

# ------------------------------------------
# Step 2: Insert sample data
# ------------------------------------------

sample_data = [
    ('Laptop', 5, 60000, '2025-10-01'),
    ('Mouse', 20, 500, '2025-10-02'),
    ('Keyboard', 15, 1200, '2025-10-02'),
    ('Monitor', 8, 10000, '2025-10-03'),
    ('Headphones', 12, 2500, '2025-10-04'),
    ('Laptop', 3, 60000, '2025-10-05'),
    ('Mouse', 10, 500, '2025-10-06'),
    ('Keyboard', 7, 1200, '2025-10-07')
]

cursor.executemany("""
INSERT INTO sales (product_name, quantity_sold, price_per_unit, sale_date)
VALUES (?, ?, ?, ?)
""", sample_data)

conn.commit()

# ------------------------------------------
# Step 3: Query sales information
# ------------------------------------------

query = """
SELECT 
    product_name,
    SUM(quantity_sold) AS total_quantity,
    SUM(quantity_sold * price_per_unit) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
"""

df = pd.read_sql_query(query, conn)

# Display data in console
print("📊 Sales Summary:\n")
print(df)

# ------------------------------------------
# Step 4: Visualization (Bar Chart)
# ------------------------------------------

plt.figure(figsize=(8, 5))
plt.bar(df['product_name'], df['total_revenue'])
plt.title("Total Revenue by Product")
plt.xlabel("Product Name")
plt.ylabel("Total Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close connection
conn.close()
