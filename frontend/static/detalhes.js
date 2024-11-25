document.addEventListener('DOMContentLoaded', () => {
    const escolaId = localStorage.getItem('currentescola');
    if (!escolaId) {
        alert('Nenhuma escola selecionada!');
        window.location.href = 'index.html';
        return;
    }

    document.getElementById('escola-title').innerText = `Detalhes da Escola ${escolaId}`;
    initializePhotoUploads();
    loadSavedPhotos();
});

// Inicializa os campos de upload de fotos de A a Z com pré-visualização
function initializePhotoUploads() {
    const photoContainer = document.getElementById('photo-uploads');
    for (let char of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
        const wrapper = document.createElement('div');
        wrapper.id = `wrapper-${char}`;
        wrapper.style.marginBottom = '20px';

        const label = document.createElement('label');
        label.innerText = `Foto ${char}:`;

        const preview = document.createElement('img');
        preview.id = `preview-${char}`;
        preview.alt = `Pré-visualização Foto ${char}`;
        preview.style.width = '150px';
        preview.style.height = '150px';
        preview.style.objectFit = 'cover';
        preview.style.display = 'none'; // Oculta até que haja uma imagem

        const input = document.createElement('input');
        input.type = 'file';
        input.id = `photo-${char}`;
        input.accept = 'image/*';
        input.style.marginTop = '10px';
        input.addEventListener('change', (event) => handleFileChange(event, char));
        console.log(input.type)

        wrapper.appendChild(label);
        wrapper.appendChild(preview);
        wrapper.appendChild(input);
        photoContainer.appendChild(wrapper);
    }
}

// Manipula o evento de mudança de arquivo para exibir a pré-visualização
function handleFileChange(event, char) {
    const input = event.target;
    const preview = document.getElementById(`preview-${char}`);

    if (input.files && input.files[0]) {
        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result; // Define a pré-visualização com a imagem carregada
            preview.style.display = 'block'; // Exibe o preview
        };

        reader.readAsDataURL(file); // Lê o arquivo para criar a URL de visualização
    }
}

// Carrega as fotos salvas do localStorage e exibe no campo de upload correspondente
function loadSavedPhotos() {
    const escolaId = localStorage.getItem('currentescola');
    const photos = JSON.parse(localStorage.getItem(`photos-${escolaId}`)) || {};

    for (let char of Object.keys(photos)) {
        const preview = document.getElementById(`preview-${char}`);
        if (preview) {
            preview.src = photos[char];
            preview.style.display = 'block'; // Exibe a imagem salva
        }
    }
}

function convertToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

// Sincroniza as fotos com o backend
async function synchronize() {
    const escolaId = localStorage.getItem('currentescola');
    if (!escolaId) {
        alert('Nenhuma escola selecionada!');
        return;
    }

    let photosData = {}; // Armazena as fotos em formato Base64
    let hasFiles = false;

    for (let char of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
        const input = document.getElementById(`photo-${char}`);
        if (input && input.files.length > 0) {
            hasFiles = true;
            const file = input.files[0];

            // Validação: verificar se é uma imagem
            if (!file.type.startsWith('image/')) {
                alert(`O arquivo ${file.name} não é uma imagem válida.`);
                continue;
            }

            try {
                const base64Image = await convertToBase64(file);
                photosData[char] = base64Image; // Adiciona a foto ao objeto
            } catch (error) {
                console.error(`Erro ao converter ${file.name}:`, error);
                alert(`Erro ao processar o arquivo ${file.name}.`);
                continue;
            }
        }
    }

    if (!hasFiles) {
        alert('Nenhuma foto selecionada para sincronizar.');
        return;
    }

    const data = { // Organiza os dados no formato esperado pelo backend
        nome: escolaId,
        fotos: photosData
    };

    try {
        // Envia os dados para o backend
        const response = await fetch('http://localhost:5000/api/detalhes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        });

        if (response.ok) {
            const result = await response.json();
            console.log('Sincronização bem-sucedida:', result);
            alert('Sincronização concluída!');
        } else {
            console.error('Erro na sincronização:', response.statusText);
            alert(`Erro ao sincronizar fotos: ${response.status}`);
        }
    } catch (error) {
        console.error('Erro de conexão:', error);
        alert('Erro de conexão com o servidor.');
    }
}


// Salva as fotos no localStorage e atualiza a visualização
function savePhotos() {
    const escolaId = localStorage.getItem('currentescola');
    if (!escolaId) {
        alert('Nenhuma escola selecionada!');
        return;
    }

    // Carrega as fotos existentes do localStorage
    const existingPhotos = JSON.parse(localStorage.getItem(`photos-${escolaId}`)) || {};

    // Atualiza o objeto de fotos com as novas imagens
    for (let char of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
        const input = document.getElementById(`photo-${char}`);
        const preview = document.getElementById(`preview-${char}`);
        if (input && input.files.length > 0 && preview) {
            existingPhotos[char] = preview.src; // Atualiza ou adiciona a nova imagem
        }
    }

    // Salva o objeto atualizado no localStorage
    localStorage.setItem(`photos-${escolaId}`, JSON.stringify(existingPhotos));
    alert('Fotos salvas com sucesso!');
    loadSavedPhotos(); // Atualiza a exibição com as imagens salvas
}
