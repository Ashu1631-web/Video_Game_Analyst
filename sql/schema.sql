-- 🎮 GAMES DATA

-- 1. Top Rated Games
SELECT Title, Rating FROM games ORDER BY Rating DESC LIMIT 10;

-- 2. Most Wishlisted
SELECT Title, Wishlist FROM games ORDER BY Wishlist DESC LIMIT 10;

-- 3. Avg Rating by Genre
SELECT Genres, AVG(Rating) FROM games GROUP BY Genres;

-- 4. Most Played
SELECT Title, Plays FROM games ORDER BY Plays DESC LIMIT 10;

-- 5. Developer Performance
SELECT Team, AVG(Rating) FROM games GROUP BY Team;


-- 💰 SALES DATA

-- 6. Sales by Platform
SELECT Platform, SUM(Global_Sales) FROM vgsales GROUP BY Platform;

-- 7. Top Publishers
SELECT Publisher, SUM(Global_Sales) FROM vgsales GROUP BY Publisher;

-- 8. Yearly Sales
SELECT Year, SUM(Global_Sales) FROM vgsales GROUP BY Year;

-- 9. Regional Sales
SELECT SUM(NA_Sales), SUM(EU_Sales), SUM(JP_Sales) FROM vgsales;

-- 10. Top Selling Games
SELECT Name, Global_Sales FROM vgsales ORDER BY Global_Sales DESC LIMIT 10;


-- 🔄 COMBINED

-- 11. Rating vs Sales
SELECT g.Title, g.Rating, v.Global_Sales 
FROM games g JOIN vgsales v ON g.Title = v.Name;

-- 12. Genre Sales
SELECT Genre, SUM(Global_Sales) FROM vgsales GROUP BY Genre;

-- 13. Platform Rating
SELECT v.Platform, AVG(g.Rating)
FROM games g JOIN vgsales v ON g.Title = v.Name
GROUP BY v.Platform;

-- 14. Wishlist vs Sales
SELECT g.Title, g.Wishlist, v.Global_Sales
FROM games g JOIN vgsales v ON g.Title = v.Name;

-- 15. Genre + Platform
SELECT Genre, Platform, SUM(Global_Sales)
FROM vgsales GROUP BY Genre, Platform;
