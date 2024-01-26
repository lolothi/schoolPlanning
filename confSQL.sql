CREATE TABLE IF NOT EXISTS Childs (
    id integer primary key autoincrement,
    child_name VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Activities (
    id integer primary key autoincrement,
    activity_name VARCHAR(30) UNIQUE NOT NULL,
    activity_price decimal(4, 2) NOT NULL,
    activity_time smallint,
    activity_comment VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS School_months (
    id integer primary key autoincrement, 
    year integer NOT NULL,
    month integer NOT NULL,
    school_days integer,
    payed boolean DEFAULT 0,
    price_calculated integer,
    price_payed integer,
    activities integer,
    school_canceled boolean DEFAULT 0,
    family_canceled boolean DEFAULT 0,
    strike_canceled boolean DEFAULT 0,
    UNIQUE(year, month)
);

CREATE TABLE IF NOT EXISTS Comments (
    id integer primary key autoincrement, 
    comment VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Usual_activities (
    id integer primary key autoincrement,
    day VARCHAR(15) NOT NULL,
    activity_id integer,
    child_id integer,
    FOREIGN KEY (activity_id) REFERENCES Activities(id),
    FOREIGN KEY (child_id) REFERENCES Childs(id),
    UNIQUE(day, activity_id, child_id)
);

CREATE TABLE IF NOT EXISTS Month_activities (
    id integer primary key autoincrement, 
    date text NOT NULL,
    activity_id integer,
    child_id integer,
    web_validated boolean DEFAULT 0,
    school_canceled boolean DEFAULT 0,
    family_canceled boolean DEFAULT 0,
    strike_canceled boolean DEFAULT 0,
    comment_id integer,
    FOREIGN KEY (activity_id) REFERENCES Activities(id),
    FOREIGN KEY (child_id) REFERENCES Childs(id),
    FOREIGN KEY (comment_id) REFERENCES Comments(id)
);

CREATE TABLE IF NOT EXISTS off_days (
    id integer primary key autoincrement, 
    date text NOT NULL,
    child_id integer,
    web_validated boolean DEFAULT 0,
    school_canceled boolean DEFAULT 0,
    family_canceled boolean DEFAULT 0,
    strike_canceled boolean DEFAULT 0,
    comment_id integer,
    FOREIGN KEY (child_id) REFERENCES Childs(id),
    FOREIGN KEY (comment_id) REFERENCES Comments(id)
);

