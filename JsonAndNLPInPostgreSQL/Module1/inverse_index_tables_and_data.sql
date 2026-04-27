CREATE TABLE docs01 (id SERIAL, doc TEXT, PRIMARY KEY(id));

CREATE TABLE invert01 (
  keyword TEXT,
  doc_id INTEGER REFERENCES docs01(id) ON DELETE CASCADE
);

INSERT INTO docs01 (doc) VALUES
('communicate with it Python is not intelligent You are'),
('really just having a conversation with yourself but using proper'),
('In a sense when you use a program written by someone else the'),
('conversation is between you and those other programmers with Python'),
('acting as an intermediary Python is a way for the creators of programs'),
('to express how the conversation is supposed to proceed And in just a'),
('few more chapters you will be one of those programmers using Python to'),
('talk to the users of your program'),
('Before we leave our first conversation with the Python interpreter you'),
('should probably know the proper way to say goodbye when interacting');