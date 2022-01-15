import sqlite3

def createAdmin(id_user):
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("UPDATE userInfo SET is_admin=1 WHERE id=?",(id_user,))
    con.commit()
    con.close

createAdmin(1)