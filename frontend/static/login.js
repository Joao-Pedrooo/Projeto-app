document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simulação de autenticação
    if (username === 'admin' && password === 'admin') {
        localStorage.setItem('role', 'admin');
        window.location.href = 'index.html';
    } else if (username === 'user' && password === 'user') {
        localStorage.setItem('role', 'user');
        window.location.href = 'index.html';
    } else {
        document.getElementById('error-message').textContent =
            'Usuário ou senha inválidos.';
    }
});
