-- ==========================================
-- DATABASE: Video Game Analytics
-- ==========================================

CREATE DATABASE IF NOT EXISTS video_game_analytics;
USE video_game_analytics;

-- ==========================================
-- TABLE: games (Engagement Data)
-- ==========================================

CREATE TABLE games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Rating FLOAT,
    Genres VARCHAR(255),
    Plays INT,
    Backlogs INT,
    Wishlist INT,
    Release_Date DATE,
    Platform VARCHAR(100),
    Team VARCHAR(255),
    UNIQUE (Title)
);

-- ==========================================
-- TABLE: sales (Regional Sales Data)
-- ==========================================

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Platform VARCHAR(100),
    Year INT,
    Genre VARCHAR(100),
    Publisher VARCHAR(255),
    NA_Sales FLOAT,
    EU_Sales FLOAT,
    JP_Sales FLOAT,
    Other_Sales FLOAT,
    Global_Sales FLOAT,
    
    FOREIGN KEY (Title) REFERENCES games(Title)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ==========================================
-- INDEXES FOR PERFORMANCE
-- ==========================================

CREATE INDEX idx_genre ON sales(Genre);
CREATE INDEX idx_platform ON sales(Platform);
CREATE INDEX idx_year ON sales(Year);
CREATE INDEX idx_publisher ON sales(Publisher);

-- ==========================================
-- VIEW: Merged Dataset
-- ==========================================

CREATE VIEW merged_game_data AS
SELECT 
    g.Title,
    g.Rating,
    g.Genres,
    g.Plays,
    g.Backlogs,
    g.Wishlist,
    g.Release_Date,
    g.Platform AS Game_Platform,
    g.Team,
    s.Year,
    s.Genre,
    s.Publisher,
    s.NA_Sales,
    s.EU_Sales,
    s.JP_Sales,
    s.Other_Sales,
    s.Global_Sales
FROM games g
JOIN sales s
ON g.Title = s.Title;
