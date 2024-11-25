document.addEventListener('DOMContentLoaded', () => {
    const role = localStorage.getItem('role');

    // Exibir/ocultar abas com base no tipo de usuário
    if (role === 'admin') {
        document.getElementById('admin-link').style.display = 'inline-block';
        document.getElementById('coleta-link').style.display = 'inline-block';
    } else if (role === 'user') {
        document.getElementById('admin-link').style.display = 'none';
        document.getElementById('coleta-link').style.display = 'none';
    } else {
        // Redirecionar para login se não autenticado
        window.location.href = 'login.html';
    }
});
