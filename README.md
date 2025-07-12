# 📺 Videoflix – Dein persönliches Videoportal

Videoflix ist eine minimalistische Video-Streaming-Plattform mit Fokus auf sauberen Code, modernes Design und responsives UI. Nutzer können sich registrieren, Videos entdecken, abspielen und ihren Fortschritt speichern. Das Backend basiert auf Django mit einer klar strukturierten REST-API.

---

## ✨ Features

### 🔐 Authentifizierung
- Registrierung mit E-Mail-Verifizierung
- Login & Logout
- Passwort-Zurücksetzen per E-Mail-Link

### 🎥 Video-Funktionen
- Dashboard mit Hero-Video + Genre-Gruppierung
- Sortierung nach Erstellungsdatum (neueste zuerst)
- Videoplayer mit verschiedenen Auflösungen (120p bis 1080p)
- Fortschrittsspeicherung (optional)

### ⚙️ Backend-Technik
- Django + Django REST Framework
- Redis als Cache + Django RQ für Background Tasks
- PostgreSQL statt SQLite
- REST-API zwischen Frontend und Backend

---

## 🚀 Schnellstart

### Voraussetzungen
- Python >= 3.12
- Docker + Docker Compose

### Lokales Setup mit Docker
```bash
git clone https://github.com/BadPain/Videoflix-Backend.git
cd videoflix
docker compose up --build
```

### Beispiel `.env`
```env
Look at .env.template
```

---

## 🔗 API-Endpunkte (Auszug)

| Methode | Endpoint                     | Beschreibung             |
|--------|------------------------------|--------------------------|
| POST   | /api/register/               | Registrierung            |
| POST   | /api/login/                  | Login                    |
| POST   | /api/logout/                 | Logout                   |
| GET    | /api/videos/                 | Video-Dashboard          |
| GET    | /api/videos/<id>/            | Einzelnes Video          |
| POST   | /api/progress/               | Fortschritt speichern     |

---

## 📂 Projektstruktur (Kurzfassung)

```
videoflix_backend/
├── auth_app/
│   └── api/ (Login, Registrierung)
├── video_app/
│   └── api/ (Video-Endpunkte)
├── utils/ (Hilfsfunktionen)
├── templates/emails/ (E-Mail-Vorlagen)
└── manage.py
```

## ✅ Definition of Done (DoD)
- [x] Clean Code (PEP8, kurze Funktionen, sprechende Namen)
- [x] REST-API mit Django
- [x] Tests vorhanden (>80%)
- [x] Redis + Background Tasks (Django RQ)
- [x] Fortschrittsspeicherung & Videoqualität wählbar

---
