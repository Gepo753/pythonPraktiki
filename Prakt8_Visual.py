import tkinter as tk
import tksheet
import calendar
import datetime

matrix = []
history = []

def update_history(action_text):
    history.append(action_text)
    txt_hist.delete(1.0, tk.END)
    for i, item in enumerate(history, 1):
        txt_hist.insert(tk.END, f"{i}. {item}\n")

def show_about():
    update_history("Открыто окно 'О программе'")
    win_about = tk.Toplevel(root)
    win_about.title("О программе")
    win_about.geometry("300x150")

    lbl = tk.Label(win_about, text="Практическая работа №8\nВариант 12", font=("Arial", 12))
    lbl.pack(pady=20)

    btn_close = tk.Button(win_about, text="Закрыть", command=win_about.destroy)
    btn_close.pack(pady=10)

def add_record():
    if len(matrix) >= 5:
        update_history("Ошибка: Таблица уже заполнена (5 записей)")
        return

    try:
        y = int(ent_year.get())
        b = float(ent_bonus.get())

        leap = "Да" if calendar.isleap(y) else "Нет"

        work_days = 0
        date = datetime.date(y, 1, 1)
        while date.year == y:
            if date.weekday() < 5:  # 0–4 = пн–пт
                work_days += 1
            date += datetime.timedelta(days=1)

        total = 366 if calendar.isleap(y) else 365
        days_off = total - work_days

        matrix.append([y, days_off, leap, b])

        table.set_sheet_data(matrix)
        update_history(f"Добавлена запись за {y} год")

        ent_year.delete(0, tk.END)
        ent_bonus.delete(0, tk.END)

    except ValueError:
        update_history("Ошибка ввода! Проверьте данные.")

def calculate():
    if not matrix:
        update_history("Ошибка: Нет данных для расчета")
        return

    matrix.sort(key=lambda x: x[0])
    table.set_sheet_data(matrix)
    update_history("Выполнена сортировка по году")

    sum_bonus = 0
    for row in matrix:
        if row[2] == "Да":
            sum_bonus += row[3]

    lbl_res.config(text=f"Сумма надбавок в високосные года: {sum_bonus}")
    update_history("Выполнен расчет суммы надбавок")


def clear_data():
    matrix.clear()
    table.set_sheet_data([])
    lbl_res.config(text="Сумма надбавок в високосные года: 0")
    update_history("Данные таблицы очищены")


def exit_app():
    """Выход из программы"""
    root.destroy()

root = tk.Tk()
root.title("ПР №8. Вариант 12")
root.geometry("1080x500")

root.iconphoto(False, tk.PhotoImage(width=1, height=1))

frame_in = tk.Frame(root)
frame_in.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

tk.Label(frame_in, text="Введите год:").pack(anchor="w")
ent_year = tk.Entry(frame_in)
ent_year.pack(pady=5)

tk.Label(frame_in, text="Введите надбавку:").pack(anchor="w")
ent_bonus = tk.Entry(frame_in)
ent_bonus.pack(pady=5)

btn_add = tk.Button(frame_in, text="Добавить запись", command=add_record)
btn_add.pack(pady=10, fill=tk.X)

btn_calc = tk.Button(frame_in, text="Расчет и сортировка", command=calculate)
btn_calc.pack(pady=5, fill=tk.X)

btn_clear = tk.Button(frame_in, text="Очистка", command=clear_data)
btn_clear.pack(pady=5, fill=tk.X)

lbl_res = tk.Label(frame_in, text="Сумма надбавок в високосные года: 0", wraplength=150)
lbl_res.pack(pady=15)

btn_about = tk.Button(frame_in, text="О программе", command=show_about)
btn_about.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

btn_exit = tk.Button(frame_in, text="Выход", command=exit_app, )
btn_exit.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

frame_tbl = tk.Frame(root)
frame_tbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=20)

table = tksheet.Sheet(frame_tbl, headers=["Год", "Нераб. дни", "Високосный", "Надбавка"])
table.pack(fill=tk.BOTH, expand=True)
table.set_sheet_data(matrix)

frame_hist = tk.Frame(root)
frame_hist.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

tk.Label(frame_hist, text="История действий:").pack(anchor="w")
txt_hist = tk.Text(frame_hist, width=30, height=20)
txt_hist.pack()

root.mainloop()
