IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[oneliners]') AND type in (N'U'))
CREATE TABLE oneliners (
    number INT IDENTITY(1,1) PRIMARY KEY,
    category NVARCHAR(80) NOT NULL,
    joke NVARCHAR(MAX) NOT NULL
);
