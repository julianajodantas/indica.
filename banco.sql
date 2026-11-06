CREATE DATABASE IF NOT EXISTS indica
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE indica;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recomendacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    categoria ENUM('Livro', 'Filme', 'Série', 'Música') NOT NULL,
    descricao TEXT,
    avaliacao DECIMAL(2,1) NOT NULL DEFAULT 5.0,
    usuario_id INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recomendacoes_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    recomendacao_id INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_favoritos_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_favoritos_recomendacao
        FOREIGN KEY (recomendacao_id) REFERENCES recomendacoes(id)
        ON DELETE CASCADE,
    UNIQUE KEY usuario_recomendacao_unicos (usuario_id, recomendacao_id)
);
