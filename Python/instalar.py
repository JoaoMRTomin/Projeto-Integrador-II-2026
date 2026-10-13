import subprocess
import sys

print("Iniciando a instalação das bibliotecas...")

# Adicionamos a flag de permissão para o Python gerenciado pelo uv
subprocess.check_call([
    sys.executable, "-m", "pip", "install",
    "--break-system-packages",
    "flask", "flask-cors", "mysql-connector-python"
])

print("\n--- TUDO INSTALADO COM SUCESSO! ---")