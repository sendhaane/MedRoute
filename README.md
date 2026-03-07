# 💊 MedRoute — Medicine Search & Navigation

MedRoute is a location-aware web app that helps users find medicines at nearby pharmacies in Puducherry, India. Search for any medicine — whether for humans or pets — and instantly see which pharmacies have it in stock, complete with an interactive map and turn-by-turn navigation.

![MedRoute Screenshot](https://img.shields.io/badge/Status-Live-brightgreen) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey)

---

## ✨ Features

- **🔍 Medicine Search** — Search by medicine name with real-time results from verified pharmacy stock
- **🧑 Human & 🐾 Pet Medicines** — Toggle between human and veterinary pharmacy categories
- **🗺️ Interactive Map** — Leaflet-powered map showing pharmacy locations with custom markers
- **🧭 Turn-by-Turn Navigation** — Get driving directions from your location to any pharmacy
- **📋 Browse All Medicines** — View the full medicine catalogue with availability counts
- **📱 Responsive Design** — Works seamlessly on desktop and mobile devices

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **Database** | SQLite |
| **Frontend** | HTML, CSS, JavaScript |
| **Maps** | Leaflet.js, Leaflet Routing Machine |
| **Fonts** | Google Fonts (Inter) |
| **Deployment** | Render |

---

## 📁 Project Structure

```
Medical/
├── app.py                  # Flask application (routes & API)
├── setup_db.py             # Database schema & seed data
├── database.db             # SQLite database (auto-generated)
├── requirements.txt        # Python dependencies
├── build.sh                # Render build script
├── render.yaml             # Render deployment blueprint
├── templates/
│   └── index.html          # Main page template
└── static/
    ├── css/
    │   └── style.css       # Application styles
    └── js/
        └── map.js          # Map, search & navigation logic
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/medroute.git
cd medroute

# Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize the database with seed data
python setup_db.py

# Start the development server
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🌐 Deployment (Render)

This project is pre-configured for one-click deployment on [Render](https://render.com):

1. Push the code to a GitHub repository
2. Go to **Render Dashboard → New + → Blueprint**
3. Select your repo — Render auto-detects `render.yaml`
4. Click **Apply** and your app will be live!

> **Note:** The free tier uses an ephemeral filesystem, so the SQLite database is re-seeded on each deploy via `build.sh`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main page |
| `GET` | `/search?medicine=<name>&category=<human\|pet>` | Search pharmacies stocking a medicine |
| `GET` | `/medicines?category=<human\|pet>` | List all medicines with pharmacy counts |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
