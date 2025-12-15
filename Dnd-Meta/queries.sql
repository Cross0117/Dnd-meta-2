-- 1) Most popular class overall
SELECT
    c.ClassName,
    COUNT(*) AS TimesPlayed
FROM SessionPlayers sp
JOIN Classes c ON c.ClassID = sp.ClassID
GROUP BY c.ClassName
ORDER BY TimesPlayed DESC;

-- 2) Most popular race overall
SELECT
    r.RaceName,
    COUNT(*) AS TimesPlayed
FROM SessionPlayers sp
JOIN Races r ON r.RaceID = sp.RaceID
GROUP BY r.RaceName
ORDER BY TimesPlayed DESC;

-- 3) Top race-class combinations
SELECT
    r.RaceName,
    c.ClassName,
    COUNT(*) AS TimesPlayed
FROM SessionPlayers sp
JOIN Races r   ON r.RaceID = sp.RaceID
JOIN Classes c ON c.ClassID = sp.ClassID
GROUP BY r.RaceName, c.ClassName
ORDER BY TimesPlayed DESC;

-- 4) Most active players by session count
SELECT
    p.PlayerName,
    COUNT(DISTINCT sp.SessionID) AS SessionsPlayed
FROM SessionPlayers sp
JOIN Players p ON p.PlayerID = sp.PlayerID
GROUP BY p.PlayerName
ORDER BY SessionsPlayed DESC;

-- 5) Campaign engagement: total player appearances
SELECT
    cam.Title AS CampaignTitle,
    COUNT(*) AS TotalPlayerAppearances,
    COUNT(DISTINCT s.SessionID) AS SessionCount,
    COUNT(DISTINCT sp.PlayerID) AS UniquePlayers
FROM SessionPlayers sp
JOIN Sessions s   ON s.SessionID = sp.SessionID
JOIN Campaigns cam ON cam.CampaignID = s.CampaignID
GROUP BY cam.Title
ORDER BY TotalPlayerAppearances DESC;
