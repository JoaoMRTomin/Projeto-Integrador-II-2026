// 1. Função global para o Google Sign-In (deve ficar fora do DOMContentLoaded)
function manipularRespostaGoogle(response) {
    console.log("Token do Google recebido:", response.credential);
    // Futuramente, envie este token para autenticar no backend
}

document.addEventListener('DOMContentLoaded', () => {
    // Captura dos formulários e links de troca
    const formLogin = document.querySelector('#form-login');
    const formCadastro = document.querySelector('#form-cadastro');
    const linkIrCadastro = document.querySelector('#linkIrCadastro');
    const linkIrLogin = document.querySelector('#linkIrLogin');

    // 2. Alternar entre formulários de Login e Cadastro
    if (linkIrCadastro && linkIrLogin) {
        linkIrCadastro.addEventListener('click', (e) => {
            e.preventDefault();
            formLogin.classList.add('hidden');
            formCadastro.classList.remove('hidden');
        });

        linkIrLogin.addEventListener('click', (e) => {
            e.preventDefault();
            formCadastro.classList.add('hidden');
            formLogin.classList.remove('hidden');
        });
    }

    // 3. Envio do formulário de CADASTRO
    if (formCadastro) {
       formCadastro.addEventListener('submit', async (e) => {
    e.preventDefault();

    const elNome = document.querySelector('#cad-nome');
    const elEmail = document.querySelector('#cad-email');
    const elSenha = document.querySelector('#cad-senha');

    // Validação de segurança para garantir que os elementos existem no DOM
    if (!elNome || !elEmail || !elSenha) {
        console.error('Erro: Um ou mais IDs (#cad-nome, #cad-email, #cad-senha) não foram encontrados no HTML.');
        alert('Erro interno: Campos do formulário não encontrados.');
        return;
    }

    const nome = elNome.value;
    const email = elEmail.value;
    const senha = elSenha.value;

    try {
        const response = await fetch('http://127.0.0.1:3000/api/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.message || 'Erro ao realizar cadastro.');
            return;
        }

        alert('Conta criada com sucesso!');
        localStorage.setItem('usuarioLogado', JSON.stringify(data.usuario));
        window.location.href = 'dashboard.html';

    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Não foi possível conectar ao servidor backend.');
    }
});
    }

    // 4. Envio do formulário de LOGIN
    if (formLogin) {
        formLogin.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.querySelector('#login-email').value;
            const senha = document.querySelector('#login-senha').value;

            try {
                const response = await fetch('http://127.0.0.1:3000/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, senha })
                });

                const data = await response.json();

                if (!response.ok) {
                    alert(data.message || 'E-mail ou senha incorretos.');
                    return;
                }

                localStorage.setItem('usuarioLogado', JSON.stringify(data.usuario));
                window.location.href = 'dashboard.html';

            } catch (error) {
                console.error('Erro no login:', error);
                alert('Não foi possível conectar ao servidor.');
            }
        });
    }
});