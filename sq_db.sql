create table if not exists tv (
rowid integer primary key autoincrement,
mac text not null,
user_id integer,
monter text,
comment text,
status text,
date text
);

create table if not exists router (
rowid integer primary key autoincrement,
wan_mac text,
lan_mac text not null,
model text not null,
user_id integer,
monter text,
comment text,
status text,
date text
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
login text NOT NULL,
psw text NOT NULL,
name text,
admin integer
);

CREATE TABLE IF NOT EXISTS monter (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
id_billing integer
);

CREATE TABLE IF NOT EXISTS commentsTV (
rowid integer PRIMARY KEY AUTOINCREMENT,
comment text,
id integer
);

CREATE TABLE IF NOT EXISTS commentsRouter (
rowid integer PRIMARY KEY AUTOINCREMENT,
comment text,
id integer
);