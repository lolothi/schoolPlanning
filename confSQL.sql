
CREATE TABLE IF NOT EXISTS Childs (
id integer primary key autoincrement, 
childname VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Activities (
id integer primary key autoincrement, 
activityname VARCHAR(30) UNIQUE NOT NULL,
activityprice decimal(4,2) NOT NULL, 
activitytime smallint,
activitycomment VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Usualactivities (
id integer primary key autoincrement, 
day VARCHAR(15) NOT NULL,
activity_id integer, 
FOREIGN KEY (activity_id) REFERENCES Activities(id)
);

-- CREATE TABLE IF NOT EXISTS Usualactivities (
-- id integer primary key autoincrement, 
-- day VARCHAR(15) NOT NULL,
-- activity_id integer, 
-- FOREIGN KEY (activity_id) REFERENCES Activities(id),
-- child_id integer, 
-- FOREIGN KEY (child_id) REFERENCES Childs(id)
-- );

-- CREATE TABLE IF NOT EXISTS MonthActivities (
-- id integer primary key autoincrement, 
-- day integer NOT NULL,
-- year integer NOT NULL,
-- month integer NOT NULL,
-- activity_id integer, 
-- FOREIGN KEY (activity_id) REFERENCES Activities(id),
-- child_id integer, 
-- FOREIGN KEY (child_id) REFERENCES Childs(id)
-- );


