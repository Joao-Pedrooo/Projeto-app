document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/api/escolas');
        if (!response.ok) throw new Error('Erro na requisição ao backend');
        const escolas = await response.json();

        if (!escolas || escolas.length === 0) {
            alert('Nenhuma escola encontrada!');
            return;
        }

        const tbody = document.getElementById('escola-list');
        escolas.forEach((escola) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${escola.id}</td>
                <td>${escola.nome}</td>
                <td>${escola.endereco}</td>
                <td><button onclick="viewDetails(${escola.id})">Detalhes</button></td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error('Erro ao carregar as escolas:', err);
        alert(
            'Ocorreu um erro ao carregar as escolas. Tente novamente mais tarde.'
        );
    }
});

function viewDetails(id) {
    localStorage.setItem('currentescola', id);
    window.location.href = 'detalhes.html';
}
