import hashlib
import os
from database import DatabaseConnection
from models.user import User

class AuthService:
    """Handles cryptographic authentication and database registration processes."""
    
    @staticmethod
    def _generate_salt():
        return os.urandom(16).hex()

    @staticmethod
    def _hash_password(password, salt):
        salted_pass = password + salt
        return hashlib.sha256(salted_pass.encode('utf-8')).hexdigest()

    def register_user(self, username, password):
        if not username or not password:
            return False, "Username and password fields cannot be empty."
        
        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt)

        query = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"
        try:
            with DatabaseConnection() as db:
                db.execute_query(query, (username, hashed_password, salt))
                return True, "User registered successfully!"
        except Exception as e:
            # Check for unique constraint violation
            if "Duplicate entry" in str(e):
                return False, "Registration Failed: Username already exists."
            return False, f"Internal Error: {str(e)}"

    def login_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s"
        try:
            with DatabaseConnection() as db:
                user_record = db.fetch_one(query, (username,))
                
                if not user_record:
                    return None, "Invalid username or password."

                stored_hash = user_record['password_hash']
                salt = user_record['salt']
                computed_hash = self._hash_password(password, salt)

                if computed_hash == stored_hash:
                    user = User(
                        user_id=user_record['id'],
                        username=user_record['username'],
                        password_hash=stored_hash,
                        salt=salt,
                        created_at=user_record['created_at']
                    )
                    return user, "Authentication Successful."
                else:
                    return None, "Invalid username or password."
        except Exception as e:
            return None, f"Database Error during login: {str(e)}"