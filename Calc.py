import streamlit as st
from fractions import Fraction

# --- Настройки и Функции (остаются без изменений) ---
TOLERANCE = 1e-3

def inch_to_mm(inches):
    """Конвертирует дюймы в миллиметры."""
    return inches * 25.4

def is_close(a, b, tol=TOLERANCE):
    """Проверяет, близки ли два числа друг к другу в пределах допуска."""
    return abs(a - b) < tol

def find_nearest(values, target):
    """Находит ближайшие меньшее и большее значения в списке."""
    less = greater = None
    for v in values:
        if v < target and (less is None or target - v < target - less):
            less = v
        if v > target and (greater is None or v - target < greater - target):
            greater = v
    return less, greater

def find_gauge_by_mm(mm_dict, mm_val):
    """Находит номер калибра по значению в миллиметрах."""
    for mm, gauge in mm_dict.items():
        if is_close(mm, mm_val):
            return gauge
    return None

# --- Данные (загружаются один раз при запуске) ---

# Таблицы калибров
steel_mm_to_gauge = {
    6.073: 3, 5.695: 4, 5.314: 5, 4.935: 6, 4.554: 7, 4.176: 8, 3.797: 9,
    3.416: 10, 3.038: 11, 2.657: 12, 2.278: 13, 1.897: 14, 1.709: 15,
    1.519: 16, 1.367: 17, 1.214: 18, 1.062: 19, 0.912: 20, 0.836: 21,
    0.759: 22, 0.683: 23, 0.607: 24, 0.531: 25, 0.455: 26, 0.378: 28
}
galvanized_mm_to_gauge = {
    4.27: 8, 3.891: 9, 3.51: 10, 3.132: 11, 2.753: 12, 2.372: 13,
    1.994: 14, 1.803: 15, 1.613: 16, 1.46: 17, 1.311: 18, 1.158: 19,
    1.006: 20, 0.93: 21, 0.853: 22, 0.777: 23, 0.701: 24, 0.627: 25,
    0.551: 26, 0.475: 28
}
stainless_mm_to_gauge = {
    4.762: 7, 4.366: 8, 3.97: 9, 3.571: 10, 3.175: 11, 2.779: 12,
    2.388: 13, 1.984: 14, 1.778: 15, 1.587: 16, 1.422: 17, 1.27: 18,
    1.118: 19, 0.952: 20, 0.864: 21, 0.787: 22, 0.711: 23, 0.635: 24,
    0.559: 25, 0.483: 26, 0.406: 28
}
aluminum_mm_to_gauge = {
    4.115: 6, 3.665: 7, 3.264: 8, 2.906: 9, 2.588: 10, 2.304: 11,
    2.052: 12, 1.829: 13, 1.628: 14, 1.448: 15, 1.29: 16, 1.143: 17,
    1.024: 18, 0.914: 19, 0.813: 20, 0.711: 21, 0.635: 22, 0.584: 23,
    0.508: 24, 0.457: 25, 0.432: 26, 0.32: 28
}
gauge_maps = {
    "Steel Gauge": steel_mm_to_gauge, "Galvanized Steel Gauge": galvanized_mm_to_gauge,
    "Stainless Steel Gauge": stainless_mm_to_gauge, "Aluminum Gauge": aluminum_mm_to_gauge
}

# Дюймовые ряды
fractional_inches = [
    '1/64', '1/32', '3/64', '1/16', '5/64', '3/32', '7/64', '1/8', '9/64', '5/32', '11/64',
    '3/16', '13/64', '7/32', '15/64', '1/4', '17/64', '9/32', '19/64', '5/16', '21/64',
    '11/32', '23/64', '3/8', '25/64', '13/32', '27/64', '7/16', '29/64', '15/32', '31/64',
    '1/2', '33/64', '17/32', '35/64', '9/16', '37/64', '19/32', '39/64', '5/8', '41/64',
    '21/32', '43/64', '11/16', '45/64', '23/32', '47/64', '3/4', '49/64', '25/32', '51/64',
    '13/16', '53/64', '27/32', '55/64', '7/8', '57/64', '29/32', '59/64', '15/16', '61/64',
    '31/32', '63/64', '1'
]
decimal_inches = [float(Fraction(x)) for x in fractional_inches]
decimal_mm = [round(inch_to_mm(x), 3) for x in decimal_inches]
mm_to_fraction_map = {mm: frac for mm, frac in zip(decimal_mm, fractional_inches)}

