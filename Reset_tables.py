import sqlite3

con = sqlite3.connect("kleps.db")
cursor = con.cursor()
msg = ''

try:
    cursor.execute("DROP TABLE userInfo")
    msg += 'La Table userInfo a été reinitialisée'
except:
    None

try:
    cursor.execute("DROP TABLE debates")
    msg += ' La Table debates a été reinitialisée'
except:
    None

try:
    cursor.execute("DROP TABLE messages")
    msg += ' La Table messages a été reinitialisée'
except:
    None

try:
    cursor.execute("DROP TABLE tokens")
    msg += ' La Table tokens a été reinitialisée'
except:
    None

try:
    cursor.execute("DROP TABLE spaces_users")
    msg += 'La Table spaces_users a été reinitialisée'
except:
    None

print(msg)