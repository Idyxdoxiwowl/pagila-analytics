import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="pagila",
    user="postgres",
    password="ayana",  
    host="localhost",
    port="5432"
)

# Список запросов
queries = {
    "top_actors": "SELECT * FROM actor LIMIT 10;",
    "active_customers": """
        SELECT c.first_name || ' ' || c.last_name AS customer, COUNT(r.rental_id) AS rental_count
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        GROUP BY customer
        ORDER BY rental_count DESC
        LIMIT 10;
    """,
    "revenue_by_category": """
        SELECT c.name AS category, SUM(p.amount) AS total_revenue
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY c.name
        ORDER BY total_revenue DESC;
    """
}

# Выполняем запросы и сохраняем
for name, query in queries.items():
    df = pd.read_sql(query, conn)
    print(f"\n=== {name.upper()} ===")
    print(df)

    # Сохраняем в CSV
    df.to_csv(f"{name}.csv", index=False)

conn.close()
