import psycopg2
import pandas as pd
import plotly.express as px

# Подключение к БД
conn = psycopg2.connect(
    dbname="pagila",
    user="postgres",
    password="ayana",   # замени на свой пароль
    host="localhost",
    port="5432"
)

# SQL: доход по категориям фильмов по месяцам
query = """
    SELECT DATE_TRUNC('month', p.payment_date) AS month,
           c.name AS category,
           SUM(p.amount) AS revenue
    FROM payment p
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    GROUP BY month, c.name
    ORDER BY month, revenue DESC;
"""

df = pd.read_sql(query, conn)
conn.close()

# Преобразуем месяц в строку (чтобы ползунок нормально работал)
df["month"] = df["month"].dt.strftime("%Y-%m")

# Строим интерактивный график
fig = px.bar(
    df,
    x="category",
    y="revenue",
    color="category",
    animation_frame="month",   # 👈 вот тут появляется ползунок времени
    range_y=[0, df["revenue"].max() + 100]
)

fig.update_layout(
    title="Revenue by Category over Time",
    xaxis_title="Category",
    yaxis_title="Revenue ($)"
)

fig.show()
