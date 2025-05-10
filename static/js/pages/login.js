document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault()
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    // Validação simples (apenas para demonstração)
    if (!email || !password) {
        errorMessage.textContent = 'Por favor, preencha todos os campos.';
        errorMessage.style.display = 'block';
        return;
    }
    
    // Simulação login sucedido
    if (email === 'admin' && password === '1234') {
        errorMessage.style.display = 'none';
        successMessage.textContent = 'Cadastro realizado com sucesso! Redirecionando...';
        successMessage.style.display = 'block';
        setTimeout(() => {
        window.location.href = "/";
        }, 1500);
    } else {
        errorMessage.textContent = 'Usuário ou senha incorretos.';
        errorMessage.style.display = 'block';
    }
})