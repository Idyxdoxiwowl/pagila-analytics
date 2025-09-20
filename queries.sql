---1. Top 10 actors by number of films
SELECT a.first_name || ' ' || a.last_name AS actor, COUNT(fa.film_id) AS film_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY actor
ORDER BY film_count DESC
LIMIT 10;

-- 2. Actors whose name starts with "A", sorted by last name
SELECT first_name, last_name, last_update
FROM actor
WHERE first_name LIKE 'A%'
ORDER BY last_name ASC;

-- 3. Average, minimal, maximum rental rate by category
SELECT 
    c.name AS category,
    AVG(f.rental_rate) AS avg_rate,
    MIN(f.rental_rate) AS min_rate,
    MAX(f.rental_rate) AS max_rate
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY avg_rate DESC;

-- 4. Count of films per category
SELECT c.name AS category, COUNT(fc.film_id) AS film_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY film_count DESC;

-- 5. Top 10 most active customers (by rentals)
SELECT c.first_name || ' ' || c.last_name AS customer, COUNT(r.rental_id) AS rental_count
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY customer
ORDER BY rental_count DESC
LIMIT 10;

-- 6. Total revenue per customer
SELECT c.first_name || ' ' || c.last_name AS customer, SUM(p.amount) AS total_payment
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY customer
ORDER BY total_payment DESC
LIMIT 10;

-- 7. Total rentals per store
SELECT s.store_id, COUNT(r.rental_id) AS rental_count
FROM store s
JOIN staff st ON s.store_id = st.store_id
JOIN rental r ON st.staff_id = r.staff_id
GROUP BY s.store_id;

-- 8. Films with the longest rental duration
SELECT title, rental_duration
FROM film
ORDER BY rental_duration DESC
LIMIT 10;

-- 9. Total payments per month
SELECT DATE_TRUNC('month', payment_date) AS month, SUM(amount) AS total_revenue
FROM payment
GROUP BY month
ORDER BY month;

-- 10. Average payment amount per country
SELECT co.country, AVG(p.amount) AS avg_payment
FROM payment p
JOIN customer c ON p.customer_id = c.customer_id
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
GROUP BY co.country
ORDER BY avg_payment DESC;
