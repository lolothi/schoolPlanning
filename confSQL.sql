
CREATE TABLE IF NOT EXISTS Childs (
id integer primary key autoincrement, 
childname VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Activities (
id integer primary key autoincrement, 
activityname VARCHAR(30) NOT NULL,
activityprice decimal(4,2), 
activitytime smallint,
activitycomment VARCHAR(50) NOT NULL
);



