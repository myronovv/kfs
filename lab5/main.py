import streamlit as st
import matplotlib.pyplot as plt
import random
import mysql.connector
from genetic_tsp import run_genetic_algorithm

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2505", 
        database="tsp_db"
    )

# генерація міст 
def generate_random_cities(n, x_range=(0, 100), y_range=(0, 100)):
    return [(random.randint(*x_range), random.randint(*y_range)) for _ in range(n)]

# візуалізація маршруту
def plot_route(route, title="Маршрут"):
    plt.figure(figsize=(8, 6))
    x = [point[0] for point in route] + [route[0][0]]
    y = [point[1] for point in route] + [route[0][1]]
    plt.plot(x, y, 'o-', color='blue')
    for i, (px, py) in enumerate(route):
        plt.text(px + 1, py + 1, str(i + 1), fontsize=9)
    plt.title(title)
    plt.grid(True)
    st.pyplot(plt)

# запис в бд 
def save_to_db(cities, best_route, best_distance, num_cities, max_iterations):
    conn = connect_db()
    cursor = conn.cursor()

    # додаємо запис про запуск
    cursor.execute("""
        INSERT INTO runs (num_cities, max_iterations, best_distance)
        VALUES (%s, %s, %s)
    """, (num_cities, max_iterations, best_distance))
    run_id = cursor.lastrowid

    # зберігаємо початкові міста
    for i, (x, y) in enumerate(cities):
        cursor.execute("""
            INSERT INTO cities (run_id, city_index, x, y)
            VALUES (%s, %s, %s, %s)
        """, (run_id, i, x, y))

    # зберігаємо найкращий маршрут
    for i, (x, y) in enumerate(best_route):
        cursor.execute("""
            INSERT INTO best_route (run_id, city_order, x, y)
            VALUES (%s, %s, %s, %s)
        """, (run_id, i, x, y))

    conn.commit()
    conn.close()
    return run_id

# інтерфейс
st.title("🧠 Елітний генетичний алгоритм — Задача комівояжера")

num_cities = st.slider("Кількість міст", min_value=5, max_value=30, value=10)
max_iterations = st.slider("Кількість ітерацій", min_value=1, max_value=500, value=250)

# параметри
num_individuals = 100
mutation_rate = 0.05
elite_size = 2
stable_limit = 100

if st.button("🔁 Запустити алгоритм"):
    cities = generate_random_cities(num_cities)

    st.subheader("📍 Початкові міста:")
    for i, city in enumerate(cities):
        st.write(f"{i + 1}: {city}")

    best_route, best_distance = run_genetic_algorithm(
        cities,
        num_individuals=num_individuals,
        max_iterations=max_iterations,
        mutation_rate=mutation_rate,
        elite_size=elite_size,
        stable_limit=stable_limit,
        verbose=False
    )

    st.subheader("🏁 Найкраща знайдена особина (маршрут):")
    for i, city in enumerate(best_route):
        st.write(f"{i + 1}: {city}")

    st.success(f"Загальна довжина маршруту: {best_distance:.2f}")
    plot_route(best_route, title="Найкращий знайдений маршрут")

    # зберігання в бд
    run_id = save_to_db(cities, best_route, best_distance, num_cities, max_iterations)
    st.info(f"✅ Результати збережено в БД - ID запуску: {run_id}")
