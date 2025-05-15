import os
import sqlite3
import random
import hashlib
import pickle

# ❌ Hardcoded secret
API_KEY = "sk_test_51ExampleSecretKey"

# ❌ Insecure random token
def generate_token():
    return str(random.randint(100000, 999999))

# ❌ Command injection
def list_files(user_input):
    os.system(f"ls {user_input}")

# ❌ SQL Injection
def get_user(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = '%s'" % username)
    return cursor.fetchall()

# ❌ Path traversal
def read_config(filename):
    with open(f"./configs/{filename}", "r") as f:
        return f.read()

# ❌ Insecure deserialization
def load_data(pickled_data):
    return pickle.loads(pickled_data)

# ❌ Weak cryptography
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == "__main__":
    print("Token:", generate_token())
