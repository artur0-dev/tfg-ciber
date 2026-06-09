import sqlite3
import subprocess
import hashlib
import os

# VULNERABILIDAD 1: SQL Injection
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)
    return cursor.fetchone()

# VULNERABILIDAD 2: Command Injection
def ping_host(host):
    result = subprocess.call("ping -c 1 " + host, shell=True)
    return result

# VULNERABILIDAD 3: Contraseña hardcodeada
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# VULNERABILIDAD 4: Hash MD5 inseguro
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILIDAD 5: Path traversal
def read_file(filename):
    with open("/var/www/" + filename, "r") as f:
        return f.read()

if __name__ == "__main__":
    print(login("admin", "admin"))
    print(ping_host("8.8.8.8"))
    print(hash_password("password123"))
