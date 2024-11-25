CREATE TABLE IF NOT EXISTS escolas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    metragem FLOAT DEFAULT NULL,
    status VARCHAR(50) DEFAULT 'pendente'
);

INSERT INTO escolas (nome, endereco, metragem, status) VALUES
('Escola A', 'Rua 1, Centro', 200, 'pendente'),
('Escola B', 'Rua 2, Bairro B', 150, 'coletado'),
('Escola C', 'Av. Principal, Bairro C', NULL, 'pendente');

CREATE TABLE IF NOT EXISTS fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    foto LONGBLOB NOT NULL,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
