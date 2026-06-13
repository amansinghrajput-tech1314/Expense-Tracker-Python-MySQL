from database import DatabaseConnection
import csv

class IncomeService:
    """Manages all CRUD mutations and analytical operations for Income entities."""
    
    def add_income(self, user_id, amount, source, description, date_str):
        query = "INSERT INTO income (user_id, amount, source, description, date) VALUES (%s, %s, %s, %s, %s)"
        try:
            with DatabaseConnection() as db:
                db.execute_query(query, (user_id, amount, source, description, date_str))
                return True, "Income entry logged successfully."
        except Exception as e:
            return False, f"Failed to record income: {str(e)}"

    def get_all_income(self, user_id):
        query = "SELECT id, amount, source, description, date FROM income WHERE user_id = %s ORDER BY date DESC"
        try:
            with DatabaseConnection() as db:
                return db.fetch_all(query, (user_id,))
        except Exception:
            return []

    def get_total_income(self, user_id):
        query = "SELECT SUM(amount) as total FROM income WHERE user_id = %s"
        try:
            with DatabaseConnection() as db:
                res = db.fetch_one(query, (user_id,))
                return float(res['total']) if res and res['total'] else 0.0
        except Exception:
            return 0.0

    def delete_income(self, user_id, income_id):
        query = "DELETE FROM income WHERE id = %s AND user_id = %s"
        try:
            with DatabaseConnection() as db:
                cursor = db.execute_query(query, (income_id, user_id))
                if cursor.rowcount > 0:
                    return True, "Income record purged successfully."
                return False, "No such record found or access unauthorized."
        except Exception as e:
            return False, str(e)