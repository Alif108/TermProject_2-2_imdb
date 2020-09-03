DROP TABLE "Artist";
CREATE TABLE "Artist" (
  "aID " NUMBER NOT NULL,
  "Name" VARCHAR2(30) NOT NULL,
  "Gender" VARCHAR2(20) NOT NULL,
  "Birth_Date" DATE NOT NULL,
  "Nationality" VARCHAR2(30) NOT NULL,
  "Birth_Place" VARCHAR2(30) NOT NULL,
  "Death_Date" DATE,
  "Photo" BLOB NOT NULL,
  CONSTRAINT "ArtistPK" PRIMARY KEY ("aID ")
);

