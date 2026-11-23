import tkinter as tk
import tksheet
import calendar
import datetime

# === ДАННЫЕ (из Лекции 4) ===
# Двумерный массив для записей: [Год, Нераб. дни, Високосный, Надбавка]
data_matrix = []
# Одномерный массив для истории действий
history_log = []


# === СОБЫТИЯ (из Лекции 6) ===
def update_history(action_text):
    """Добавление действия в историю"""
    history_log.append(action_text)
    history_text.delete(1.0, tk.END)
    for i, item in enumerate(history_log, 1):
        history_text.insert(tk.END, f"{i}. {item}\n")


def show_about():
    """Событие для кнопки 'О программе'"""
    update_history("Открыто окно 'О программе'")
    about_win = tk.Toplevel(root)
    about_win.title("О программе")
    about_win.geometry("300x150")

    label = tk.Label(about_win, text="Практическая работа №8\nВариант 12", font=("Arial", 12))
    label.pack(pady=20)

    close_btn = tk.Button(about_win, text="Закрыть", command=about_win.destroy)
    close_btn.pack(pady=10)


def add_record():
    """Добавление новой записи с авторасчетом"""
    if len(data_matrix) >= 5:
        update_history("Ошибка: Таблица уже заполнена (5 записей)")
        return

    try:
        year = int(entry_year.get())
        bonus = float(entry_bonus.get())

        # Встроенная логика расчета
        is_leap = "Да" if calendar.isleap(year) else "Нет"

        count_working = 0
        d = datetime.date(year, 1, 1)
        while d.year == year:
            if d.weekday() < 5:  # 0–4 = пн–пт
                count_working += 1
            d += datetime.timedelta(days=1)

        # Общее количество дней в году минус рабочие = нерабочие
        total_days = 366 if calendar.isleap(year) else 365
        non_working_days = total_days - count_working

        # Добавляем запись в двумерный массив
        data_matrix.append([year, non_working_days, is_leap, bonus])

        # Обновляем таблицу на экране
        sheet.set_sheet_data(data_matrix)
        update_history(f"Добавлена запись за {year} год")

        # Очищаем поля ввода
        entry_year.delete(0, tk.END)
        entry_bonus.delete(0, tk.END)

    except ValueError:
        update_history("Ошибка ввода! Проверьте данные.")


def calculate():
    """Сортировка и расчет"""
    if not data_matrix:
        update_history("Ошибка: Нет данных для расчета")
        return

    # Сортировка по году (теперь год находится под индексом 0)
    data_matrix.sort(key=lambda x: x[0])
    sheet.set_sheet_data(data_matrix)
    update_history("Выполнена сортировка по году")

    # Расчет суммы надбавок в високосные года (високосность под индексом 2, надбавка под индексом 3)
    total_bonus = 0
    for row in data_matrix:
        if row[2] == "Да":
            total_bonus += row[3]

    # Вывод результата
    result_label.config(text=f"Сумма надбавок в високосные года: {total_bonus}")
    update_history("Выполнен расчет суммы надбавок")


def clear_data():
    """Очистка всех данных"""
    data_matrix.clear()
    sheet.set_sheet_data([])
    result_label.config(text="Сумма надбавок в високосные года: 0")
    update_history("Данные таблицы очищены")


def exit_app():
    """Выход из программы"""
    root.destroy()


# === ГЛАВНОЕ ОКНО (из Лекции 6) ===
root = tk.Tk()
root.title("ПР №8. Вариант 12")
root.geometry("1000x600")

# Убираем иконку по умолчанию (заменяем на прозрачный пиксель)
root.iconphoto(False, tk.PhotoImage(width=1, height=1))

# --- Левая панель (Ввод данных) ---
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

tk.Label(input_frame, text="Введите год:").pack(anchor="w")
entry_year = tk.Entry(input_frame)
entry_year.pack(pady=5)

tk.Label(input_frame, text="Введите надбавку:").pack(anchor="w")
entry_bonus = tk.Entry(input_frame)
entry_bonus.pack(pady=5)

# Кнопки
btn_add = tk.Button(input_frame, text="Добавить запись", command=add_record)
btn_add.pack(pady=10, fill=tk.X)

btn_calc = tk.Button(input_frame, text="Расчет и сортировка", command=calculate)
btn_calc.pack(pady=5, fill=tk.X)

btn_clear = tk.Button(input_frame, text="Очистка", command=clear_data)
btn_clear.pack(pady=5, fill=tk.X)

# Результат
result_label = tk.Label(input_frame, text="Сумма надбавок в високосные года: 0", fg="blue", wraplength=150)
result_label.pack(pady=15)

# Кнопки меню снизу
btn_about = tk.Button(input_frame, text="О программе", command=show_about)
btn_about.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

btn_exit = tk.Button(input_frame, text="Выход", command=exit_app, fg="red")
btn_exit.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

# --- Центральная панель (Таблица) ---
table_frame = tk.Frame(root)
table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=20)

# Создание таблицы tksheet (без столбца "№")
sheet = tksheet.Sheet(table_frame, headers=["Год", "Нераб. дни", "Високосный", "Надбавка"])
sheet.pack(fill=tk.BOTH, expand=True)
sheet.set_sheet_data(data_matrix)

# --- Правая панель (История действий) ---
history_frame = tk.Frame(root)
history_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

tk.Label(history_frame, text="История действий:").pack(anchor="w")
history_text = tk.Text(history_frame, width=30, height=20)
history_text.pack()

# Запуск главного цикла окна
root.mainloop()