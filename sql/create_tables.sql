CREATE TABLE IF NOT EXISTS joke (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(80) NOT NULL,
    joke TEXT NOT NULL,
    punchline TEXT NOT NULL
);