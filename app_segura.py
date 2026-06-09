import sqlite3
import subprocess
import hashlib
import os
import secrets

# CORRECCIÓN 1: SQL Injection → Usar consultas parametrizadas
def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # ANTES: query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    # AHORA: consulta parametrizada, el driver escapa los valores automáticamente
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    return cursor.fetchone()

# CORRECCIÓN 2: Command Injection → Usar lista de argumentos sin shell=True
def ping_host(host):
    # ANTES: subprocess.call("ping -c 1 " + host, shell=True)
    # AHORA: lista de argumentos, imposible inyectar comandos
    allowed_hosts = ["192.168.58.128", "192.168.58.129", "192.168.58.131"]
    if host not in allowed_hosts:
        raise ValueError("Host no permitido")
    result = subprocess.call(["ping", "-c", "1", host], shell=False)
    return result

# CORRECCIÓN 3: Credenciales hardcodeadas → Usar variables de entorno
# ANTES: DB_PASSWORD = "admin123" / API_KEY = "sk-1234567890abcdef"
# AHORA: leer de variables de entorno, nunca en el código fuente
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY = os.environ.get("API_KEY")
if not DB_PASSWORD or not API_KEY:
    raise EnvironmentError("Variables de entorno DB_PASSWORD y API_KEY requeridas")

# CORRECCIÓN 4: Hash MD5 inseguro → Usar bcrypt/SHA-256 con salt
def hash_password(password):
    # ANTES: hashlib.md5(password.encode()).hexdigest()
    # AHORA: SHA-256 con salt aleatorio
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"

# CORRECCIÓN 5: Path traversal → Validar y sanitizar el path
def read_file(filename):
    # ANTES: open("/var/www/" + filename)
    # AHORA: verificar que el path no sale del directorio permitido
    base_dir = "/var/www/public/"
    safe_path = os.path.realpath(os.path.join(base_dir, filename))
    if not safe_path.startswith(base_dir):
        raise ValueError("Acceso denegado: path traversal detectado")
    with open(safe_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    print(login("admin", "admin"))
    print(hash_password("password123"))
