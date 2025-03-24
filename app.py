import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Загружаем модель (здесь предполагается, что "career_model.pkl" уже обучен и лежит рядом)
model = joblib.load("career_model.pkl")

# Список всех профессий для выбора/фильтра
PROFESSIONS = [
    "Инженер-механик", "Инженер-электрик", "Инженер-строитель", "Инженер-химик", 
    "Инженер-робототехник", "Авиакосмический инженер", "Инженер-эколог", "Архитектор",
    "Сварщик", "Электрик", "Автомеханик", "Пилот (лётчик)", "Специалист по 3D-печати", 
    "Наноинженер", "Инженер-нефтяник", "Геолог", "Инженер-мехатроник", "Инженер-энергетик", 
    "Космонавт", "Филолог", "Переводчик", "Историк", "Юрист", "Политолог", "Социолог", 
    "Философ", "Библиотекарь", "Редактор", "Журналист", "Археолог", "Врач", "Хирург", 
    "Стоматолог", "Ветеринар", "Фармацевт", "Медсестра (Медбрат)", "Фельдшер", "Психиатр",
    "Физиотерапевт", "Диетолог", "Массажист", "Художник", "Музыкант", "Актёр", "Режиссёр",
    "Графический дизайнер", "Модельер (дизайнер одежды)", "Дизайнер интерьера", "Фотограф",
    "Видеомонтажёр", "Аниматор (мультипликатор)", "Скульптор", "Писатель", "Копирайтер",
    "Танцор", "Ювелир", "Повар (шеф-повар)", "Парикмахер", "Учитель", 
    "Воспитатель детского сада", "Социальный работник", "Психолог (консультант)",
    "Спортивный тренер", "Полицейский", "Военный офицер", "Пожарный", 
    "Менеджер по персоналу (HR)", "Event-менеджер", "Менеджер по туризму", 
    "Экскурсовод (гид)", "Логопед (дефектолог)", "Программист", "Веб-разработчик", 
    "Мобильный разработчик", "Аналитик данных (Data Analyst)", "Системный администратор", 
    "Специалист по кибербезопасности", "Администратор баз данных",
    "Специалист по искусственному интеллекту (AI)", "Сетевой инженер",
    "Специалист техподдержки (IT)", "Тестировщик ПО (QA-инженер)", "UX/UI дизайнер",
    "Гейм-дизайнер", "Разработчик игр", "Контент-менеджер", "SEO-специалист",
    "SMM-менеджер (специалист по соц. медиа)", "3D-дизайнер (3D-моделлер)", 
    "Блогер (контент-креатор)", "Экономист", "Бухгалтер", "Финансовый аналитик", 
    "Маркетолог", "Продукт-менеджер", "Менеджер по продажам", "Менеджер проектов", 
    "Бизнес-аналитик", "Логист", "Предприниматель"
]

st.set_page_config(page_title="Профориентация", layout="centered")
st.title("🎓 Рекомендательная система профориентации")

st.markdown("""
Введите информацию о себе, и система предложит наиболее подходящие профессии.

**Блок 1. Оценки по предметам**  
Укажите свою фактическую оценку за текущую четверть/семестр *по 5-балльной шкале* (можно вводить десятичные значения, например 4.50).  
Сервис автоматически переведёт её в проценты и выставит соответствующий слайдер.  
Вы можете при необходимости подправить значение на слайдере, если считаете, что ваш уровень знаний лучше/хуже, чем показывает формула.
""")

def input_grade_and_slider(subject_name, default_grade=4.0):
    # Числовой ввод оценки по 5-балльной шкале (можно с десятичной частью)
    grade = st.number_input(f"Оценка за последнюю четверть/семестр по {subject_name} (1.0 - 5.0)",
                            min_value=1.0, max_value=5.0, value=default_grade, step=0.01)
    # Переводим оценку в проценты
    grade_percentage = int(round((grade / 5.0) * 100))
    # Выводим слайдер, где по умолчанию установлено вычисленное значение
    percentage = st.slider(f"Процент владения предметом {subject_name}", 0, 100, grade_percentage)
    return percentage

# Получаем значения для основных предметов
math = input_grade_and_slider("математике")
bio = input_grade_and_slider("биологии")
inf = input_grade_and_slider("информатике")
lit = input_grade_and_slider("литературе")
eng = input_grade_and_slider("английскому языку")

st.markdown("""
**Блок 2. Интересы**  
Оцените по 10-балльной шкале свою мотивацию и увлечённость в разных областях. Если сомневаетесь, можете пройти тест, например 
[здесь](https://bvbinfo.ru/lk-student/realizing), чтобы точнее оценить свои интересы.
""")

tech = st.slider("Интерес к техническим наукам (0-10)", 0, 10, 5)
art = st.slider("Интерес к творчеству (0-10)", 0, 10, 5)
social = st.slider("Интерес к людям и помощи (0-10)", 0, 10, 5)

st.markdown("""
**Блок 3. Тип личности**  
Для более точной оценки рекомендуем пройти тест на [my-type.ru](https://my-type.ru/) и определить свой MBTI.  
После прохождения теста выберите полученные буквы в полях ниже.
""")

ei = st.selectbox("Экстраверт (E) или Интроверт (I)", ["E", "I"])
sn = st.selectbox("Ощущение (S) или Интуиция (N)", ["S", "N"])
tf = st.selectbox("Мышление (T) или Чувства (F)", ["T", "F"])
jp = st.selectbox("Суждение (J) или Восприятие (P)", ["J", "P"])

