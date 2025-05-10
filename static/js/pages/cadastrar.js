document.getElementById('cadastroForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nome = document.getElementById('nome').value;
    const sobrenome = document.getElementById('sobrenome').value;
    const email = document.getElementById('email').value;
    const razaoSocial = document.getElementById('razao-social').value;
    const cnpj = document.getElementById('cnpj-empresa').value;
    const endereco = document.getElementById('endereco-empresa').value;
    const senha = document.getElementById('senha').value;
    const confirmarSenha = document.getElementById('confirmarSenha').value;
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    
    // Reiniciar mensagens
    errorMessage.style.display = 'none';
    successMessage.style.display = 'none';
        
    // Validações 
    // TODO: Validar o restante dos campos
    if (senha !== confirmarSenha) {
    errorMessage.textContent = 'As senhas não coincidem.';
    errorMessage.style.display = 'block';
    return;
    }
        
    if (!document.getElementById('termos').checked) {
    errorMessage.textContent = 'Você deve aceitar os Termos de Serviço.';
    errorMessage.style.display = 'block';
    return;
    }

    // TODO: Mandar informações do cadastro para o back
        
    successMessage.textContent = 'Cadastro realizado com sucesso! Redirecionando...';
    successMessage.style.display = 'block';

    setTimeout(() => {
    window.location.href = "/login";
    }, 1500);
});