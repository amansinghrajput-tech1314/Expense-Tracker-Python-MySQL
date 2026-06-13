from database import DatabaseConnection
import csv

class ExpenseService:
    """Manages analytical evaluations, CSV aggregation, and transactional lifecycle for Expenses."""
    
    def add_expense(self, user_id, amount, category, description, date_str):
        query = "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (%s, %s, %s, %s, %s)"
        try:
            with DatabaseConnection() as db:
                db.execute_query(query, (user_id, amount, category, description, date_str))
                return True, "Expense record added successfully."
        except Exception as e:
            return False, f"Failed to record expense: {str(e)}"

    def get_all_expenses(self, user_id):
        query = "SELECT id, amount, category, description, date FROM expenses WHERE user_id = %s ORDER BY date DESC"
        try:
            with DatabaseConnection() as db:
                return db.fetch_all(query, (user_id,))
        except Exception:
            return []

    def get_total_expense(self, user_id):
        query = "SELECT SUM(amount) as total FROM expenses WHERE user_id = %s"
        try:
            with DatabaseConnection() as db:
                res = db.fetch_one(query, (user_id,))
                return float(res['total']) if res and res['total'] else 0.0
        except Exception:
            return 0.0

    def update_expense(self, user_id, expense_id, amount, category, description, date_str):
        query = """UPDATE expenses 
                   SET amount = %s, category = %s, description = %s, date = %s 
                   WHERE id = %s AND user_id = %s"""
        try:
            with DatabaseConnection() as db:
                cursor = db.execute_query(query, (amount, category, description, date_str, expense_id, user_id))
                if cursor.rowcount > 0:
                    return True, "Expense record updated successfully."
                return False, "Record updated or modification rejected."
        except Exception as e:
            return False, str(e)

    def delete_expense(self, user_id, expense_id):
        query = "DELETE FROM expenses WHERE id = %s AND user_id = %s"
        try:
            with DatabaseConnection() as db:
                cursor = db.execute_query(query, (expense_id, user_id))
                if cursor.rowcount > 0:
                    return True, "Expense track destroyed."
                return False, "Record targeted for deletion could not be discovered."
        except Exception as e:
            return False, str(e)

    def get_category_analytics(self, user_id):
        query = """SELECT category, SUM(amount) as total 
                   FROM expenses WHERE user_id = %s 
                   GROUP BY category ORDER BY total DESC"""
        try:
            with DatabaseConnection() as db:
                return db.fetch_all(query, (user_id,))
        except Exception:
            return []

    def get_monthly_summary(self, user_id):
        query = """SELECT DATE_FORMAT(date, '%Y-%m') as month, SUM(amount) as total 
                   FROM expenses WHERE user_id = %s 
                   GROUP BY month ORDER BY month DESC"""
        try:
            with DatabaseConnection() as db:
                return db.fetch_all(query, (user_id,))
        except Exception:
            return []

    def search_transactions(self, user_id, keyword):
        query = """SELECT 'Expense' as type, id, amount, category as metric, description, date 
                   FROM expenses WHERE user_id = %s AND (description LIKE %s OR category LIKE %s)
                   UNION 
                   SELECT 'Income' as type, id, amount, source as metric, description, date 
                   FROM income WHERE user_id = %s AND (description LIKE %s OR source LIKE %s)
                   ORDER BY date DESC"""
        like_term = f"%{keyword}%"
        try:
            with DatabaseConnection() as db:
                return db.fetch_all(query, (user_id, like_term, like_term, user_id, like_term, like_term))
        except Exception:
            return []

    def export_to_csv(self, user_id, filename="financial_export.csv"):
        try:
            expenses = self.get_all_expenses(user_id)
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Transaction ID', 'Type', 'Amount', 'Category/Source', 'Description', 'Date'])
                for exp in expenses:
                    writer.writerow([exp['id'], 'Expense', exp['amount'], exp['category'], exp['description'], exp['date']])
            return True, f"Dataset flushed securely to filesystem at {filename}"
        except Exception as e:
            return False, f"File export failure encountered: {str(e)}"