import tkinter as tk
from tkinter import ttk
import sqlite3
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimeschluessel'
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

class UserManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Benutzerverwaltung")

        self.label_username = ttk.Label(root, text="Benutzername:")
        self.label_password = ttk.Label(root, text="Passwort:")

        self.entry_username = ttk.Entry(root)
        self.entry_password = ttk.Entry(root, show="*")

        self.button_create_user = ttk.Button(root, text="Benutzer erstellen", command=self.create_user)
        self.button_login = ttk.Button(root, text="Login", command=self.login)

        self.label_username.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.label_password.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        self.button_create_user.grid(row=2, column=0, pady=10, padx=5)
        self.button_login.grid(row=2, column=1, pady=10, padx=5)

    def create_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        print(f"Benutzer {username} erstellt!")

    def login(self):
        with app.app_context():
            username = self.entry_username.get()
            password = self.entry_password.get()

            conn = sqlite3.connect('user_database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user_data = cursor.fetchone()
            conn.close()

            if user_data:
                user = User(user_data[0], user_data[1], user_data[2])
                login_user(user)
                print(f"Benutzer {username} erfolgreich angemeldet!")
            else:
                print("Falscher Benutzername oder Passwort!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementGUI(root)
    root.mainloop()
