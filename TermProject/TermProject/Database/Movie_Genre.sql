DROP TABLE "MOVIE_GENRE";
CREATE TABLE "MOVIE_GENRE" (
  "mID" NUMBER NOT NULL,
  "gID" NUMBER NOT NULL,
  CONSTRAINT "MovieGenrePk" PRIMARY KEY ("mID", "gID")
);

ALTER TABLE "Movie_Genre" ADD CONSTRAINT "Movie_Movie_Genre_Fk" FOREIGN KEY ("mID") REFERENCES Movie("mID") ON DELETE CASCADE;
ALTER TABLE "Movie_Genre" ADD CONSTRAINT "Genre_Movie_Genre_Fk" FOREIGN KEY ("gID") REFERENCES Genre("gID") ON DELETE CASCADE;
