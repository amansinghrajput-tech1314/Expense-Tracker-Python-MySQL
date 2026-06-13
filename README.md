# Expense-Tracker-Python-MySQL

An enterprise-grade, clean-architecture personal finance tracking application built using Python and MySQL. This system leverages Domain-Driven Design (DDD) principles, robust validation layers, and cryptographic security to deliver a high-performance terminal dashboard for modern asset management.

---

##  Architectural Overview
The system is engineered with a strict **Separation of Concerns (SoC)**, ensuring horizontal scalability and easy testability:
- **Presentation Layer (`main.py`):** Resilient console terminal driving structured menu-driven execution loops.
- **Service Layer (`services/`):** Stateless core business logic engines supervising computational data analytics and operations.
- **Domain Entity Layer (`models/`):** Strongly encapsulated Python data objects mapping core structural relational tables.
- **Data Access Layer (`database.py`):** Resource-safe Python context managers executing parameterized, injection-safe database actions.

---

##  Key Technical Capabilities
- **Cryptographic Security:** Passwords are fully hashed using industry-standard **SHA-256 with unique dynamic cryptographic salts** per user.
- **Multi-Entity Unified Search:** A single high-performance `UNION` scan querying across multiple dynamic transaction tables simultaneously.
- **Advanced Financial Analytics:** Real-time computational processing for category cost distributions, month-over-month trajectories, and net current balances.
- **Automated Data Archiving:** Secure native pipeline flushing relational ledger histories into structured, flat-file CSV formats for external accounting.
- **Fault-Tolerant Sanitization Engine:** Upfront formatting blockages discarding empty buffers, negative valuations, and malformed dates before database transmission.

---

##  Tech Stack & Dependencies
- **Core Engine:** Python 3.10+
- **Database Engine:** MySQL 8.0+ / MariaDB (XAMPP Environment compliant)
- **External Framework Libraries:** `mysql-connector-python`, `tabulate`

---

## 📂 Project Directory Architecture
```text
Expense-Tracker-Python-MySQL/
│
├── config.py                 # Configuration states & credential bindings
├── database.py               # Resource-safe context-driven database handlers
├── main.py                   # Dynamic presentation dashboard router
├── requirements.txt          # Third-party module dependencies
├── .gitignore                # Source control exclusions
├── README.md                 # Technical portfolio blueprint
│
├── models/                   # Strongly encapsulated entity frameworks
│   ├── __init__.py
│   ├── user.py
│   ├── income.py
│   └── expense.py
│
├── services/                 # Decoupled business logic modules
│   ├── __init__.py
│   ├── auth_service.py
│   ├── income_service.py
│   └── expense_service.py
│
└── sql/                      # Relational schema optimization scripts
    └── expense_tracker.sql