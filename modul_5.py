import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

users = {
    'guardianskk': {'password': 'password123', 'secret': 'meow'},
    'defendservice': {'password': 'password321', 'secret': 'woof'}
}

class SecurityApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Стражник - Вход')
        self.root.geometry('700x700')
        self.root.resizable(False, False)

        self.current_user = None
        self.user_role = None
        self.photo_path = None

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text='Вход в систему', font=('Arial', 14)).pack(pady=20)

        fields = [('Тип пользователя', 'combobox', ['Администратор доступа', 'Сотрудник службы безопасности']), ('Логин', 'entry', None), ('Пароль', 'entry', '*'), ('Секретное слово', 'entry', '*')]

        self.entries = {}

        for text, field_type, param in fields:
            tk.Label(self.root, text=text).pack(pady=(10, 0))

            if field_type == 'entry':
                entry = tk.Entry(self.root, show=param)
                entry.pack(pady=5, padx=50, fill='x')
                self.entries[text] = entry
            else:
                combo = ttk.Combobox(self.root, values=param)
                combo.pack(pady=5, padx=50, fill='x')
                self.entries[text] = combo

        tk.Button(self.root, text='Войти', command=self.login).pack(pady=20)

    def login(self):
        role = self.entries['Тип пользователя'].get()
        username = self.entries['Логин'].get()
        password = self.entries['Пароль'].get()
        secret = self.entries['Секретное слово'].get()

        if not all([role, username, password, secret]):
            messagebox.showerror('Ошибка', 'Все поля должны быть заполнены!')
            return

        if len(password) < 8:
            messagebox.showerror('Ошибка', 'Пароль должен содержать не менее 8 символов')
            return

        if username in users:
            user = users[username]
            if user['password'] == password and user['secret'] == secret:
                self.current_user = username
                self.user_role = role
                messagebox.showinfo('Победа', f'Добро пожаловать {username}')
                self.show_control_panel()
                return

        messagebox.showerror('Ошибка', 'Неверные учетные данные')

    def show_control_panel(self):
        self.clear_screen()

        tk.Label(self.root, text=f'Панель управления ({self.user_role})', font=('Arial', 14)).pack(pady=20)

        fields = ['Фамилия', 'Имя', 'Отчество', 'Должность']
        self.data_entries = {}

        for field in fields:
            tk.Label(self.root, text=field).pack(pady=(10, 0))
            entry = tk.Entry(self.root)
            entry.pack(pady=5, padx=50, fill='x')
            self.data_entries[field] = entry

        tk.Label(self.root, text='Пол').pack(pady=(10, 0))
        self.gender_var = tk.StringVar()
        tk.Radiobutton(self.root, text='Мужской', variable=self.gender_var, value='Мужской').pack()
        tk.Radiobutton(self.root, text='Женский', variable=self.gender_var, value='Женский').pack()

        tk.Label(self.root, text='Фотография (3x4)').pack(pady=(20, 5))

        self.photo_label = tk.Label(self.root, text='Фото не загружено', width=30, height=10, relief='solid')
        self.photo_label.pack()

        tk.Button(self.root, text='Выбрать фото', command=self.load_photo).pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text='Сохранить', command=self.save_data).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text='Очистить', command=self.show_control_panel).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text='Выйти', command=self.show_login_screen).grid(row=0, column=2, padx=10)

    def load_photo(self):
        filepath = filedialog.askopenfilename(title='Выберите фотографию', filetypes=[('Изображения', '*.jpg *.png')])

        if not filepath:
            return

        file_size = os.path.getsize(filepath) / (1024 * 1024)
        if file_size > 2:
            messagebox.showerror('Ошибка', 'Файл слишком большой (макс. 2 МБ)')
            return

        try:
            img = Image.open(filepath)
            width, height = img.size
            ratio = width / height

            if abs(ratio - 0.75) > 0.05:
                messagebox.showerror('Ошибка', 'Изображение должно быть размером 3x4')
                return

            img.thumbnail((150, 200))
            photo = ImageTk.PhotoImage(img)

            self.photo_label.config(image=photo, text='')
            self.photo_label.image = photo
            self.photo_path = filepath

        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось загрузить изображение: {e}')

    def save_data(self):
        surname = self.data_entries['Фамилия'].get().strip()
        name = self.data_entries['Имя'].get().strip()
        patronymic = self.data_entries['Отчество'].get().strip()
        position = self.data_entries['Должность'].get().strip()
        gender = self.gender_var.get()

        if not all([surname, name, patronymic, position, gender]):
            messagebox.showerror('Ошибка', 'Все поля должны быть заполнены!')
            return

        if not self.photo_path:
            messagebox.showerror('Ошибка', 'Необходимо загрузить фотографию!')
            return

        filename = f'{surname}_{name}_{patronymic}.txt'

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'Фамилия: {surname}\n')
                f.write(f'Имя: {name}\n')
                f.write(f'Отчество: {patronymic}\n')
                f.write(f'Должность: {position}\n')
                f.write(f'Пол: {gender}\n')
                f.write(f'Фото: {self.photo_path}\n')

            messagebox.showinfo('Победа', 'Данные успешно сохранены!')
            self.show_control_panel()

        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось сохранить данные: {e}')


if __name__ == '__main__':
    app = SecurityApp()
    app.root.mainloop()
