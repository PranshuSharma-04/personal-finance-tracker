# Personal Finance & Expense Tracker

A web-based personal finance management application built using Python, Flask, and MySQL. It helps users track income and expenses, manage transactions, and understand their spending through financial summaries and visual analytics.

## Features

- **Dashboard:** View total income, expenses, and available balance.
- **Transaction Management:** Add, edit, and delete income and expense records.
- **Transaction History:** View all financial transactions.
- **Search & Filtering:** Filter transactions by category, type, and date range.
- **Financial Analytics:** Visualize monthly income and expenses.
- **Category-wise Analysis:** Understand spending across different categories.
- **Database Integration:** Store transaction records persistently using MySQL.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| HTML | Page structure |
| CSS | User interface and styling |
| JavaScript | Interactive charts |
| Chart.js | Financial data visualization |

## Project Structure

```text
personal-finance-tracker/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── dashboard.html
    ├── transactions.html
    └── edit_transaction.html
```

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/PranshuSharma-04/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MySQL

Create the database:

```sql
CREATE DATABASE finance_tracker;
USE finance_tracker;
```

Create the transactions table:

```sql
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_type ENUM('income', 'expense') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=finance_tracker
```

Replace the credentials with your local MySQL configuration.

### 6. Run the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

## Future Improvements

- User authentication and account management
- Budget planning and expense limits
- Export financial reports
- Improved financial insights

## Author

**Pranshu Sharma**

B.Tech Computer Science Engineering

GitHub: [PranshuSharma-04](https://github.com/PranshuSharma-04)
