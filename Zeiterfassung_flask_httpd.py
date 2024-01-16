from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimeschluessel'
login_manager = LoginManager(app)

# Benutzerklasse für Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# Login-Manager-Konfiguration
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

# Routen für Flask-Webanwendung
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('user_database.db')
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
    return f'Dashboard für Benutzer: {current_user.username}'

if __name__ == "__main__":
    app.run(debug=True)
