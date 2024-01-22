
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

def create_user():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', generate_password_hash('1234')))
    conn.commit()
    conn.close()

def create_user_times_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_times
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    start_time DATETIME,
                    end_time DATETIME)''')
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect('user_database.db')

create_user_times_table()

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
            return redirect(url_for('dashboard'))
        else:
            print("Falscher Benutzername oder Passwort!")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_times = get_user_times(current_user.id)
    total_hours = 0

    for start_time_str, end_time_str in user_times:
        # Konvertiere die Zeit-Strings in datetime-Objekte
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

        # Hier die Logik zur Berechnung der Differenz und Summe der Stunden
        timedelta = end_time - start_time
        total_hours += timedelta.total_seconds() / 3600

    # Benutzerdefiniertes Soll-Pensum (kann an deine Anforderungen angepasst werden)
    default_pensum_hours = 40  # Standardwert: 40 Stunden pro Woche

    # Überprüfe, ob der Benutzer ein Soll-Pensum ausgewählt hat
    selected_pensum_hours = request.args.get('pensum_hours')
    if selected_pensum_hours:
        try:
            pensum_hours = float(selected_pensum_hours)
        except ValueError:
            pensum_hours = default_pensum_hours
    else:
        pensum_hours = default_pensum_hours

    # Berechne das erreichte Pensum in Prozent
    achieved_percent = (total_hours / pensum_hours) * 100 if pensum_hours > 0 else 0

    return render_template('dashboard.html', user_times=user_times, total_hours=total_hours,
                           pensum_hours=pensum_hours, achieved_percent=achieved_percent)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_time', methods=['POST'])
@login_required
def add_time():
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        add_user_time(current_user.id, start_time, end_time)
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

def add_user_time(user_id, start_time, end_time):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_times (user_id, start_time, end_time) VALUES (?, ?, ?)', (user_id, start_time, end_time))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)