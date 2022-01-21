CREATE TABLE usuarios (
    nome_usuario TEXT NOT NULL PRIMARY KEY, 
    senha TEXT NOT NULL
);

CREATE TABLE cargos (
    id_cargo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    nivel_acesso INTEGER NOT NULL
);

CREATE TABLE funcionarios (
    id_funcionario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    foto_cracha BLOB,
    id_cargo INTEGER NOT NULL, 
    FOREIGN KEY (id_cargo) REFERENCES cargos (id_cargo) 
);

CREATE TABLE templates (
    id_template INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_funcionario INTEGER NOT NULL,
    descritor TEXT NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
);

CREATE TABLE log_det (
    id_log INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_funcionario INTEGER,
    autorizado INTEGER NOT NULL,
    data_det TEXT NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
);

INSERT INTO usuarios VALUES ('Daniel', '123');
INSERT INTO cargos (descricao, nivel_acesso) VALUES ('GERENTE', 0);
INSERT INTO funcionarios (nome, id_cargo) VALUES ('Daniel Jangua', 1);
INSERT INTO log_det (id_funcionario, autorizado, data_det) VALUES (1, 1, datetime('2022-01-19 01:02:20'));
