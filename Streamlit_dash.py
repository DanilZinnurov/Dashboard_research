import streamlit as st
import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import time
import numpy as np

def refresh_page():
    st.experimental_rerun()



def get_form_data():
    study = st.number_input('Во сколько лет вы освоили базовый функционал для работы аналитиком', 18, 70, step=5)
    work_age = st.number_input('Во сколько лет вы устроились на работу', 18, 75, step=5)
    growth = st.number_input('Оцените по 10-бальной шкале как выросли ваши навыки за время пока вы искали работу', 0, 10, step=1)
    growth_with_work = st.number_input('Оцените по 10-бальной шкале как выросли ваши навыки за первые полгода '
                                       'как вы устроились на работу', 0, 10, step=1)

    if st.button('Submit'):
        result = []
        result.append(study)
        result.append(work_age)
        result.append(growth)
        result.append(growth_with_work)
        st.write("Спасибо за участие в опросе!")

        sqlite_insert_query = f"""INSERT INTO docs
                                  (final_study, work_age, growth, growth_with_work)
                                  VALUES
                                  ({result[0]}, {result[1]}, {result[2]}, {result[3]});"""
        cursor.execute(sqlite_insert_query)
        connection.commit()



plt.style.use('dark_background')

connection = sqlite3.connect('docs.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS docs
              (final_study INT, work_age INT, growth INT, growth_with_work INT)''')
connection.commit()


df = pd.read_sql('SELECT * FROM docs', connection)
st.title('Опрос')
get_form_data()


plt.figure()
plt.hist(df['final_study'], bins=10, edgecolor='black')
plt.title('График распределения возраста людей, поучаствовавших в опросе')
plt.xlabel('Возраст')
plt.ylabel('Количество людей')
plt.grid(True, alpha=0.3)
st.pyplot(plt)


plt.figure()
plt.hist(df['work_age'] - df['final_study'],
         bins=9, edgecolor='black', orientation='horizontal')
plt.grid(True, alpha=0.3)
plt.xlim(0)
plt.title('Сколько лет прошло, пока люди искали работу')
plt.xlabel('Количество лет')
plt.ylabel('Количество людей')
new_list = range(min(df['work_age'] - df['final_study']), max(df['work_age'] - df['final_study'])+1)
plt.yticks(new_list)
st.pyplot(plt)



plt.figure(figsize=(8, 8))
plt.plot(df.growth[len(df) - 100:], label='оценка роста навыков во время простоя')
plt.plot(df.growth_with_work[len(df) - 100:], label='оценка роста навыков на работе')
plt.title("График роста навыков")
plt.grid (True, linestyle='-', color='orange', linewidth= 0.5, alpha=0.3)
plt.ylim(0, 10)
plt.legend(loc='upper right')
st.pyplot(plt)


cursor.close()

while True:
        time.sleep(5)
        refresh_page()