# Метрический ряд
metric_standard_mm = [0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]

# --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
# Список рядов для обработки. Изменен порядок для соответствия запросу.
rows = [
    (list(steel_mm_to_gauge.keys()), "Сталь (Steel Gauge)"),
    (list(galvanized_mm_to_gauge.keys()), "Оцинкованная сталь (Galvanized)"),
    (list(stainless_mm_to_gauge.keys()), "Нержавеющая сталь (Stainless)"),
    (decimal_mm, "Дюймовые размеры (Fractional Inches)"), # <-- ПЕРЕМЕЩЕНО СЮДА
    (list(aluminum_mm_to_gauge.keys()), "Алюминий (Aluminum Gauge)"),
    (metric_standard_mm, "Метрический стандарт")
]

# --- Интерфейс приложения Streamlit ---

st.set_page_config(page_title="Калькулятор толщины металла", layout="wide")
st.title("⚙️ Калькулятор толщины листового металла")
st.info("Введите значение в миллиметрах (например, `3.5`) или в дюймах в виде дроби (например, `1/8`).")

# Поле для ввода
user_input = st.text_input("Введите толщину для анализа:", "")

# Основная логика выполняется только если есть ввод
if user_input:
    target_mm = 0
    
    # --- Парсинг ввода ---
    try:
        if '/' in user_input:
            input_fraction = Fraction(user_input)
            target_mm = inch_to_mm(float(input_fraction))
            st.write(f"> **Принято к расчету:** `{user_input}\"` (дюймы), что равно **`{target_mm:.3f}` мм**")
        else:
            target_mm = float(user_input)
            st.write(f"> **Принято к расчету:** **`{target_mm}` мм**")
    except (ValueError, ZeroDivisionError):
        st.error(f"Ошибка: Некорректный формат ввода '{user_input}'. Введите число или дюймовую дробь.")
        st.stop() # Останавливаем выполнение скрипта

    st.markdown("---") # Разделитель
    
    # --- Основной блок вычислений и вывода ---
    standard_found = False
    
    # Используем колонки для более компактного отображения
    cols = st.columns(3)
    col_idx = 0

    for values_mm, label in rows:
        less, greater = find_nearest(values_mm, target_mm)
        
        # Выбираем текущую колонку для вывода
        current_col = cols[col_idx % 3]
        
        with current_col:
            st.subheader(label)
            
            # Формируем строки для вывода
            if less:
                if label == "Дюймовые размеры (Fractional Inches)":
                    st.write(f"**Ближайшее меньшее:** `{less}` мм (`{mm_to_fraction_map.get(less, '')}\")")
                else:
                    st.write(f"**Ближайшее меньшее:** `{less}` мм")
            
            if greater:
                if label == "Дюймовые размеры (Fractional Inches)":
                     st.write(f"**Ближайшее большее:** `{greater}` мм (`{mm_to_fraction_map.get(greater, '')}\")")
                else:
                     st.write(f"**Ближайшее большее:** `{greater}` мм")

            # Поиск точного совпадения
            for v in values_mm:
                if is_close(v, target_mm):
                    standard_found = True
                    # Для калибров ищем ключ "Steel" в названии, чтобы сопоставить с gauge_maps
                    gauge_key = next((k for k in gauge_maps.keys() if k in label), None)
                    gauge = find_gauge_by_mm(gauge_maps.get(gauge_key, {}), v)
                    
                    if gauge:
                        st.success(f"✅ **Стандарт:** `{v}` мм (Gauge `{gauge}`)")
                    elif label == "Дюймовые размеры (Fractional Inches)":
                        st.success(f"✅ **Стандарт:** `{v}` мм (`{mm_to_fraction_map.get(v, '')}\")")
                    else:
                        st.success(f"✅ **Стандарт:** `{v}` мм")
            
            st.markdown('<hr style="margin-top: 1em; margin-bottom: 1em;">', unsafe_allow_html=True)

        col_idx += 1


    if not standard_found:
        st.warning("ℹ️ Точное стандартное значение не найдено ни в одном из рядов.")