PRAGMA foreign_keys = OFF;

DELETE FROM SessionPlayers;
DELETE FROM Sessions;
DELETE FROM Players;
DELETE FROM Campaigns;
DELETE FROM Classes;
DELETE FROM Races;

PRAGMA foreign_keys = ON;

-- === RACES ===
INSERT INTO Races (RaceID, RaceName) VALUES
  (1, 'Human'),
  (2, 'Elf'),
  (3, 'Dwarf'),
  (4, 'Halfling'),
  (5, 'Tiefling');

-- === CLASSES ===
INSERT INTO Classes (ClassID, ClassName, Tier, Popularity) VALUES
  (1, 'Fighter', 'Mid', 'High'),
  (2, 'Wizard',  'High', 'High'),
  (3, 'Rogue',   'Mid', 'Medium'),
  (4, 'Cleric',  'High', 'Medium'),
  (5, 'Warlock', 'Mid', 'Low');

-- === PLAYERS ===
INSERT INTO Players (PlayerID, PlayerName) VALUES
  (1, 'Asha'),
  (2, 'Bryn'),
  (3, 'Corin'),
  (4, 'Dax'),
  (5, 'Elira'),
  (6, 'Finn');

-- === CAMPAIGNS ===
INSERT INTO Campaigns (CampaignID, Title, Setting) VALUES
  (1, 'Curse of the Ember King',   'Forgotten Realms'),
  (2, 'Shadows Over Blackreach',   'Homebrew Dark Fantasy'),
  (3, 'Storms of the Sapphire Sea','Seafaring / Ocean');

-- === SESSIONS ===
-- assume column is SessionDate; if yours is called "Date", change that
INSERT INTO Sessions (SessionID, CampaignID, SessionDate, Notes) VALUES
  (1, 1, '2025-01-05', 'Session 1: Village on fire'),
  (2, 1, '2025-01-12', 'Session 2: Into the Ember Mines'),
  (3, 1, '2025-01-19', 'Session 3: First boss fight'),
  (4, 2, '2025-02-02', 'Session 1: Mysterious disappearances'),
  (5, 2, '2025-02-09', 'Session 2: Cultist hideout'),
  (6, 3, '2025-03-01', 'Session 1: Shipwreck on sapphire reef');

-- === SESSION PLAYERS (attendance + build) ===
-- one row = one player in one session, with their race/class/subclass choice

INSERT INTO SessionPlayers (SessionID, PlayerID, RaceID, ClassID, Subclass) VALUES
  -- Campaign 1, Session 1
  (1, 1, 2, 2, 'Evocation'),      -- Asha: Elf Wizard
  (1, 2, 1, 1, 'Champion'),       -- Bryn: Human Fighter
  (1, 3, 4, 3, 'Thief'),          -- Corin: Halfling Rogue

  -- Campaign 1, Session 2
  (2, 1, 2, 2, 'Evocation'),
  (2, 2, 1, 1, 'Champion'),
  (2, 4, 3, 4, 'Life Domain'),    -- Dax: Dwarf Cleric

  -- Campaign 1, Session 3
  (3, 1, 2, 2, 'Evocation'),
  (3, 2, 1, 1, 'Champion'),
  (3, 4, 3, 4, 'Life Domain'),
  (3, 5, 5, 5, 'Fiend Pact'),     -- Elira: Tiefling Warlock

  -- Campaign 2, Session 1
  (4, 2, 1, 3, 'Assassin'),       -- Bryn: Human Rogue
  (4, 3, 4, 3, 'Thief'),
  (4, 6, 2, 1, 'Battlemaster'),   -- Finn: Elf Fighter

  -- Campaign 2, Session 2
  (5, 2, 1, 3, 'Assassin'),
  (5, 3, 4, 3, 'Thief'),
  (5, 6, 2, 1, 'Battlemaster'),

  -- Campaign 3, Session 1
  (6, 1, 2, 2, 'Evocation'),
  (6, 5, 5, 5, 'Fiend Pact'),
  (6, 6, 2, 1, 'Battlemaster');