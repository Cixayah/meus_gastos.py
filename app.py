import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)


class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, description, amount):
        self.expenses.append({"description": description, "amount": amount})

    def show_expenses(self):
        return self.expenses

    def calculate_total(self):
        return sum(expense["amount"] for expense in self.expenses)

    def delete_expense(self, index):
        """Remove o gasto pelo índice."""
        if 0 <= index < len(self.expenses):
            del self.expenses[index]


# Gerenciando gastos
manager = ExpenseManager()


# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form["description"]
        amount = float(request.form["amount"])
        manager.add_expense(description, amount)
        return redirect(url_for("index"))

    expenses = manager.show_expenses()
    total = manager.calculate_total()
    return render_template("index.html", expenses=expenses, total=total)


# Remover gasto
@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    manager.delete_expense(index)
    return redirect(url_for("index"))


# Enviar relatório por e-mail
@app.route("/send_email", methods=["POST"])
def email():
    to_email = request.form["to_email"]

    expenses = manager.show_expenses()
    total = manager.calculate_total()
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
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login, password)
            server.send_message(msg)
            print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar o email: {e}")


# Executa o app
if __name__ == "__main__":
    app.run(debug=True)
