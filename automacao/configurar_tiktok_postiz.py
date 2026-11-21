import os
import re
import subprocess
import sys

POSTIZ_DIR = r"C:\Users\guibson.krause\Documents\ChatGPT\Postiz"
COMPOSE_FILE = os.path.join(POSTIZ_DIR, "docker-compose.yaml")

print("=" * 50)
print("   Configurador TikTok OAuth - Postiz")
print("=" * 50)

if not os.path.exists(COMPOSE_FILE):
    print(f"Erro: Arquivo {COMPOSE_FILE} nao encontrado.")
    sys.exit(1)

client_key = input("Cole o Client key do TikTok: ").strip()
client_secret = input("Cole o Client secret do TikTok: ").strip()

if not client_key or not client_secret:
    print("Erro: Client key ou Client secret nao podem ser vazios.")
    sys.exit(1)

with open(COMPOSE_FILE, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(
    r"(?m)^\s*TIKTOK_CLIENT_ID:\s*.*$",
    f"      TIKTOK_CLIENT_ID: '{client_key}'",
    content
)

content = re.sub(
    r"(?m)^\s*TIKTOK_CLIENT_SECRET:\s*.*$",
    f"      TIKTOK_CLIENT_SECRET: '{client_secret}'",
    content
)

with open(COMPOSE_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("\ndocker-compose.yaml atualizado com sucesso!")
print("Reiniciando o conteiner postiz...")

try:
    subprocess.run(["docker", "compose", "up", "-d", "postiz"], cwd=POSTIZ_DIR, check=True)
    print("\n[SUCESSO] Postiz atualizado e reiniciado com o TikTok configurado!")
    print("Acesse http://localhost:4007 e conecte sua conta do TikTok.")
except Exception as e:
    print(f"Erro ao reiniciar docker: {e}")
