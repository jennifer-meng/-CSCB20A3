drop table feedback;
drop table mark;
drop table remark;
drop table user;

CREATE TABLE "Remark" (
	"mark_id"	INTEGER,
	"reason"	TEXT
);
CREATE TABLE "User"(
	"username"	TEXT,
	"password"	TEXT,
	"admin"	INTEGER,
	PRIMARY KEY("username")
);
CREATE TABLE "Feedback" (
    "feedbackid" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Instructor" TEXT NOT NULL,
    "Q1" TEXT NOT NULL,
    "Q2" TEXT,
    "Q3" TEXT,
    "Q4" TEXT
);

CREATE TABLE "Mark" (
	"mark_id"	INTEGER NOT NULL,
	"name"	TEXT,
	"grade"	NUMERIC,
	"username"	TEXT NOT NULL,
	PRIMARY KEY("mark_id")
);