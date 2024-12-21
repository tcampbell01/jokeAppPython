DROP TABLE IF EXISTS oneliners;

CREATE TABLE oneliners (
    number INT IDENTITY(1,1) PRIMARY KEY,
    category NVARCHAR(80) NOT NULL,
    joke NVARCHAR(MAX) NOT NULL
);


