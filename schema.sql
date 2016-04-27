DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS Results;

CREATE TABLE Students(
    ID INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT);

CREATE TABLE Quiz(
    ID INTEGER PRIMARY KEY, subject TEXT, questions INT, quizDate date);
						
CREATE TABLE Results(
    ID INTEGER PRIMARY KEY, quizID INT, studentID INT, score INT);

INSERT INTO Students VALUES(NULL,'John','Smith');
INSERT INTO Quiz VALUES(NULL,'Python Basics',5,'02/05/2015');
INSERT INTO Results select NULL,(
    select ID from Quiz where subject = 'Python Basics'
    ),(
        select ID from Students where firstName = 'John' and lastName = 'Smith'
        ),85;



