import streamlit as st
from predict import predict_safety
from train_model import TSmodel
from utils import load_db, preprocess_data
from correlations import show_correlations
import pandas as pd

st.title("Аналітика якості повітря для алергіків")

df = load_db()
df = preprocess_data(df)

menu = st.sidebar.radio("Меню", ["Рекомендації за місяцем", "Передбачення по введеним параметрам", "Тренування моделі" , "Залежності"])

if menu == "Рекомендації за місяцем":

    if 'day' not in df.columns:
        df['day'] = df['last_updated'].dt.day

    if 'country' not in df.columns:
        st.error("У таблиці немає колонки 'country'")
    else:
        country = st.selectbox("Оберіть країну", sorted(df['country'].unique()))
        
        country_df = df[df['country'] == country]
        
        if country_df.empty:
            st.warning("Немає даних для вибраної країни.")
        else:

            month = st.selectbox("Оберіть місяць", sorted(country_df['month'].unique()))

            month_df = country_df[country_df['month'] == month]

            if month_df.empty:
                st.warning("Немає даних для вибраного місяця.")
            else:
                recommendations = []

                for day in sorted(month_df['day'].unique()):
                    daily_data = month_df[month_df['day'] == day]
                    avg_pm = daily_data['air_quality_pm2_5'].mean()

                    if avg_pm < 10:
                        recommendation = "🟢 Повітря чисте. Можна виходити алергіку."
                    elif avg_pm < 25:
                        recommendation = "🟡 Помірна якість. Можна виходити, але з обережністю."
                    else:
                        recommendation = "🔴 Високий рівень забруднення. Краще залишитись вдома."

                    recommendations.append([day, round(avg_pm, 1), recommendation])

                recommendation_df = pd.DataFrame(recommendations, columns=["День", "Середнє PM2.5", "Рекомендація"])
                st.table(recommendation_df)

elif menu == "Передбачення по введеним параметрам":
    st.subheader("Введіть погодні та хімічні параметри:")
    temperature = st.slider("Температура (°C)", -20, 45, 20)
    humidity = st.slider("Вологість (%)", 0, 100, 50)
    uv_index = st.slider("UV Index", 0, 11, 3)
    pm10 = st.slider("PM10", 0, 300, 20)
    no2 = st.slider("NO2", 0.0, 0.2, 0.02)
    co = st.slider("CO", 0.0, 2.0, 0.4)

    input_data = pd.DataFrame([[temperature, humidity, uv_index, pm10, no2, co]],
                              columns=['temperature_celsius', 'humidity', 'uv_index',
                                       'air_quality_pm10', 'air_quality_nitrogen_dioxide',
                                       'air_quality_carbon_monoxide'])

    result = predict_safety(input_data)[0]
    if result == 1:
        st.success("✅ Можна виходити алергіку")
    else:
        st.error("🚫 Краще залишитись вдома")

elif menu == "Тренування моделі":
    st.subheader("Навчання моделі")
    if st.button("навчити модель"):
        acc = TSmodel(df)
        st.success(f"Модель навчена. Точність: {acc:.2f}")

if menu == "Залежності":
    st.subheader("Залежності")
    if st.button("показати залежності"):
        show_correlations()
