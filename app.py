
from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__)


# DASHBOARD
@app.route("/")
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN transaction_type = 'income'
                THEN amount ELSE 0 END), 0) AS income,
            COALESCE(SUM(CASE WHEN transaction_type = 'expense'
                THEN amount ELSE 0 END), 0) AS expenses
        FROM transactions
    """)
    totals = cursor.fetchone()

    cursor.execute("""
        SELECT
            DATE_FORMAT(transaction_date, '%Y-%m') AS month,
            SUM(CASE WHEN transaction_type = 'income'
                THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN transaction_type = 'expense'
                THEN amount ELSE 0 END) AS expenses
        FROM transactions
        GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
        ORDER BY month DESC
    """)
    monthly_data = cursor.fetchall()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """)
    category_data = cursor.fetchall()

    cursor.close()
    db.close()

    income = float(totals["income"])
    expenses = float(totals["expenses"])

    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        balance=income - expenses,
        monthly_data=monthly_data,
        category_data=category_data
    )


# ADD TRANSACTION
@app.route("/add", methods=["POST"])
def add_transaction():
    transaction_type = request.form["transaction_type"]
    amount = request.form["amount"]
    category = request.form["category"].strip()
    description = request.form.get("description", "").strip()
    transaction_date = request.form["transaction_date"]

    if transaction_type not in ("income", "expense"):
        return "Invalid transaction type", 400

    try:
        amount = float(amount)
        if amount <= 0:
            return "Amount must be greater than zero", 400
    except ValueError:
        return "Invalid amount", 400

    if not category or not transaction_date:
        return "Category and date are required", 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (transaction_type, amount, category, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (transaction_type, amount, category, description, transaction_date))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("dashboard"))


# VIEW, SEARCH AND FILTER TRANSACTIONS
@app.route("/transactions")
def transactions():
    search = request.args.get("search", "").strip()
    transaction_type = request.args.get("type", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if search:
        query += " AND (category LIKE %s OR description LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if transaction_type in ("income", "expense"):
        query += " AND transaction_type = %s"
        params.append(transaction_type)

    if start_date:
        query += " AND transaction_date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND transaction_date <= %s"
        params.append(end_date)

    query += " ORDER BY transaction_date DESC, transaction_id DESC"

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    records = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "transactions.html",
        transactions=records,
        search=search,
        selected_type=transaction_type,
        start_date=start_date,
        end_date=end_date
    )


# DELETE TRANSACTION
@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE transaction_id = %s",
        (transaction_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("transactions"))


# EDIT TRANSACTION
@app.route("/edit/<int:transaction_id>", methods=["GET"])
def edit_transaction(transaction_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM transactions WHERE transaction_id = %s",
        (transaction_id,)
    )
    transaction = cursor.fetchone()

    cursor.close()
    db.close()

    if transaction is None:
        return "Transaction not found", 404

    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )


# UPDATE TRANSACTION
@app.route("/update/<int:transaction_id>", methods=["POST"])
def update_transaction(transaction_id):
    transaction_type = request.form["transaction_type"]
    amount = request.form["amount"]
    category = request.form["category"].strip()
    description = request.form.get("description", "").strip()
    transaction_date = request.form["transaction_date"]

    if transaction_type not in ("income", "expense"):
        return "Invalid transaction type", 400

    try:
        amount = float(amount)
        if amount <= 0:
            return "Amount must be greater than zero", 400
    except ValueError:
        return "Invalid amount", 400

    if not category or not transaction_date:
        return "Category and date are required", 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE transactions
        SET transaction_type = %s,
            amount = %s,
            category = %s,
            description = %s,
            transaction_date = %s
        WHERE transaction_id = %s
    """, (
        transaction_type, amount, category, description,
        transaction_date, transaction_id
    ))

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("transactions"))


if __name__ == "__main__":
    app.run(debug=True)
