# CampusShare 🎓

A college-exclusive marketplace where students **rent, borrow, sell, donate, and exchange** academic and campus-life essentials — uniforms, books, notes, lab coats, calculators, electronics, stationery, hostel essentials and sports equipment.

Built with **Flask + Bootstrap 5** and a clean, explainable **content-based AI recommender**.

---

## Project Overview

Every semester students buy items — uniforms, lab coats, calculators, textbooks — that get used briefly and then sit unused. CampusShare lets a college's own students trade these directly with each other: rent instead of buying, sell what you don't need, donate what's still useful, or exchange items outright. See [`docs/project-overview.md`](docs/project-overview.md) for the full write-up.

## Features

**Students can:** register (college email only) · login/logout · edit profile · create/edit/delete listings · browse, search, and filter items · request to rent/buy/receive-donation/exchange · accept/reject requests as an owner · track a full rental pickup→return lifecycle · favorite items · leave & receive 1–5 star reviews · get in-app notifications · report problematic listings.

**Admins can:** view a stats dashboard with Chart.js charts · block/unblock students · remove inappropriate listings · manage categories · resolve or reject reports.

**AI/ML:** an independent `ml/` module implementing a TF-IDF + cosine-similarity content-based item recommender (see [`docs/ai-ml.md`](docs/ai-ml.md)).

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF |
| Frontend | HTML5, Bootstrap 5, Bootstrap Icons, vanilla JS, Chart.js |
| Database | MySQL (via PyMySQL) — **falls back to SQLite automatically** if no `DATABASE_URL` is configured, so the app runs with zero database setup |
| Auth/Security | Werkzeug password hashing, Flask-Login sessions, CSRF protection |
| AI/ML | pandas, NumPy, scikit-learn (TF-IDF + cosine similarity) |
| Testing | pytest |

## Project Structure

```text
CampusShare/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/               # SQLAlchemy models
│   ├── routes/                # Flask blueprints
│   ├── templates/             # Jinja2 templates (Bootstrap 5)
│   ├── static/                 # CSS / JS
│   └── utils/                  # Forms, decorators, upload helpers
├── ml/                        # Independent AI/ML recommendation module
│   ├── data/                   # Exported item snapshots
│   ├── models/                 # Pickled trained recommender
│   ├── preprocessing.py
│   ├── train.py
│   ├── predict.py
│   └── recommender.py
├── uploads/items/             # Uploaded item images
├── instance/                  # SQLite DB (auto-created)
├── tests/                     # pytest test suite (32 tests)
├── docs/                      # Architecture, DB design, API docs, ai-ml.md ...
├── seed.py                    # Demo data seeding script
├── run.py                     # App entry point
├── config.py                  # Environment-based configuration
├── requirements.txt
├── .env.example
├── .gitignore
├── database.sql               # MySQL database/user creation script
└── README.md
```

## Requirements

- Python 3.12+
- pip
- (Optional) MySQL 8+ if you want to use MySQL instead of the default SQLite fallback

## Installation

```bash
git clone <repository-url>
cd CampusShare
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
# then edit .env — at minimum set a real SECRET_KEY
```

By default `DATABASE_URL` is left unset, so the app automatically uses a
local SQLite database at `instance/campusshare.db` — **no database setup
required to get started.**

### (Optional) Using MySQL instead of SQLite

```bash
mysql -u root -p < database.sql
```

Then set in `.env`:
```env
DATABASE_URL=mysql+pymysql://campusshare_user:change_this_password@localhost/campusshare
```

### Run the application

```bash
python run.py
```

Open your browser at:

```text
http://127.0.0.1:5000
```

### Load demo data

```bash
python seed.py
```

This creates 1 admin account, 5 sample students, 10 categories, and 15
sample listings. **These are development/demo credentials only — change
them before any real deployment.**

### Run tests

```bash
pytest tests/ -v
```

All 32 tests should pass (see [`docs/testing.md`](docs/testing.md)).

### Train / try the AI/ML recommender (optional, independent of the web app)

```bash
python ml/train.py
python ml/predict.py --item-id 2 --top-n 5
python ml/predict.py --user-favorites 2,5,9 --top-n 6
```

## Demo Credentials

Run `python seed.py` to create development-only demo accounts. Do not use demo accounts or passwords in production.

## Important Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Flask session/CSRF signing key | dev key — **must** be changed for production |
| `DATABASE_URL` | SQLAlchemy connection string | unset → SQLite fallback |
| `COLLEGE_EMAIL_DOMAIN` | Only emails ending in `@<this>` can register | `mycollege.edu` |

Never commit a real `.env` file, secret keys, or database passwords to
source control — `.gitignore` already excludes `.env`.

## Implemented Features (checklist)

- [x] Registration/login/logout with hashed passwords & college-domain restriction
- [x] Role-based access control (Student / Admin)
- [x] Item CRUD with listing-type-specific validation
- [x] Image upload with extension/size validation
- [x] Browse, search, multi-field filters, sorting, pagination
- [x] Full RENT lifecycle (request → accept → pickup → return)
- [x] SELL / DONATE / EXCHANGE request→accept flows
- [x] Favorites (with duplicate prevention)
- [x] Reviews & average rating calculation (with duplicate prevention)
- [x] Database-backed notifications with unread count & mark-as-read
- [x] Reporting system with admin resolution workflow
- [x] Admin dashboard with Chart.js charts (category/type/monthly activity)
- [x] Category management (add/delete, delete blocked if in use)
- [x] Friendly 400/403/404/500 error pages
- [x] CSRF protection on all state-changing forms
- [x] Light/dark mode toggle
- [x] pytest test suite (32 tests, all passing)
- [x] Independent content-based AI recommendation module

## AI/ML Features Implemented

- **Content-based item recommender** using TF-IDF + cosine similarity
  (see [`docs/ai-ml.md`](docs/ai-ml.md) for full dataset/preprocessing/
  algorithm/evaluation write-up). Not wired into the live UI yet by
  design (kept independent per the project brief) — CLI-runnable and
  ready for integration.

## Limitations & things that could not be fully tested

- **MySQL** was not available in the build/test environment used to
  create this project, so the MySQL connection path (PyMySQL) could not
  be live-tested end-to-end — only code-reviewed. SQLite (the default)
  and an in-memory SQLite (via pytest) were both fully tested. The same
  SQLAlchemy ORM code path is used regardless of backend, so MySQL is
  expected to behave identically; please smoke-test after switching.
- **WebSocket/real-time notifications** were intentionally not
  implemented, per the project brief (notifications are database-backed
  and refresh on page load).
- **Online payments** were intentionally not implemented — all
  transactions are coordinated offline between students.
- The AI/ML recommender is not yet wired into the live UI (see
  `docs/ai-ml.md` §8 for the exact integration points for a future
  iteration).

## License

Built as an academic / portfolio project. Free to use and adapt for
learning purposes.
