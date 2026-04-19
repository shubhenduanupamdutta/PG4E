CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE
);

DROP TABLE course CASCADE;

-- `DROP TABLE course CASCADE` is used to drop the `course` table and all its dependent objects, such as foreign key constraints. This allows us to recreate the `course` table with the necessary changes without encountering errors due to existing dependencies.

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) UNIQUE
);

DROP TABLE roster CASCADE;
CREATE TABLE roster (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES student(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES course(id) ON DELETE CASCADE,
    role INTEGER,
    UNIQUE (student_id, course_id)
);