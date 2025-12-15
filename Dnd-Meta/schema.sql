CREATE TABLE Players (
  PlayerID INTEGER PRIMARY KEY,
  PlayerName TEXT NOT NULL
);

CREATE TABLE Campaigns (
  CampaignID INTEGER PRIMARY KEY,
  Title TEXT NOT NULL,
  Setting TEXT
);

CREATE TABLE Races (
  RaceID INTEGER PRIMARY KEY,
  RaceName TEXT NOT NULL
);

CREATE TABLE Classes (
  ClassID INTEGER PRIMARY KEY,
  ClassName TEXT NOT NULL,
  Tier INTEGER,
  Popularity TEXT
);

CREATE TABLE Sessions (
  SessionID INTEGER PRIMARY KEY,
  CampaignID INTEGER NOT NULL,
  SessionDate DATE NOT NULL,
  Notes TEXT,
  FOREIGN KEY (CampaignID) REFERENCES Campaigns(CampaignID)
);

CREATE TABLE SessionPlayers (
  SessionID INTEGER NOT NULL,
  PlayerID  INTEGER NOT NULL,
  RaceID    INTEGER,
  ClassID   INTEGER,
  Subclass  TEXT,
  PRIMARY KEY (SessionID, PlayerID),
  FOREIGN KEY (SessionID) REFERENCES Sessions(SessionID),
  FOREIGN KEY (PlayerID)  REFERENCES Players(PlayerID),
  FOREIGN KEY (RaceID)    REFERENCES Races(RaceID),
  FOREIGN KEY (ClassID)   REFERENCES Classes(ClassID)
);

-- === SPELLS ===
CREATE TABLE IF NOT EXISTS Spells (
    SpellID     INTEGER PRIMARY KEY,
    Name        TEXT NOT NULL,
    Level       INTEGER NOT NULL,          -- 0 = cantrip, 1–9 = spell level
    School      TEXT,                      -- Evocation, Abjuration, etc.
    CastingTime TEXT,
    Range       TEXT,
    Components  TEXT,                      -- e.g. "V,S,M"
    Duration    TEXT,
    Ritual      INTEGER DEFAULT 0,         -- 0 = no, 1 = ritual
    Concentration INTEGER DEFAULT 0        -- 0 = no, 1 = yes
);

-- Many-to-many between Classes and Spells
CREATE TABLE IF NOT EXISTS ClassSpells (
    ClassID  INTEGER NOT NULL,
    SpellID  INTEGER NOT NULL,
    PRIMARY KEY (ClassID, SpellID),
    FOREIGN KEY (ClassID) REFERENCES Classes(ClassID),
    FOREIGN KEY (SpellID) REFERENCES Spells(SpellID)
);
