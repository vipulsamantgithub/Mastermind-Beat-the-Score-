import sqlite3
c=sqlite3.connect("C:/Users/SamantVi/OneDrive - Unisys/Desktop/Py/Chapter 14 -Project-3/game_scores.db")
cur=c.cursor()
cur.execute("Select * from scores")
for row in cur:
    print(row)
c.close()