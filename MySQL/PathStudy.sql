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

CREATE TABLE playlists (
    id_playlist INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE CASCADE
);

CREATE TABLE playlist_videos (
    PRIMARY KEY (id_playlist, id_video),
    id_playlist INT,
    id_video INT,
    ordem INT DEFAULT 1,
    FOREIGN KEY (id_playlist) REFERENCES playlists (id_playlist) ON DELETE CASCADE,
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

