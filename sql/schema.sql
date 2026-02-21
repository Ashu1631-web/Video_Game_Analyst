CREATE TABLE games (
    Title VARCHAR(255) PRIMARY KEY,
    Rating FLOAT,
    Genres VARCHAR(255),
    Plays INT,
    Backlogs INT,
    Wishlist INT,
    Release_Date DATE,
    Platform VARCHAR(100),
    Team VARCHAR(255)
);

CREATE TABLE sales (
    Title VARCHAR(255),
    Platform VARCHAR(100),
    Year INT,
    Genre VARCHAR(100),
    Publisher VARCHAR(255),
    NA_Sales FLOAT,
    EU_Sales FLOAT,
    JP_Sales FLOAT,
    Other_Sales FLOAT,
    Global_Sales FLOAT
);
