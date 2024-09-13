import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv(
    "SECRET_KEY", "chave_secreta_fallback"
)  # Defina uma chave secreta para as sessões


class ExpenseManager:
    @staticmethod
    def add_expense(description, amount):
        if "expenses" not in session:
            session["expenses"] = []
        session["expenses"].append({"description": description, "amount": amount})
        session.modified = True  # Garante que a sessão seja atualizada

    @staticmethod
    def show_expenses():
        return session.get("expenses", [])

    @staticmethod
    def calculate_total():
        return sum(expense["amount"] for expense in session.get("expenses", []))

    @staticmethod
    def delete_expense(index):
        """Remove o gasto pelo índice."""
        if "expenses" in session and 0 <= index < len(session["expenses"]):
            session["expenses"].pop(index)
            session.modified = True  # Atualiza a sessão após a remoção


# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        ExpenseManager.add_expense(description, amount)
        return redirect(url_for("index"))

    expenses = ExpenseManager.show_expenses()
    total = ExpenseManager.calculate_total()
    return render_template("index.html", expenses=expenses, total=total)


# Remover gasto
@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    ExpenseManager.delete_expense(index)
    return redirect(url_for("index"))


# Enviar relatório por e-mail
@app.route("/send_email", methods=["POST"])
def email():
    to_email = request.form["to_email"]

    expenses = ExpenseManager.show_expenses()
    total = ExpenseManager.calculate_total()
    expenses_text = "\n".join(
        [f"{expense['description']}: R${expense['amount']:.2f}" for expense in expenses]
    )
    body = f"Olá,\n\nRelatório de gastos:\n\n{expenses_text}\nTotal: R${total:.2f}\n\nValeu,\nCix 👾"

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    from_email = login
    subject = "Relatório de Gastos"

    send_email(
        subject, body, to_email, from_email, smtp_server, smtp_port, login, password
    )

    return redirect(url_for("index"))


def send_email(
    subject, body, to_email, from_email, smtp_server, smtp_port, login, password
):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Conexão com o servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Identificação com o servidor SMTP
            server.starttls()  # Inicia a conexão segura
            server.ehlo()  # Necessário após o starttls()
            server.login(login, password)  # Autenticação
            server.send_message(msg)
            print("Email enviado com sucesso!")
    except smtplib.SMTPException as e:
        print(f"Falha ao enviar o email: {e}")


# Executa o app
if __name__ == "__main__":
    app.run(debug=True)
