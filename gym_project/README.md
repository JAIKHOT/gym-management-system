# 🏋️ Gym Management System

**A Hybrid Database Application using MySQL and MongoDB with Flask**

![Status](https://img.shields.io/badge/status-complete-success)
![Course](https://img.shields.io/badge/course-DBMS-blue)
![Semester](https://img.shields.io/badge/semester-V-orange)

Aligned with **SDG 3** (Good Health and Well-Being), **SDG 8** (Decent Work and Economic Growth), and **SDG 9** (Industry, Innovation and Infrastructure).

---

## 👥 Team

| Role | Name | PRN |
|---|---|---|
| Group Leader | Jai Khot | 1262240490 |
| Member | Arya Borgaonkar | 126225285 |

**Guide:** Dr. Vibha Patel  
**Course:** Database Management Systems (DBMS)  
**Program:** T.Y. B.Tech (ECE - AI/ML)  
**Semester:** V, AY 2026-27  
**University:** MIT World Peace University, Pune

---

## 🎯 Project Overview

A full-stack web application for managing gym operations, built with a **hybrid database architecture**. The system demonstrates **polyglot persistence** by combining:

- **MySQL** — for structured, transactional data with referential integrity
- **MongoDB** — for semi-structured, nested, and evolving data

### Core Features

- ✅ Member registration and management
- ✅ Membership plans (Monthly / Quarterly / Half-Yearly / Yearly / Annual Plus)
- ✅ Trainer assignment and specialization tracking
- ✅ Payment recording with automatic audit logging
- ✅ Attendance tracking with time-consistency checks
- ✅ Personalized workout plans with nested day-wise exercises
- ✅ Goal-based exercise presets with AJAX auto-fill
- ✅ Member feedback with real-time average rating
- ✅ Live dashboard aggregating data from both databases
- ✅ Admin panel with stored procedure runner and audit log

---

## 🏗️ Architecture

Three-tier client-server architecture:

```
┌─────────────────────────┐
│   USER / Browser        │
│   HTML + CSS + Bootstrap│
└────────────┬────────────┘
             │ HTTP
┌────────────▼────────────┐
│   Flask Backend         │
│   Python 3 + app.py     │
└─────┬───────────────┬───┘
      │               │
  PyMySQL         PyMongo
      │               │
┌─────▼──────┐   ┌────▼─────┐
│   MySQL    │   │ MongoDB  │
│ Relational │   │ Document │
└────────────┘   └──────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, JavaScript |
| **Backend** | Python 3.11, Flask 3.x, Jinja2 |
| **Relational DB** | MySQL 8.0 |
| **Document DB** | MongoDB 7.x |
| **MySQL Driver** | `mysql-connector-python` |
| **MongoDB Driver** | `pymongo` |

---

## 📊 Database Design

### MySQL Tables (6)

| Table | Purpose |
|---|---|
| `plans` | Membership plans with duration and price |
| `trainers` | Trainer contact and specialization |
| `members` | Member registration, plan, and trainer assignment |
| `payments` | Payment records with mode (Cash/UPI/Card) |
| `attendance` | Check-in / check-out timestamps |
| `audit_log` | Auto-populated audit trail |

### MySQL Additional Objects

- **View:** `member_details` — encapsulates 3-table JOIN
- **Stored Procedures:** `monthly_revenue`, `expire_memberships`, `top_members`
- **Triggers:** `payment_after_insert`, `member_after_delete`
- **Indexes:** 7 performance indexes
- **Constraint:** `CHECK (check_out > check_in)` on attendance

### MongoDB Collections (3)

| Collection | Purpose |
|---|---|
| `workout_plans` | Nested day → exercises structure |
| `feedback` | Flat documents with ratings and comments |
| `presets` | Goal-based exercise templates |

- **Indexes:** `idx_preset_goal`, `feedback.date`, `workout_plans.created_at`

---

## 🎓 DBMS Concepts Demonstrated

- ✅ Entity-Relationship modeling
- ✅ Normalization (UNF → 1NF → 2NF → 3NF)
- ✅ Primary, foreign, unique, check constraints
- ✅ ENUM types for restricted values
- ✅ CASCADE and SET NULL foreign key behaviors
- ✅ Stored procedures with IN parameters and ROW_COUNT
- ✅ Triggers with OLD / NEW references for auditing
- ✅ Views for JOIN encapsulation
- ✅ Indexes for query optimization (O(n) → O(log n))
- ✅ MongoDB aggregation pipeline (`$group`, `$avg`, `$sum`)
- ✅ Nested documents with array structures
- ✅ Polyglot persistence design decisions

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or newer
- MySQL 8.0 (via MySQL Workbench recommended)
- MongoDB 7.x (via MongoDB Compass recommended)
- VS Code (recommended)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/gym-management-system.git
cd gym-management-system
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set Up MySQL

1. Open **MySQL Workbench**
2. Connect to your local MySQL server
3. Create a new SQL tab
4. Paste the entire contents of `gym_db_setup.sql`
5. Run it (Ctrl + Shift + Enter)

This creates the `gym_db` database with 6 tables, indexes, view, 3 procedures, 2 triggers, and sample data (10 members, 5 plans, 5 trainers, 14 payments, 20 attendance entries).

### Step 4 — Set Up MongoDB

1. Open **MongoDB Shell** or **MongoDB Compass**
2. Paste the entire contents of `mongodb_setup.js`
3. Run it

This creates the `gym_db` database with 3 collections and sample data (10 workout plans, 10 feedback entries, 5 presets).

### Step 5 — Configure MySQL Password

Open `app.py` and update the password in the `get_mysql()` function:

```python
def get_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # <-- change this
        database="gym_db"
    )
```

### Step 6 — Run the Application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure

```
gym_project/
├── app.py                    # Flask backend (~450 lines)
├── gym_db_setup.sql          # MySQL setup script
├── mongodb_setup.js          # MongoDB setup script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git exclusion rules
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Layout + navbar + flash messages
│   ├── dashboard.html        # Live hybrid stats
│   ├── index.html            # Members page
│   ├── plans.html            # Plans page
│   ├── trainers.html         # Trainers page
│   ├── payments.html         # Payments page
│   ├── workouts.html         # Workout plans (MongoDB)
│   ├── feedback.html         # Feedback page (MongoDB)
│   ├── presets.html          # Preset admin (MongoDB)
│   └── admin.html            # Audit log + procedure runner
└── static/                   # Static assets (optional)
```

---

## 🌐 Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Dashboard with hybrid stats |
| `/members` | GET | List members |
| `/add_member` | POST | Insert member |
| `/delete_member/<id>` | GET | Delete member (CASCADE) |
| `/plans` | GET | List plans |
| `/add_plan` | POST | Insert plan |
| `/delete_plan/<id>` | GET | Delete plan (SET NULL) |
| `/trainers` | GET | List trainers |
| `/add_trainer` | POST | Insert trainer |
| `/delete_trainer/<id>` | GET | Delete trainer (SET NULL) |
| `/payments` | GET | List payments |
| `/add_payment` | POST | Record payment |
| `/workouts` | GET | List workout plans |
| `/add_workout` | POST | Assign workout |
| `/feedback` | GET | List feedback |
| `/add_feedback` | POST | Submit feedback |
| `/presets` | GET | List presets |
| `/add_preset` | POST | Insert preset |
| `/delete_preset/<id>` | GET | Delete preset |
| `/get_presets/<goal>` | GET | JSON API for preset lookup |
| `/admin` | GET | Audit log + procedure runner |
| `/run_expire` | GET | Call `expire_memberships()` |
| `/revenue/<month>` | GET | Call `monthly_revenue()` |

---

## 📸 Application Screenshots

The application provides:

- **Dashboard** — 5 stats from MySQL, 2 from MongoDB, aggregated in a single view
- **Members** — 10 members with plans, trainers, and delete option
- **Plans** — 5 membership tiers with prices
- **Trainers** — 5 trainers with specializations
- **Payments** — 14 payment records with mode tracking
- **Workouts** — 10 workout cards with nested day-wise exercises
- **Feedback** — 10 reviews with live average rating (4.5/5)
- **Presets** — 5 goal-based exercise templates
- **Admin** — audit log and one-click procedure runner

---

## 🧪 Testing

The project includes **18 manual test cases** covering:

- CRUD operations across all entities
- Trigger firing verification
- Stored procedure invocation
- CASCADE and SET NULL behavior
- MongoDB aggregation correctness
- Form validation and error handling
- SQL injection prevention (parameterized queries)
- Duplicate constraint handling

Full test case table is available in the project report.

---

## 📚 References

1. M. Fowler, "Polyglot Persistence," martinfowler.com, 2011.
2. A. Silberschatz, H. F. Korth, and S. Sudarshan, *Database System Concepts*, 7th ed. McGraw-Hill, 2019.
3. R. Elmasri and S. B. Navathe, *Fundamentals of Database Systems*, 7th ed. Pearson, 2016.
4. Z. Du, J. Zhang, and C. Yang, "Design and Implementation of an Intelligent Gym Management System Based on openGauss and Spring Boot," in *Proc. 2025 IEEE ICEACE*, 2025.
5. Oracle Corporation, "MySQL 8.0 Reference Manual." [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/
6. MongoDB Inc., "MongoDB Manual." [Online]. Available: https://www.mongodb.com/docs/manual/
7. Pallets Projects, "Flask Documentation." [Online]. Available: https://flask.palletsprojects.com/
8. K. Chodorow, *MongoDB: The Definitive Guide*, 3rd ed. O'Reilly Media, 2013.

---

## 📄 License

This project is submitted as part of the T.Y. B.Tech DBMS PBL course at MIT-WPU Pune.  
For academic use only.

---

## 🙏 Acknowledgment

We sincerely thank **Dr. Vibha Patel** for her continuous guidance and valuable feedback throughout this project. We also thank **MIT World Peace University, Pune** for providing the resources and academic environment that made this work possible.

---

**Built with ❤️ at MIT-WPU Pune | Semester V | 2026-27**