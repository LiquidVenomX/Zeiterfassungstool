from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, sqlite3

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

@app.route('/')
def index():
    return 'Willkommen!'

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Willkommen im Dashboard, {current_user.username}!'

if __name__ == "__main__":
    app.run(debug=True)
