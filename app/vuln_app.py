import os
import sqlite3
import random
import hashlib
import pickle

# ❌ Command injection
def list_files(user_input):
    os.system(f"ls {user_input}")

# ❌ SQL Injection
def get_user(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = '%s'" % username)
    return cursor.fetchall()

# ❌ Weak cryptography
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == "__main__":
    print("Token:", generate_token())
