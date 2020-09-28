DROP TABLE "GENRE";
CREATE TABLE "GENRE" (
  "gID" NUMBER NOT NULL,
  "Name" VARCHAR2(30) NOT NULL,
  CONSTRAINT "GenrePk" PRIMARY KEY ("gID")
);

CREATE SEQUENCE seq_genre
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;
