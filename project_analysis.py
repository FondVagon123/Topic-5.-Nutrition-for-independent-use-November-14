import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import os

CURRENT_DATE = date(2025, 11, 11)
EXCHANGE_RATE = 40.5
GRAPH_FILE_NAME = 'Графік_Автопром_2024.png'

def create_project_data(year):
    if year == 2024:
        data = {
            'Назва проекту': ['Седан A (Hybrid)', 'Кросовер B (EV)', 'Мінівен C (Safety)', 'Седан A (Hybrid)', 'Кросовер D (Luxury)', 'Кросовер B (EV)'],
            'Назва клієнта': ['Toyota', 'Nissan', 'Honda', 'Suzuki', 'Toyota', 'Honda'],
            'Адреса': ['Японія', 'США', 'Європа', 'Індія', 'Японія', 'США'],
            'Дата початку проекту': [
                '2024-01-15', '2024-04-20', '2024-08-10', '2024-03-01', '2024-10-05', '2024-06-12'
            ],
            'Ключова технологія': ['Гібридна система THS', 'Модульна EV-платформа', 'Система Honda Sensing', 'Економічні ДВЗ', 'Преміальний інтер\'єр', 'Модульна EV-платформа'],
            'Од. виміру прибутку': ['USD', 'USD', 'USD', 'USD', 'USD', 'USD'],
            'Прибуток/од. (у.о.)': [2500, 3500, 1800, 1000, 5000, 3500],
            'Кількість продано (тис.)': [500.0, 100.0, 150.0, 200.0, 50.0, 80.0]
        }
    else:
        data = {
            'Назва проекту': ['Пікап E (Premium)', 'Спорткар F (EV)', 'Компакт G (Global)', 'Пікап E (Premium)', 'Кросовер H (EV)', 'Компакт G (Global)'],
            'Назва клієнта': ['Toyota', 'Nissan', 'Honda', 'Mazda', 'Toyota', 'Mazda'],
            'Адреса': ['США', 'Європа', 'Азія', 'Японія', 'Європа', 'Азія'],
            'Дата початку проекту': [
                '2025-01-05', '2025-05-15', '2025-09-20', '2025-02-10', '2025-11-01', '2025-07-01'
            ],
            'Ключова технологія': ['Надійна трансмісія', 'Високоефективна батарея', 'Глобальна платформа', 'Роторний EV-рейндж', 'Високоефективна батарея', 'Глобальна платформа'],
            'Од. виміру прибутку': ['USD', 'USD', 'USD', 'USD', 'USD', 'USD'],
            'Прибуток/од. (у.о.)': [3000, 4500, 1500, 2800, 4500, 1500],
            'Кількість продано (тис.)': [150.0, 80.0, 400.0, 70.0, 120.0, 30.0]
        }
    df = pd.DataFrame(data)
    df['Рік'] = year
    return df

def calculate_fields(df, exchange_rate):
    df['Дата початку проекту'] = pd.to_datetime(df['Дата початку проекту'])
    df['Квартал'] = df['Дата початку проекту'].dt.to_period('Q').dt.strftime('Квартал %q')
    df['Прибуток/од. в грн'] = df['Прибуток/од. (у.о.)'] * exchange_rate
    df['Заг. прибуток у.о. (тис.)'] = df['Кількість продано (тис.)'] * df['Прибуток/од. (у.о.)']
    df['Заг. прибуток грн (тис.)'] = df['Кількість продано (тис.)'] * df['Прибуток/од. в грн']
    return df

def create_pivot_table(df):
    pivot_full = pd.pivot_table(
        df,
        values='Заг. прибуток грн (тис.)',
        index=['Квартал', 'Ключова технологія'],
        columns='Назва клієнта',
        aggfunc='sum',
        fill_value=0
    )
    return pivot_full.sort_index()

