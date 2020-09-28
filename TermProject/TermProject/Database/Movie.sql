DROP TABLE "Movie";
CREATE TABLE "Movie" (
  "mID" NUMBER NOT NULL,
  "Title" VARCHAR2(30) NOT NULL,
  "Release_Date" DATE NOT NULL,
  "Rating" INTEGER NOT NULL,
  "Duration" INTEGER NOT NULL,
	"Language" VARCHAR2(20) NOT NULL,
  CONSTRAINT "MoviePK" PRIMARY KEY ("mID"),
  CONSTRAINT "RatingMovie" CHECK ("Rating" BETWEEN 1 and 10)
);

CREATE SEQUENCE seq_movie
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;
