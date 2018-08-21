DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS Names;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS MemberRoles;
DROP TABLE IF EXISTS Roles;

CREATE TABLE entries (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    'text' text NOT NULL
);

CREATE TABLE Question (question_id integer PRIMARY KEY AUTOINCREMENT, block_id INTEGER question_text text);
CREATE TABLE Blocks (block_id integer PRIMARY KEY AUTOINCREMENT, block_name text);
CREATE TABLE Box (box_id integer PRIMARY KEY AUTOINCREMENT, box_name text);
CREATE TABLE Answer (question_id integer, user_id integer, attempt integer, answer_text text, PRIMARY KEY (question_id, user_id, attempt));

CREATE TABLE QUUSBOX_MATRIX (question_id INTEGER, box_id INTEGER, user_id INTEGER, PRIMARY KEY (question_id, box_id, user_id))

CREATE TABLE User (user_id integer PRIMARY KEY AUTOINCREMENT, name text, surname text);
CREATE TABLE UserRoles (user_id integer UNIQUE, role_id INTEGER, PRIMARY KEY (user_id));
CREATE TABLE Roles (role_id integer PRIMARY KEY AUTOINCREMENT, name text);


INSERT INTO entries (title, 'text') values ('Закреплённое навеки тестовое сообщение', 'Это учебный микроблог, который должен быть веб-прослойкой для вк-бота. В дальнейшем здесь будет собираться статистика и всякая левая неособо интересная инфа, нужная для двух с половиной недопрогеров.')

INSERT INTO Roles (name) values ('Студент')
INSERT INTO Roles (name) values ('Преподаватель')
INSERT INTO Roles (name) values ('Супер')
