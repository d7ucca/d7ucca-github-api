
import jwt
from dotenv import load_dotenv
from pathlib import Path
import os
import time

load_dotenv()

chave = Path(
    os.getenv("GITHUB_PRIVATE_KEY_PATH")
).read_text(encoding="utf-8")

agora = int(time.time())

payload = {
    "iat": agora - 60,
    "exp": agora + 540,
    "iss": os.getenv("GITHUB_APP_ID")
}

try:
    token = jwt.encode(
        payload,
        chave,
        algorithm="RS256"
    )

    print("JWT gerado com sucesso!")
    print("Versão PyJWT:", jwt.__version__)

except Exception as erro:
    print("Erro:", type(erro).__name__)
    print("Detalhes:", erro)
