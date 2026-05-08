import tkinter as tk
from tkinter import ttk
import random
import json
import os


def load_tasks():
    """Загружает список задач из файла или возвращает предустановленные"""
    default_tasks = [
        {"task": "Прочитать статью", "type": "учёба"},
        {"task": "Сделать зарядку", "type": "спорт"},
        {"task": "Написать отчёт", "type": "работа"},
        {"task": "Подготовить презентацию", "type": "работа"},
        {"task": "Повторить лекцию", "type": "учёба"},
        {"task": "Пробежать 5 км", "type": "спорт"},
        {"task": "Изучить новую тему", "type": "учёба"},
        {"task": "Посетить тренировку", "type": "спорт"},
        {"task": "Составить план проекта", "type": "работа"}
    ]
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_tasks
    return default_tasks


def save_tasks(tasks):
    """Сохраняет список задач в файл"""
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def load_history():
    """Загружает историю из файла"""
    if os.path.exists('history.json'):
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_history(history):
    """Сохраняет историю в файл"""
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def create_app():
    """Создает и запускает приложение"""
    root = tk.Tk()
    root.title("Random Task Generator")
    root.geometry("500x600")

    # Загружаем данные
    tasks = load_tasks()
    history = load_history()

    # Создаем виджеты
    input_frame = ttk.LabelFrame(root, text="Добавить новую задачу")
    input_frame.pack(pady=10, padx=10, fill='x')

    ttk.Label(input_frame, text="Текст задачи:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    task_entry = ttk.Entry(input_frame, width=40)
    task_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
    input_frame.columnconfigure(1, weight=1)

    ttk.Label(input_frame, text="Тип задачи:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    type_combobox = ttk.Combobox(
        input_frame,
        values=["учёба", "спорт", "работа"],
        state="readonly",
        width=15
    )
    type_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    type_combobox.current(0)

    add_task_btn = ttk.Button(
        input_frame,
        text="Добавить задачу"
    )
    add_task_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # Статус для операций с задачами
    status_label = ttk.Label(
        input_frame,
        text="",
        font=("Arial", 9),
        wraplength=450
    )
    status_label.grid(row=3, column=0, columnspan=2, pady=5)

    generate_btn = ttk.Button(
        root,
        text="Сгенерировать случайную задачу"
    )
    generate_btn.pack(pady=10, padx=10, fill='x')

    # Статус для генерации задачи
    task_status_label = ttk.Label(
        root,
        text="",
        font=("Arial", 9, "italic"),
        wraplength=450,
        foreground="blue"
    )
    task_status_label.pack(pady=5, padx=10, fill='x')

    filter_frame = ttk.LabelFrame(root, text="Фильтр по типу")
    filter_frame.pack(pady=10, padx=10, fill='x')

    ttk.Label(filter_frame, text="Показать задачи типа:").pack(side='left', padx=5)
    filter_combobox = ttk.Combobox(
        filter_frame,
        values=["Все", "учёба", "спорт", "работа"],
        state="readonly",
        width=15
    )
    filter_combobox.pack(side='left', padx=5)
    filter_combobox.current(0)

    reset_btn = ttk.Button(
        filter_frame,
        text="Сбросить"
    )
    reset_btn.pack(side='right', padx=5)

    history_frame = ttk.LabelFrame(root, text="История задач")
    history_frame.pack(pady=10, padx=10, fill='both', expand=True)

    history_listbox = tk.Listbox(
        history_frame,
        width=50,
        height=12,
        font=("Arial", 10)
    )
    history_listbox.pack(pady=5, padx=5, fill='both', expand=True)

    scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=history_listbox.yview)
    scrollbar.pack(side='right', fill='y')
    history_listbox.config(yscrollcommand=scrollbar.set)

    # Функции приложения
    def clear_status():
        """Очищает статусные метки через 3 секунды"""
        status_label.config(text="")
        task_status_label.config(text="")

    def show_status(message, is_error=False, is_task_status=False):
        """Отображает статусное сообщение"""
        if is_task_status:
            task_status_label.config(
                text=message,
                foreground="red" if is_error else "blue"
            )
        else:
            status_label.config(
                text=message,
                foreground="red" if is_error else "green"
            )

        # Очищаем статус через 3 секунды
        root.after(3000, clear_status)

    def update_history_listbox():
        """Обновляет отображение истории"""
        history_listbox.delete(0, tk.END)
        # Отображаем задачи в порядке от новых к старым
        for i, item in enumerate(reversed(history), 1):
            history_listbox.insert(
                0,
                f"{i}. {item['task']} | Тип: {item['type']}"
            )

    def add_task():
        """Добавляет новую задачу в список"""
        task_text = task_entry.get().strip()
        task_type = type_combobox.get()

        if not task_text:
            show_status("Ошибка: Текст задачи не может быть пустым!", is_error=True)
            return

        # Добавляем в общий список задач
        tasks.append({"task": task_text, "type": task_type})
        task_entry.delete(0, tk.END)
        show_status("Задача успешно добавлена в список!", is_error=False)

        # Явно обновляем интерфейс
        root.update_idletasks()

    def generate_task():
        """Генерирует случайную задачу и добавляет в историю"""
        if not tasks:
            show_status("Список задач пуст! Добавьте хотя бы одну задачу.", is_error=True, is_task_status=True)
            return

        selected_task = random.choice(tasks)
        history.append(selected_task)

        # Обновляем историю и интерфейс
        update_history_listbox()
        history_listbox.see(tk.END)

        # Добавлено: принудительное обновление интерфейса
        history_listbox.update_idletasks()

        show_status(
            f"Сгенерировано: {selected_task['task']} | Тип: {selected_task['type']}",
            is_error=False,
            is_task_status=True
        )

    def filter_history(event=None):
        """Фильтрует историю по выбранному типу"""
        selected_filter = filter_combobox.get()

        filtered = []
        if selected_filter != "Все":
            filtered = [item for item in history if item['type'] == selected_filter]
        else:
            filtered = history.copy()

        history_listbox.delete(0, tk.END)
        for i, item in enumerate(reversed(filtered), 1):
            history_listbox.insert(
                0,
                f"{i}. {item['task']} | Тип: {item['type']}"
            )

    def reset_filter():
        """Сбрасывает фильтр"""
        filter_combobox.current(0)
        update_history_listbox()

    def on_closing():
        """Действия при закрытии окна"""
        save_tasks(tasks)
        save_history(history)
        root.destroy()

    # Привязываем функции к виджетам
    add_task_btn.config(command=add_task)
    generate_btn.config(command=generate_task)
    filter_combobox.bind("<<ComboboxSelected>>", filter_history)
    reset_btn.config(command=reset_filter)

    # Инициализация
    update_history_listbox()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    create_app()