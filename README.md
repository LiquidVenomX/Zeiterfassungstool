# Zeiterfassungstool mit Flask

Dieses Projekt ist ein einfaches Zeiterfassungstool, das mit Flask, einer Web-Framework für Python, erstellt wurde.

## Funktionalitäten
- Benutzeranmeldung und -verwaltung
- Zeiterfassungsfunktionen
- Dashboard-Ansicht für eingeloggte Benutzer

## Anforderungen
- Python (Version 3.x)
- Flask
- Flask-Login
- SQLite3 (für die Benutzerdatenbank)

## Installation

1. Klone das Repository:

   ```bash
   git clone https://github.com/LiquidVenomX/Zeiterfassungstool.git
   cd Zeiterfassungstool
Installiere die erforderlichen Python-Pakete:

bash
Copy code
pip install Flask Flask-Login
Starte die Anwendung:

bash
Copy code
python Zeiterfassung_flask_httpd.py
Die Anwendung sollte unter http://127.0.0.1:5000/ erreichbar sein.

Benutzerdaten
Die Benutzerdaten werden in einer SQLite-Datenbank (user_database.db) gespeichert. Standardmäßig ist ein Benutzer mit den folgenden Anmeldeinformationen vorhanden:

Benutzername: admin
Passwort: 1234
Hinweis: Dieses Projekt ist als Beispiel gedacht und sollte nicht in einer Produktionsumgebung eingesetzt werden, es sei denn, entsprechende Sicherheitsüberlegungen wurden berücksichtigt.

Autor
Thomas Meister

Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen findest du in der Lizenzdatei.
