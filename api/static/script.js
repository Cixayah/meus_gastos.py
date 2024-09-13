document.addEventListener('DOMContentLoaded', function () {
    const expenseForm = document.getElementById('expenseForm');
    const emailForm = document.getElementById('emailForm');

    if (expenseForm) {
        expenseForm.addEventListener('submit', function (event) {
            const descriptionField = document.getElementById('description');
            const amountField = document.getElementById('amount');
            const description = descriptionField.value.trim();
            const amount = parseFloat(amountField.value);

            if (description.length > 100) {
                event.preventDefault();
                alert('A descrição deve ter no máximo 100 caracteres.');
                return;
            }

            if (isNaN(amount) || amount <= 0) {
                event.preventDefault();
                alert('O valor do gasto deve ser maior que 0.');
                return;
            }

            // Formata o valor para duas casas decimais
            amountField.value = amount.toFixed(2);
        });
    }

    if (emailForm) {
        emailForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Previne o envio padrão do formulário

            const formData = new FormData(this);
            try {
                const response = await fetch(emailForm.action, { // Garante que a URL gerada está correta
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    alert('Email enviado! Verifique sua caixa de spam se necessário.');
                    this.reset(); // Opcional: Limpa o formulário
                } else {
                    alert('Erro ao enviar o email. Tente novamente mais tarde.');
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro ao enviar o email. Tente novamente mais tarde.');
            }
        });
    }
});
