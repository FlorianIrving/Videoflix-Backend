# 🎬 VIDEOFLIX – Dein persönliches Streaming-Backend

✨ **Modulares Django REST Backend** für eine Streaming-Plattform mit Fokus auf Performance, Sicherheit & Clean Code.

---

## 🚀 Features

- ✅ **Registrierung & Login** mit E-Mail-Aktivierung
- 🔐 **JWT-Auth** via `SimpleJWT` + Token Refresh
- 📧 **E-Mail-Versand** für Account-Aktivierung & Passwort-Reset
- 🛠️ **REST API** für Frontend-Kommunikation (Videos, Auth, Progress)
- 🎥 **Video-Upload & Anzeige** inkl. Thumbnails
- 🔁 **Fortschritts-Speicherung** mit Resume-Funktion
- 🧪 **Tests mit Pytest** (inkl. Coverage-Messung)
- 🧹 **PEP-8 & Clean Code** – geprüft & umgesetzt

---

## 🧰 Tech-Stack

| Bereich       | Technologie                    |
|---------------|--------------------------------|
| Backend       | Django + DRF                   |
| Auth          | JWT via `SimpleJWT`            |
| E-Mail        | Django-Mail (SMTP)             |
| Testing       | `pytest`, `coverage.py`        |
| Datenbank     | PostgreSQL (SQLite optional)   |
| Caching       | Redis (empfohlen)              |
| Background    | Django RQ (für Video-Tasks)    |

---

## 🧑‍💻 Setup (lokal)

```bash
# Backend Setup
git clone https://github.com/DEIN_GITHUB_USERNAME/videoflix_backend.git
cd videoflix_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Erstelle `.env` Datei (bspw.):
```env
SECRET_KEY=dein_secret
DEBUG=True
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=videoflix@example.com
EMAIL_HOST_PASSWORD=dein_passwort
DEFAULT_FROM_EMAIL=videoflix@example.com
```

```bash
# Datenbank migrieren
python manage.py migrate

# Superuser erstellen
python manage.py createsuperuser

# Server starten
python manage.py runserver
```

---

## 🧪 Tests ausführen

```bash
pytest --cov=.
```

- Ziel: **80%+ Test Coverage**
- Tool: `coverage.py`

---

## 📂 Projektstruktur (Kurzform)

```
videoflix_backend/
│
├── auth_app/              # Registrierung, Login, Tokens, Activation
├── video_app/             # Video Model, Upload, Darstellung
├── progress_app/          # Fortschrittsspeicherung (optional)
│
├── core/                  # Globale Einstellungen, URLs, WSGI
├── media/                 # Video-/Thumbnail-Dateien
├── templates/             # Mail Templates
├── manage.py
└── requirements.txt
```

---

## 📬 API Overview (Auszug)

### 🔑 Auth

| Endpoint                      | Methode       | Beschreibung                        |
|-------------------------------|---------------|-------------------------------------|
| `/api/register/`              | POST          | Registrieren + Mailversand          |
| `/api/login/`                 | POST          | JWT Login                           |
| `/api/logout/`                | POST          | JWT Logout                          |
| `/api/activate/<uid>/<token>/`| GET           | Aktivierungslink                    |
| `/api/password-reset/`        | POST          | Mail zum Zurücksetzen               |
| `/api/password-reset-confirm/<uid>/<token>/`  | POST | Neues Passwort               |

---

### 🎥 Video

| Endpoint                 | Methode | Beschreibung         |
|-------------------------|---------|----------------------|
| `/api/videos/`          | GET     | Liste aller Videos   |
| `/api/videos/<id>/`     | GET     | Einzelnes Video (Stream + Info) |

---

## 📚 Dokumentation

- Siehe [📁 `docs/`](./docs/) Verzeichnis (wird bei Abgabe ergänzt)
- Enthält Diagramme, Abläufe, API-Docs, Testfälle

---