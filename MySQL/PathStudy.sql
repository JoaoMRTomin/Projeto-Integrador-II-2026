use pathstudy;

CREATE TABLE usuarios (
    id_usuario int PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(40) not NULL,
    email VARCHAR(80) UNIQUE NOT NULL,
    senha VARCHAR(30) not NULL,
    criação DATETIME
);


CREATE TABLE videos (
    id_video INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    url_video VARCHAR(255) NOT NULL,
    duracao_segundos INT NOT NULL
);

CREATE TABLE cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id VARCHAR(100) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50)
);

CREATE TABLE curso_videos (
    PRIMARY KEY (id_curso, id_video),
    id_curso INT,
    id_video INT,
    ordem INT DEFAULT 1, -- A ordem da aula dentro DAQUELE curso específico
    FOREIGN KEY (id_curso) REFERENCES cursos (id_curso) ON DELETE CASCADE,
    FOREIGN KEY (id_video) REFERENCES videos (id_video) ON DELETE CASCADE
);


CREATE TABLE progresso_usuario (
    id_usuario INT,
    id_video INT,
    concluido BOOLEAN DEFAULT TRUE,
    data_conclusao DATETIME DEFAULT CURRENT_TIMESTAMP,
    tempo_parado_segundos INT DEFAULT 0, -- Opcional: para o recurso "continuar de onde parou"
    PRIMARY KEY (id_usuario, id_video),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_video) REFERENCES videos(id_video) ON DELETE CASCADE
);

SELECT * from cursos;

UPDATE cursos
SET imagem = 'https://i.pinimg.com/736x/fd/0a/88/fd0a883bd6f2fa6607ebe58fd7d30e60.jpg'
WHERE id_curso = 1;   
INSERT INTO cursos (titulo, playlist_id, cliques, categoria) 
VALUES ('Curso de Português', 'PLToTKj2C0mWDJowVTjT0FWL14dhXOVP9p', 0, 'Linguagens');