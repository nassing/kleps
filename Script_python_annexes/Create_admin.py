import sqlite3

con = sqlite3.connect("kleps.db")
cursor = con.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS userInfo (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                        username TEXT NOT NULL UNIQUE,
                                                        email TEXT NOT NULL UNIQUE,
                                                        password TEXT NOT NULL,
                                                        is_admin INT NOT NULL DEFAULT 0)''')

def create_admin(username, email, password):
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO userInfo (username,email,password,is_admin) VALUES (?, ?, ?, ?)", (username, email, password,1))
        con.commit()
        con.close
        return username + "a été ajouté en tant qu'admin"
    except:
        con.close
        return 'Erreur durant la procédure'


create_admin()