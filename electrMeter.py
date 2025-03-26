import streamlit as st
import subprocess

class ElectricityMeter:
    def __init__(self, meterId, day, night):
        self.meterId = meterId
        self.previousDay = day
        self.previousNight = night
        self.total_cost = 0

    def update(self, currentDay, currentNight, day_rate, night_rate):
        if currentDay < self.previousDay:
            if self.previousDay + 100 > currentDay:
                updatedDay = self.previousDay + 100
            else:
                updatedDay = currentDay
        else:
            updatedDay = currentDay

        if currentNight < self.previousNight:
            if self.previousNight + 80 > currentNight:
                updatedNight = self.previousNight + 80
            else:
                updatedNight = currentNight
        else:
            updatedNight = currentNight

        dayUse = updatedDay - self.previousDay
        nightUse = updatedNight - self.previousNight

        cost = (dayUse * day_rate) + (nightUse * night_rate)
        self.total_cost = self.total_cost + cost

        self.previousDay = updatedDay
        self.previousNight = updatedNight

        return cost


def costMeter(meters, meterId, currentDay, currentNight, day_rate, night_rate):
    for meter in meters:
        if meter.meterId == meterId:
            cost = meter.update(currentDay, currentNight, day_rate, night_rate)
            return meters, cost

    new_meter = ElectricityMeter(meterId, currentDay, currentNight)
    meters.append(new_meter)
    return meters, 0

st.title("Розрахунок вартості електроенергії")

meterId = st.text_input("Введіть ID лічильника:")
currentDay = st.number_input("Поточні денні показники (кВт):", 0.0)
currentNight = st.number_input("Поточні нічні показники (кВт):", 0.0)
day_rate = st.number_input("Тариф за день (грн/кВт):", 0.0, 1.5)
night_rate = st.number_input("Тариф за ніч (грн/кВт):", 0.0, 0.9)

if st.button("Розрахувати вартість"):
    if not meterId:
        st.error("Введіть id лічильника.")
    else:
        meters = st.session_state.get("meters", [])
        meters, cost = costMeter(meters, meterId, currentDay, currentNight, day_rate, night_rate)
        st.session_state.meters = meters

        st.success(f"Рахунок для лічильника {meterId}: {cost:.2f} грн")

if "meters" in st.session_state:
    st.subheader("Загальна інформація про лічильники")
    for meter in st.session_state.meters:
        st.write(f"Лічильник {meter.meterId}: Загальна вартість = {meter.total_cost:.2f} грн")

if st.button("Запустити тести"):
    st.write("Запуск тестів...")
    
    result = subprocess.run(["python", "electrMeterTest.py"], capture_output=True, text=True)
    
    st.subheader("Результати тестів")
    st.text(result.stdout)
    if result.returncode != 0:
        st.error("Тести завершилися з помилками.")
    else:
        st.success("Усі тести пройшли успішно!")