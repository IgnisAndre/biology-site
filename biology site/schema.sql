DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Blocks;
DROP TABLE IF EXISTS Box;
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS CorrectAnswer;
DROP TABLE IF EXISTS QUUSBOX_MATRIX;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserRoles;
DROP TABLE IF EXISTS Roles;

CREATE TABLE entries (id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, 'text' text NOT NULL);

CREATE TABLE Questions (question_id integer PRIMARY KEY AUTOINCREMENT, block_id INTEGER, question_text text);
CREATE TABLE Blocks (block_id integer PRIMARY KEY AUTOINCREMENT, block_name text, is_open INTEGER);
CREATE TABLE Boxes (box_id integer PRIMARY KEY AUTOINCREMENT, box_name text);
CREATE TABLE Answers (question_id integer, user_id integer, answer_text text, PRIMARY KEY (question_id, user_id)); --а нужны ли попытки
CREATE TABLE CorrectAnswers (question_id integer PRIMARY KEY, c_answer_text text);

CREATE TABLE QUUSBOX_MATRIX (question_id INTEGER, box_id INTEGER, user_id INTEGER, PRIMARY KEY (question_id, box_id, user_id));

CREATE TABLE User (user_id integer PRIMARY KEY AUTOINCREMENT, username text UNIQUE, password text, name text, surname text);
CREATE TABLE UserRoles (user_id integer UNIQUE, role_id INTEGER, PRIMARY KEY (user_id));
CREATE TABLE Roles (role_id integer PRIMARY KEY AUTOINCREMENT, name text);


INSERT INTO entries (title, 'text') values ('Позже здесь будет описание методики и всякие новости', 'а пока просто маленькое сообщение. Чтоб не скучать, вот анекдот: идёт медведь по лесу. Видит - машина горит. Сел в неё и сгорел. Ахахахах');

INSERT INTO Roles (name) values ('Неподтверждённый');
INSERT INTO Roles (name) values ('Студент');
INSERT INTO Roles (name) values ('Преподаватель');
INSERT INTO Roles (name) values ('Суперпреподватель');
INSERT INTO Roles (name) values ('Мастер');

INSERT INTO User (username, password, name, surname) values ('Master', 'One', 'Ignis', 'Sanat');
INSERT INTO User (username, password, name, surname) values ('RedWitch', 'RedDog', 'Даша', 'Креветка');
INSERT INTO User (username, password, name, surname) values ('student', 'pass', 'stn1', 'sts1');
INSERT INTO User (username, password, name, surname) values ('teacher', 'pass', 'ten1', 'tes1');

INSERT INTO UserRoles (user_id, role_id) values (1, 5);
INSERT INTO UserRoles (user_id, role_id) values (2, 4);
INSERT INTO UserRoles (user_id, role_id) values (3, 2);
INSERT INTO UserRoles (user_id, role_id) values (4, 3);

INSERT INTO Boxes (box_name) values ('Каждый день');
INSERT INTO Boxes (box_name) values ('Раз в два дня');
INSERT INTO Boxes (box_name) values ('Раз в неделю');
INSERT INTO Boxes (box_name) values ('Раз в месяц');

INSERT INTO Blocks (block_name, is_open) values ('test', 1);
INSERT INTO Blocks (block_name, is_open) values ('test2', 0);

INSERT INTO Questions (block_id, question_text) values (1, 'test question 1');
INSERT INTO Questions (block_id, question_text) values (1, 'test question 2');
INSERT INTO Questions (block_id, question_text) values (2, 'test question 3');

INSERT INTO CorrectAnswers (question_id, c_answer_text) values (1, 'test question 1 answer');
INSERT INTO CorrectAnswers (question_id, c_answer_text) values (2, 'test question 2 answer');
INSERT INTO CorrectAnswers (question_id, c_answer_text) values (3, 'test question 3 answer');
