# INDICA

Plataforma escolar de recomendações de livros, filmes, séries e músicas, desenvolvida com Python, Flask, MySQL, HTML, CSS e JavaScript.

## 1. Pré-requisitos

- Python 3 instalado
- MySQL Server instalado e em execução
- MySQL Workbench (opcional, para administrar o banco)
- VS Code

## 2. Criar o banco

1. Abra o MySQL Workbench e conecte ao servidor local.
2. Abra o arquivo `banco.sql`.
3. Execute todo o conteúdo (ícone de raio).

## 3. Configurar o Python

No terminal do VS Code, dentro da pasta do projeto:

```bash
python -m venv venv
```

No Windows, ative o ambiente:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 4. Configurar a conexão

1. Faça uma cópia de `.env.example`.
2. Renomeie a cópia para `.env`.
3. Preencha `DB_PASSWORD` com a senha do MySQL.
4. Mantenha `DB_HOST=localhost` se o MySQL estiver instalado no mesmo computador.

Não envie o arquivo `.env` ao GitHub. Ele já está listado no `.gitignore`.

## 5. Executar

```bash
python app.py
```

Abra `http://127.0.0.1:5000` no navegador.

## 6. Publicar no GitHub

Crie um repositório no GitHub. Antes de enviar, confira se o arquivo `.env` não está sendo incluído.

```bash
git init
git add .
git commit -m "Primeira versão do INDICA"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

## Observações

- As senhas dos usuários são armazenadas com hash, não em texto puro.
- O projeto é uma base didática. Antes de publicar para uso real, acrescente proteção CSRF, validação mais completa, limites de tentativas de login e uma chave secreta forte.
- Para o projeto funcionar, o servidor MySQL precisa estar ligado.
