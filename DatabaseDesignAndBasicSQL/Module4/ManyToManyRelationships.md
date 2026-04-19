# Notes on Many To Many Relationships

---

**Really important in databases but can be a bit tricky to understand at first.**

Previously in the exercise, Many to one relationships, which were:

- **Track -> Album**: Many tracks can belong to one album.
- **Track -> Genre**: Many tracks can belong to one genre.
- **Album -> Artist**: Many albums can belong to one artist.

But in real world you see that tracks or usually on multiple albums. For example, a track can be on the original album and also on a compilation album. So there is a many-to-many relationship between tracks and albums.
**A track can have many albums as well as an album can have many tracks.**

_How do we model this in a relational database?_

---

## Many to Many Relationships

---

A naive approach would be to have multiple columns in the track for album1, album2, album3 etc. But this is not a good approach because we don't know how many albums a track can be on and it can lead to a lot of null values in the database.

The correct approach is a `Junction Table` or `Association Table` or `Link Table`. This is a table that has foreign keys to both the track and the album tables. This table will have one row for each combination of track and album.

We need to add a **connection** table with two foreign keys. This table will have a foreign key to the track table and a foreign key to the album table. This way we can model the many-to-many relationship between tracks and albums.
This sort of simplifies the relationship, now we have one to many relationship between track and connection table and one to many relationship between album and connection table. So we have broken down the many-to-many relationship into two one-to-many relationships. Which can be easily modeled in a relational database.

---

## Example of Many to Many Relationship

---

Let's start with a fresh database and create two tables, `student` and `course`. A student can enroll in many courses and a course can have many students. So there is a many-to-many relationship between students and courses.

```sql
CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128),
    email VARCHAR(128) UNIQUE
);

CREATE TABLE course (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) UNIQUE
);

CREATE TABLE member (
    student_id INTEGER REFERENCES student(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES course(id) ON DELETE CASCADE,
    role INTEGER,
    PRIMARY KEY (student_id, course_id)
)
```

`PRIMARY KEY (student_id, course_id)` means that the combination of student_id and course_id must be unique in the member table. This ensures that a student can only enroll in a course once.

---

## Insert data into the tables

---

### Inserting data into the student and course tables

```sh
music=> INSERT INTO student (name, email)
music=> VALUES
music=> ('Jane', 'jane@tsugi.org'),
music=> ('Ed', 'ed@tsugi.org'),
music=> ('Sue', 'sue@tsugi.org');
music=> SELECT * FROM student;
 id | name | email
----+------+-------------------------
  1 | Jane | jane@tsugi.org
  2 | Ed   | ed@tsugi.org
  3 | Sue  | sue@tsugi.org

music=> INSERT INTO course (title) VALUES ('Python'), ('SQL'), ('PHP');
music=> SELECT * FROM course;
 id | title
----+-------
  1 | Python
  2 | SQL
  3 | PHP
```

### Insert memberships

```sql
INSERT INTO member (student_id, course_id, role)
VALUES
    (1, 1, 1),
    (2, 1, 0),
    (3, 1, 0),
    (1, 2, 0),
    (2, 2, 1),
    (2, 3, 1),
    (3, 3, 0);
```

---

## Complexity Enables Speed

---

- Complexity makes speed possible and allows you to get very fast results as the data size grows.
- By **normalizing the data and linking it with integer keys**, the overall **amount of data** which the relational database must _scan_ is far lower than if the data were simply flattened out.
- It might seem like a **tradeoff** - spend some time designing your database so it continues to be fast when your application is a success.
