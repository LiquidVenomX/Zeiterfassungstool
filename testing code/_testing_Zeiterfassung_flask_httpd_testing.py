import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimeschluessel'
login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    print("Loaded user:", user_data)
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

def create_user():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', generate_password_hash('1234')))
    conn.commit()
    conn.close()

@app.route('/add_time', methods=['POST'])
@login_required
def add_time():
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        # Hier fügst du die Logik hinzu, um die Zeiterfassung in die Datenbank einzufügen

        print(f"Zeiterfassung hinzugefügt: {start_time} - {end_time}")
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html')

def get_user_times(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT start_time, end_time FROM user_times WHERE user_id = ?', (user_id,))
    times = cursor.fetchall()
    conn.close()
    return times

@app.route('/dashboard')
@login_required
def show_dashboard():
    user_times = get_user_times(current_user.id)

    total_hours = 0
    for start_time, end_time in user_times:
        # Hier die Logik zur Berechnung der Differenz und Summe der Stunden
        # Beispiel: timedelta = end_time - start_time
        # total_hours += timedelta.total_seconds() / 3600

        return render_template('dashboard.html', user_times=user_times, total_hours=total_hours)

def connect_db():
    return sqlite3.connect('user_database.db')

conn = connect_db()
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)''')
conn.commit()
conn.close()

conn = connect_db()
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
existing_user = cursor.fetchone()
conn.close()

if not existing_user:
    create_user()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            print(f"Benutzer {username} erfolgreich angemeldet!")
            return redirect(url_for('show_dashboard'))
        else:
            print("Falscher Benutzername oder Passwort!")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
