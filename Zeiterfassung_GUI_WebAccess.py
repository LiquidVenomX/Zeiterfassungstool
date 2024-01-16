import tkinter as tk
from tkinter import messagebox
import sqlite3

# Schritt 1: Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('zeit_erfassung.db')
cursor = conn.cursor()

# Schritt 2: Definiere die Hauptfenster-Variable "window"
window = tk.Tk()
window.title('Zeiterfassungstool')

# Schritt 3: Definiere Funktionen für Benutzerverwaltung
def benutzer_anlegen(benutzername, passwort):
    # Funktion zum Hinzufügen eines neuen Benutzers zur Datenbank
    cursor.execute('INSERT INTO benutzer (benutzername, passwort) VALUES (?, ?)', (benutzername, passwort))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Benutzer wurde erfolgreich angelegt!')

def benutzer_loeschen(benutzername):
    # Funktion zum Löschen eines Benutzers aus der Datenbank
    cursor.execute('DELETE FROM benutzer WHERE benutzername = ?', (benutzername,))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Benutzer wurde erfolgreich gelöscht!')

def passwort_aendern(benutzername, neues_passwort):
    # Funktion zum Ändern des Passworts eines Benutzers in der Datenbank
    cursor.execute('UPDATE benutzer SET passwort = ? WHERE benutzername = ?', (neues_passwort, benutzername))
    conn.commit()
    messagebox.showinfo('Erfolg', 'Passwort wurde erfolgreich geändert!')

# Schritt 4: Definiere Funktionen für die GUI
def benutzer_anmelden_gui():
    # Hier kannst du GUI-Elemente für die Benutzeranmeldung hinzufügen
    pass

def zeiterfassung_gui():
    # Hier kannst du GUI-Elemente für die Zeiterfassung hinzufügen
    pass

def admin_console_gui():
    # GUI-Elemente für die Admin-Konsole erstellen
    benutzername_label = tk.Label(window, text='Benutzername:')
    benutzername_entry = tk.Entry(window)
    passwort_label = tk.Label(window, text='Passwort:')
    passwort_entry = tk.Entry(window, show='*')

    def create_user():
        benutzer_anlegen(benutzername_entry.get(), passwort_entry.get())

    def delete_user():
        benutzer_loeschen(benutzername_entry.get())

    def change_password():
        passwort_aendern(benutzername_entry.get(), passwort_entry.get())

    benutzername_label.pack()
    benutzername_entry.pack()
    passwort_label.pack()
    passwort_entry.pack()

    create_button = tk.Button(window, text='Benutzer anlegen', command=create_user)
    create_button.pack()

    delete_button = tk.Button(window, text='Benutzer löschen', command=delete_user)
    delete_button.pack()

    change_password_button = tk.Button(window, text='Passwort ändern', command=change_password)
    change_password_button.pack()

# Schritt 5: Starte die Hauptfenster-Schleife
window.mainloop()
