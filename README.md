# D7ucca GitHub API

Projeto em Python para integração com a API REST do GitHub usando GitHub App, autenticação JWT (RS256) e tokens de instalação.

## Funcionalidades

- Autenticação de GitHub Apps.
- Geração de JWT com chave privada RSA.
- Criação de tokens de instalação.
- Listagem dos repositórios acessíveis à aplicação.

## Tecnologias

- Python
- PyJWT
- Requests
- python-dotenv
- GitHub REST API

## Configuração

Copie `.env.example` para `.env` e configure o ID da aplicação e o caminho da chave privada.

Mantenha `.env` e os arquivos `.pem` fora do Git.

## Execução

Instale as dependências:

    pip install -r requirements.txt

Execute:

    python main.py

## Segurança

Nunca publique chaves privadas, tokens ou credenciais reais.
