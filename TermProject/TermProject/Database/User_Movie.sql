-- DROP TABLE "USER_MOVIE";
CREATE TABLE "USER_MOVIE" (
  "rating" FLOAT(53) NOT NULL,
  "usID" NUMBER NOT NULL,
  "mID" NUMBER NOT NULL,
  CONSTRAINT "UserMoviePk" PRIMARY KEY ("usID", "mID")
);

ALTER TABLE "User_Movie" ADD CONSTRAINT "User_User_Movie_Fk" FOREIGN KEY ("usID") REFERENCES Users("usID") ON DELETE CASCADE;
ALTER TABLE "User_Movie" ADD CONSTRAINT "Movie_User_Movie_Fk" FOREIGN KEY ("mID") REFERENCES Movie("mID") ON DELETE CASCADE;