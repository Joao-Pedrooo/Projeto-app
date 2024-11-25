document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/api/detalhes');
        if (!response.ok) throw new Error('Erro na requisição ao backend');
        const fotos = await response.json();

        if (!fotos || fotos.length === 0) {
            alert('Nenhuma escola encontrada!');
            return;
        }

        const tbody = document.getElementById('test1');
        fotos.forEach((fotos) => {
            const row = document.createElement('p');
            row.innerHTML = `
                <p>${fotos.id}</p>
                <p>${fotos.nome}</p>
                
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


