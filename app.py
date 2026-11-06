import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from conexao import conectar

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "troque-esta-chave-em-producao")


def login_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar essa página.", "aviso")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def inicio():
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.categoria, r.descricao, r.avaliacao,
               u.nome AS autor
        FROM recomendacoes r
        LEFT JOIN usuarios u ON r.usuario_id = u.id
        ORDER BY r.id DESC
        LIMIT 6
    """)
    recomendacoes = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template("index.html", recomendacoes=recomendacoes)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return render_template("cadastro.html")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "erro")
            return render_template("cadastro.html")

        banco = conectar()
        cursor = banco.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, generate_password_hash(senha))
            )
            banco.commit()
            flash("Conta criada! Agora você pode entrar.", "sucesso")
            return redirect(url_for("login"))
        except Exception:
            banco.rollback()
            flash("Não foi possível criar a conta. Esse e-mail pode já estar cadastrado.", "erro")
        finally:
            cursor.close()
            banco.close()

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        banco = conectar()
        cursor = banco.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        banco.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            flash("Login realizado com sucesso!", "sucesso")
            return redirect(url_for("inicio"))

        flash("E-mail ou senha incorretos.", "erro")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/recomendacoes")
def listar_recomendacoes():
    categoria = request.args.get("categoria", "").strip()
    busca = request.args.get("busca", "").strip()

    banco = conectar()
    cursor = banco.cursor(dictionary=True)

    sql = """
        SELECT r.id, r.titulo, r.categoria, r.descricao, r.avaliacao,
               u.nome AS autor
        FROM recomendacoes r
        LEFT JOIN usuarios u ON r.usuario_id = u.id
        WHERE 1=1
    """
    parametros = []

    if categoria in ["Livro", "Filme", "Série", "Música"]:
        sql += " AND r.categoria = %s"
        parametros.append(categoria)

    if busca:
        sql += " AND (r.titulo LIKE %s OR r.descricao LIKE %s)"
        termo = f"%{busca}%"
        parametros.extend([termo, termo])

    sql += " ORDER BY r.id DESC"
    cursor.execute(sql, parametros)
    recomendacoes = cursor.fetchall()

    cursor.close()
    banco.close()
    return render_template(
        "recomendacoes.html",
        recomendacoes=recomendacoes,
        categoria_atual=categoria,
        busca_atual=busca
    )


@app.route("/adicionar", methods=["GET", "POST"])
@login_obrigatorio
def adicionar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        categoria = request.form.get("categoria", "")
        descricao = request.form.get("descricao", "").strip()
        avaliacao = request.form.get("avaliacao", "5")

        if not titulo or categoria not in ["Livro", "Filme", "Série", "Música"]:
            flash("Informe um título e uma categoria válida.", "erro")
            return render_template("adicionar.html")

        try:
            avaliacao = float(avaliacao)
            if not 1 <= avaliacao <= 5:
                raise ValueError
        except ValueError:
            flash("A avaliação deve ser um número entre 1 e 5.", "erro")
            return render_template("adicionar.html")

        banco = conectar()
        cursor = banco.cursor()
        cursor.execute("""
            INSERT INTO recomendacoes (titulo, categoria, descricao, avaliacao, usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, categoria, descricao, avaliacao, session["usuario_id"]))
        banco.commit()
        cursor.close()
        banco.close()

        flash("Recomendação publicada!", "sucesso")
        return redirect(url_for("listar_recomendacoes"))

    return render_template("adicionar.html")


@app.route("/favoritos")
@login_obrigatorio
def favoritos():
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.titulo, r.categoria, r.descricao, r.avaliacao,
               u.nome AS autor
        FROM favoritos f
        JOIN recomendacoes r ON r.id = f.recomendacao_id
        LEFT JOIN usuarios u ON u.id = r.usuario_id
        WHERE f.usuario_id = %s
        ORDER BY f.id DESC
    """, (session["usuario_id"],))
    lista = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template("favoritos.html", recomendacoes=lista)


@app.route("/favoritar/<int:recomendacao_id>", methods=["POST"])
@login_obrigatorio
def favoritar(recomendacao_id):
    banco = conectar()
    cursor = banco.cursor()
    cursor.execute(
        "INSERT IGNORE INTO favoritos (usuario_id, recomendacao_id) VALUES (%s, %s)",
        (session["usuario_id"], recomendacao_id)
    )
    banco.commit()
    cursor.close()
    banco.close()
    flash("Recomendação adicionada aos favoritos.", "sucesso")
    return redirect(request.referrer or url_for("listar_recomendacoes"))


@app.route("/desfavoritar/<int:recomendacao_id>", methods=["POST"])
@login_obrigatorio
def desfavoritar(recomendacao_id):
    banco = conectar()
    cursor = banco.cursor()
    cursor.execute(
        "DELETE FROM favoritos WHERE usuario_id = %s AND recomendacao_id = %s",
        (session["usuario_id"], recomendacao_id)
    )
    banco.commit()
    cursor.close()
    banco.close()
    flash("Recomendação removida dos favoritos.", "sucesso")
    return redirect(request.referrer or url_for("favoritos"))


if __name__ == "__main__":
    app.run(debug=True)
