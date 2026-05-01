CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    level VARCHAR(50),
    goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE learning_state (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    current_topic TEXT,
    last_score FLOAT,
    iteration INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student
        FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);

CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    topic TEXT,
    questions JSONB,
    answers JSONB,
    score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student_eval
        FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
