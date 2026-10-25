
import os
import time
from pathlib import Path

import jwt
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.github.com"
APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10"
}



def gerar_jwt():
    if not APP_ID or not PRIVATE_KEY_PATH:
        raise ValueError("Configure as variáveis no arquivo .env")

    chave = Path(PRIVATE_KEY_PATH).read_text(
        encoding="utf-8"
    )

    agora = int(time.time())

    payload = {
        "iat": agora - 60,
        "exp": agora + 480,
        "iss": APP_ID
    }

    return jwt.encode(
        payload,
        chave,
        algorithm="RS256"
    )




def consultar_api(metodo, endpoint, token):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"

    resposta = requests.request(
        metodo,
        BASE_URL + endpoint,
        headers=headers,
        timeout=20
    )

    print(f"Endpoint: {endpoint}")
    print(f"Status HTTP: {resposta.status_code}")

    if not resposta.ok:
        try:
            erro = resposta.json()
            print("Mensagem GitHub:", erro.get("message"))
        except ValueError:
            print("A API retornou uma resposta não JSON.")

    resposta.raise_for_status()

    return resposta.json()



def main():
    print("Iniciando d7ucca-github-api...")

    token_jwt = gerar_jwt()

    app = consultar_api("GET", "/app", token_jwt)

    print(f"Aplicação: {app['name']}")
    print("Autenticação realizada com sucesso!")

    instalacoes = consultar_api(
        "GET",
        "/app/installations",
        token_jwt
    )

    if not instalacoes:
        print("Instale a GitHub App na sua conta primeiro.")
        return

    for instalacao in instalacoes:
        installation_id = instalacao["id"]

        dados = consultar_api(
            "POST",
            f"/app/installations/{installation_id}/access_tokens",
            token_jwt
        )

        token_instalacao = dados["token"]

        repositorios = consultar_api(
            "GET",
            "/installation/repositories?per_page=100",
            token_instalacao
        )

        print("\nRepositórios encontrados:")

        for repo in repositorios["repositories"]:
            print(f"\nNome: {repo['full_name']}")
            print(f"Privado: {repo['private']}")
            print(f"URL: {repo['html_url']}")

    print("\nIntegração concluída!")


if __name__ == "__main__":
    try:
        main()
    except (
        requests.RequestException,
        ValueError,
        OSError,
        jwt.PyJWTError
    ) as erro:
        print(f"Erro na integração: {erro}")
