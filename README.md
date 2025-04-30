# Word Recitation & Notebook Flask App

A personalized vocabulary learning web application built with Flask. Users can sign up, complete a survey to select vocabulary categories (e.g., high school, IELTS), and then learn words, add them to a personal "notebook", and track daily study check‑ins. SMS reminders can be configured via Twilio.

---

## Features

- **User Authentication**: Register, login, logout with Flask‑Login & bcrypt.
- **Onboarding Survey**: New users choose which word lists to study, set a completion timeframe, and opt into SMS reminders.
- **Personalized Homepage**: After survey, users see buttons for each chosen category to begin their vocabulary journey.
- **Vocabulary Pool**: 3 categories (`highschool`, `ielts`, `uni`) loaded from CSV files and paginated for performance.
- **Add to Notebook**: Per‑word button to save to a personal notebook; saved words no longer appear in study lists.
- **My Notebook**: View all saved words in one place.
- **Daily Check‑In**: Mark daily completion with a single click; prevents duplicate check‑ins.
- **Audio Pronunciation**: Fetches phonetic transcriptions via the free Dictionary API.
- **SMS Reminders**: Optional Twilio integration to send daily study reminders.

---

## Requirements

- Python 3.8+
- Flask 3.1
- Flask‑Login
- Flask‑SQLAlchemy
- Flask‑Bcrypt
- python‑dotenv
- requests
- twilio (optional, for real SMS)

See full list in [requirements.txt](requirements.txt).

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd word_recite_app
   ```

2. **Create & activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate.bat   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Rename `.env.example` to `.env` and fill in:
   ```ini
   SECRET_KEY=your_secret_key
   TWILIO_ACCOUNT_SID=...
   TWILIO_AUTH_TOKEN=...
   TWILIO_PHONE_NUMBER=+1xxx
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Import word lists**
   ```bash
   python import_highschool_csv.py
   python import_uni_csv.py
   ```

7. **Run the application**
   ```bash
   python run.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

---

## Directory Structure

```
word_recite_app/
├── app/
│   ├── __init__.py      # Flask app factory, extensions init
│   ├── models.py        # SQLAlchemy models & relationships
│   ├── routes.py        # All application routes and view logic
│   ├── sms.py           # Stub or Twilio SMS sender
│   └── templates/       # Jinja2 HTML templates
│       ├── login.html
│       ├── register.html
│       ├── survey.html
│       ├── index.html
│       ├── word_dictionary.html
│       └── notebook.html
├── highschool_words.csv  # CSV data source
├── uni_words.csv         # CSV data source
├── import_highschool_csv.py
├── import_uni_csv.py
├── init_db.py            # Create tables
├── run.py                # Application entry point
├── requirements.txt
└── README.md
```

---

## Usage

1. **Register** a new account.
2. **Login** and complete the **survey**.
3. Click the category button on the **homepage**.
4. Browse words; click **Add to Notebook** to save and remove from study list.
5. Visit **My Notebook** from the nav to review saved words.
6. Use **Daily Check‑In** to track progress.

---

## Future Improvements

- **Review Mode**: Listen to audio, type translations in an interactive quiz.
- **Search & Filters**: Quickly find specific words.
- **User Profiles**: Track long‑term progress, statistics, streaks.
- **Shared Notebooks**: Export or share word lists with peers.
- **Mobile Responsive Design**: Improve usability on smartphones.

---

## License

MIT © Wanjie Zhang