# Преобразуем MBTI в бинарные флаги (пример)
ei_bin = 1 if ei == "E" else 0
sn_bin = 1 if sn == "S" else 0
tf_bin = 1 if tf == "T" else 0
jp_bin = 1 if jp == "J" else 0

# Кнопка для запуска рекомендаций
if st.button("🔍 Подобрать профессию"):
    features = np.array([[math, bio, inf, lit, eng, tech, art, social, 
                          ei_bin, sn_bin, tf_bin, jp_bin]])
    proba = model.predict_proba(features)[0]
    classes = model.classes_

    # Индексы топ-5 профессий
    top_indices = proba.argsort()[-5:][::-1]
    top_scores = proba[top_indices]

    # Нормализуем, чтобы сумма топ-5 была 1 (далее умножаем на 100)
    norm_top_scores = top_scores / top_scores.sum()

    results = []
    labels = []
    scores = []

    for j, i in enumerate(top_indices):
        profession = classes[i]
        probability = round(norm_top_scores[j] * 100, 2)

        # Простейший пример "причин"
        reasons = []
        if tech > 7:
            reasons.append("интерес к техническим наукам")
        if art > 7:
            reasons.append("творческие способности")
        if social > 7:
            reasons.append("интерес к людям")
        if bio > 85:
            reasons.append("сильная биология")
        if inf > 85:
            reasons.append("сильная информатика")

        reason_text = ", ".join(reasons) if reasons else "подходит по общему профилю"

        results.append({
            "Профессия": profession,
            "Вероятность": f"{probability}%",
            "Причины": reason_text
        })

        labels.append(profession)
        scores.append(probability)

    st.success("🎯 Ваши топ-5 профессий:")
    df_result = pd.DataFrame(results)
    df_result.index = [f"#{i+1}" for i in range(len(df_result))]
    st.dataframe(df_result)

    # Построим простой горизонтальный барчарт
    fig, ax = plt.subplots()
    ax.barh(labels[::-1], scores[::-1])
    ax.set_xlabel("Нормализованная вероятность (%)")
    ax.set_title("Наиболее подходящие профессии")
    st.pyplot(fig)

    # Кнопка для скачивания результатов в CSV
    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Скачать рекомендации (CSV)",
        data=csv,
        file_name='career_recommendations.csv',
        mime='text/csv'
    )

st.markdown("---")

# Блок отзывов
st.header("Отзывы пользователей")

st.write("Оставьте отзыв о профессии и оцените наш сервис звёздочками.")

REVIEWS_FILE = "reviews.xlsx"

# Загружаем или создаём файл с отзывами
if os.path.exists(REVIEWS_FILE):
    reviews_df = pd.read_excel(REVIEWS_FILE)
else:
    reviews_df = pd.DataFrame(columns=["Профессия", "Имя", "Отзыв", "Оценка сервиса"])

with st.form("review_form", clear_on_submit=True):
    st.subheader("Оставить отзыв")
    selected_profession = st.selectbox("Профессия", PROFESSIONS)
    user_name = st.text_input("Ваше имя (необязательно)")
    user_feedback = st.text_area("Ваш отзыв")

    # Настраиваем варианты со звёздочками
    star_options = {
        5: "★★★★★",
        4: "★★★★☆",
        3: "★★★☆☆",
        2: "★★☆☆☆",
        1: "★☆☆☆☆"
    }

    # Радио-кнопки со звёздочками
    # Порядок - от 5 до 1, чтобы по умолчанию пользователь видел "5" (самый высокий рейтинг) первым
    rating = st.radio(
        "Оцените сервис:",
        [5, 4, 3, 2, 1],
        index=0,  # по умолчанию выбрана самая высокая оценка
        format_func=lambda x: star_options[x]
    )

    submit_review = st.form_submit_button("Сохранить отзыв")

    if submit_review:
        if user_feedback.strip():
            new_row = {
                "Профессия": selected_profession,
                "Имя": user_name if user_name.strip() else "Аноним",
                "Отзыв": user_feedback.strip(),
                # Сохраняем именно числовое значение рейтинга, 
                # но при отображении или анализе можем снова конвертировать в звёздочки
                "Оценка сервиса": rating  
            }
            new_row_df = pd.DataFrame([new_row])
            reviews_df = pd.concat([reviews_df, new_row_df], ignore_index=True)
            reviews_df.to_excel(REVIEWS_FILE, index=False, engine="openpyxl")
            st.success("Отзыв сохранён!")
        else:
            st.error("Пожалуйста, введите текст отзыва.")

# Просмотр отзывов
st.markdown("### Все отзывы")

filter_profession = st.selectbox("Фильтр по профессии (или 'Все')", ["Все"] + PROFESSIONS)
if filter_profession == "Все":
    filtered_reviews = reviews_df
else:
    filtered_reviews = reviews_df[reviews_df["Профессия"] == filter_profession]

# Если хотите, чтобы в таблице рейтинги тоже отображались «звёздочками»:
# Можно применить преобразование перед выводом
def convert_rating_to_stars(r):
    return star_options.get(r, "—")

star_options = {
    5: "★★★★★",
    4: "★★★★☆",
    3: "★★★☆☆",
    2: "★★☆☆☆",
    1: "★☆☆☆☆"
}

# Копируем, чтобы не менять оригинальный датафрейм
display_df = filtered_reviews.copy()

if not display_df.empty:
    display_df["Оценка сервиса"] = display_df["Оценка сервиса"].apply(convert_rating_to_stars)

st.dataframe(display_df)