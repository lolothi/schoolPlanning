
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
day VARCHAR(30) NOT NULL,
activity_id integer, 
FOREIGN KEY (activity_id) REFERENCES Activities(id)
);



