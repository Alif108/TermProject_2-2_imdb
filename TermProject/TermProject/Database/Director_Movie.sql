--DROP TABLE "DIRECTOR_MOVIE";
CREATE TABLE "DIRECTOR_MOVIE" (
  "dID" NUMBER NOT NULL,
  "mID" NUMBER NOT NULL,
  CONSTRAINT "DirectorMoviePk" PRIMARY KEY ("dID", "mID")
);

ALTER TABLE "DIRECTOR_MOVIE" ADD CONSTRAINT "Director_Director_Movie_Fk" FOREIGN KEY ("dID") REFERENCES DIRECTOR("dID") ON DELETE CASCADE;
ALTER TABLE "DIRECTOR_MOVIE" ADD CONSTRAINT "Movie_Director_Movie_Fk" FOREIGN KEY ("mID") REFERENCES MOVIE("mID") ON DELETE CASCADE;