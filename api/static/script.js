document.addEventListener('DOMContentLoaded', function () {
    const emailForm = document.getElementById('emailForm');

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