def generate_and_save_graph(df, year, file_name):
    tech_summary = df.groupby('Ключова технологія')['Заг. прибуток грн (тис.)'].sum().sort_values(ascending=False)
    summary_in_mil = tech_summary / 1_000_000
    plt.figure(figsize=(12, 7))
    bars = summary_in_mil.plot(
        kind='bar',
        color=plt.cm.viridis(np.linspace(0, 1, len(summary_in_mil)))
    )
    plt.title(f'Аналіз загального прибутку за ключовими технологіями, {year}', fontsize=14)
    plt.xlabel('Ключова технологія', fontsize=12)
    plt.ylabel('Загальний прибуток (млн. грн)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars.patches:
        plt.annotate(
            f'{bar.get_height():,.1f}M',
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha='center', va='bottom', fontsize=10, color='black'
        )
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    return file_name

df_2024 = create_project_data(2024)
df_2024 = calculate_fields(df_2024, EXCHANGE_RATE)
df_2025 = create_project_data(2025)
df_2025 = calculate_fields(df_2025, EXCHANGE_RATE)

print(f"==================================================================================")
print(f"Звіт: {df_2024['Рік'].iloc[0]} | Дата: {CURRENT_DATE} | Курс (у.о./грн): {EXCHANGE_RATE}")
print(f"==================================================================================")
print("\n--- ТАБЛИЦЯ З ДАНИМИ АВТОМОБІЛЬНОЇ ГАЛУЗІ (перші 5 рядків) ---")
print(df_2024[[
    'Дата початку проекту', 'Квартал', 'Назва клієнта', 'Ключова технологія',
    'Прибуток/од. (у.о.)', 'Прибуток/од. в грн', 'Кількість продано (тис.)',
    'Заг. прибуток у.о. (тис.)', 'Заг. прибуток грн (тис.)'
]].head().to_markdown(index=False))

pivot_2024 = create_pivot_table(df_2024)
print("\n--- ЗВЕДЕНА ТАБЛИЦЯ (Аналіз загального прибутку за технологіями) ---")
print("Рядки: Квартал, Ключова технологія | Стовпці: Виробник | Значення: Сума Заг. прибутку (тис. грн)")
print("----------------------------------------------------------------------------------")
print(pivot_2024.to_markdown())

generated_graph_file = GRAPH_FILE_NAME
try:
    generate_and_save_graph(df_2024, 2024, generated_graph_file)
    print(f"\n[ГРАФІК]: Успішно створено файл візуалізації: '{generated_graph_file}'")
except Exception as e:
    generated_graph_file = None
    if 'module' in str(e) and 'matplotlib' in str(e):
        print(f"\n[ПОМИЛКА ГРАФІКА]: Не вдалося створити графік. Переконайтеся, що встановлено бібліотеки 'matplotlib' та 'numpy' (pip install matplotlib numpy).")
    else:
        print(f"\n[ПОМИЛКА ГРАФІКА]: Не вдалося створити графік. Переконайтеся, що встановлено matplotlib. Помилка: {e}")

writer_name = 'Звіт_Автопром_Аналіз_Моделей.xlsx'
try:
    with pd.ExcelWriter(writer_name, engine='xlsxwriter') as writer:
        df_2024.to_excel(writer, sheet_name='2024_Автомоделі', index=False)
        worksheet_2024 = writer.sheets['2024_Автомоделі']
        worksheet_2024.write('A1', f'Сьогоднішня дата: {CURRENT_DATE}')
        worksheet_2024.write('A2', f'Курс (у.о./грн): {EXCHANGE_RATE}')
        worksheet_2024.write('A3', f'Рік даних: {df_2024["Рік"].iloc[0]}')
        df_2025.to_excel(writer, sheet_name='2025_Автомоделі', index=False)
        worksheet_2025 = writer.sheets['2025_Автомоделі']
        worksheet_2025.write('A1', f'Сьогоднішня дата: {CURRENT_DATE}')
        worksheet_2025.write('A2', f'Курс (у.о./грн): {EXCHANGE_RATE}')
        worksheet_2025.write('A3', f'Рік даних: {df_2025["Рік"].iloc[0]}')
    print("\n----------------------------------------------------------------------------------")
    print(f"УСПІХ! Створено файл '{writer_name}'.")
    if generated_graph_file and os.path.exists(generated_graph_file):
         print(f"Також створено графік '{generated_graph_file}'.")
    print("----------------------------------------------------------------------------------")
except ImportError:
    print("\n\nПОМИЛКА: Не встановлена бібліотека 'xlsxwriter'.")
    print("Для експорту даних у файл виконайте: pip install openpyxl xlsxwriter")
except Exception as e:
    print(f"\n\nПомилка при експорті в Excel: {e}")
