from random import expovariate
import re
from flask import Flask, render_template, session, request, redirect, url_for, flash
from datetime import timedelta
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import math

app = Flask(__name__)
UPLOAD_FOLDER = 'static/data/audio_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "hello" #hello est une clé de cryptage
app.permanent_session_lifetime = timedelta(minutes=15) #faudrait expliquer cette ligne vite fait


#======================================================================================================================
#
#                                                    Databases
#
#======================================================================================================================


import sqlite3

con = sqlite3.connect("kleps.db")
cursor = con.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS userInfo (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                        username TEXT NOT NULL UNIQUE,
                                                        password TEXT NOT NULL,
                                                        is_admin INT NOT NULL DEFAULT 0)''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS messages (id_message INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                        path TEXT NOT NULL,
                                                        id_sender INTEGER NOT NULL REFERENCES userInfo(id),
                                                        id_debate VARCHAR(4) NOT NULL,
                                                        id_linked_message INTEGER DEFAULT 0,
                                                        message_title TEXT,
                                                        message_type TEXT DEFAULT "proposition")''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS debates (id_debate VARCHAR(4) NOT NULL PRIMARY KEY,
                                                       debate_name TEXT NOT NULL,
                                                       join_code VARCHAR(4),
                                                       id_creator INTEGER NOT NULL REFERENCES userInfo(id),
                                                       debate_description TEXT DEFAULT 'Pas de déscription')''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS tokens ( id_liker INTEGER NOT NULL REFERENCES userInfo(id),id_message INTEGER NOT NULL REFERENCES messages(id_message),id_debate VARCHAR(4) NOT NULL REFERENCES debates(id_debate),  PRIMARY KEY(id_liker,id_message))''')
cursor.execute(''' CREATE TABLE IF NOT EXISTS spaces_users ( id_user INTEGER NOT NULL REFERENCES userInfo(id),id_debate VARCHAR(4) NOT NULL REFERENCES debates(id_debate), PRIMARY KEY(id_user,id_debate))''')

#======================================================================================================================
#
#                                                    Fonctions diverses
#
#======================================================================================================================



def isLoggedIn():
    #Renvoie "true" si l'utilisateur connecté sinon "false"
    if "username" in session:
        return "true"
    return "false"

def credentialsAlreadyExists(username):
    #Fonction permettant de vérifier que les paramètres en entrée
    #sont bien compatibles avec les contraintes de la table
     con = sqlite3.connect("kleps.db")
     cursor = con.cursor()
     cursor.execute("SELECT username FROM userInfo")
     logInfo = cursor.fetchall()
     listVerif_username = []
     for info in logInfo:
        listVerif_username.append(info[0])
     if username in  listVerif_username:
         session["alert_message"]="Ce nom d'utilisateur existe déjà"
         return  True
         #On stocke les messages d'alertes dans session
     else:
         return False


def addNewUser( username, password):
    #Fonction premettant de rajouter un nouvel utilisateur
    if not credentialsAlreadyExists(username): #Si le bool est vérifié, on a un alert_message
        con = sqlite3.connect("kleps.db")
        cursor = con.cursor()
        command = "INSERT INTO userInfo (username, password) VALUES (?, ?)"
        cursor.execute( command, (username, password))
        con.commit()
        con.close

def isLogInfoCorrect(username, password):
    #Fonction permettant de vérifier que les paramètres en entrer
    #correspondent bien à un utilisateur via les données de la db
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT username,password FROM userInfo")
    logInfo = cursor.fetchall()
    listVerif = []
    for info in logInfo:
        listVerif.append((info[0],info[1]))
    if (username, password) in listVerif:
        return True
    return False


def generateDebateCode():
    #Honteusement dérobé à l'exam4
    #sert à générer les codes pour les débats
    import string
    import random
    alphabet = string.ascii_letters + string.digits
    
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("SELECT id_debate FROM debates")
    all_codes=cur.fetchall()
    short_code = ''.join(random.choice(alphabet) for i in range(4)) #Code du débat généré aléatoirement

    while short_code in all_codes:
        short_code = ''.join(random.choice(alphabet) for i in range(4)) #On le re-génère tant qu'il n'existe pas déjà

    return short_code

def generateJoinCode():
    #Honteusement dérobé à l'exam4
    #sert à générer les codes pour les débats
    import string
    import random
    alphabet = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(alphabet) for i in range(4))
    return short_code

def isJoinCodeValid(id_debate,join_code):
    #Vérifie qu'un code d'invitation à un débat privé est valide est valide
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("SELECT COUNT(*) FROM debates WHERE id_debate=? AND join_code=?",(id_debate,join_code))  #On vérifie que le join code est le bon
    data=cur.fetchall()
    return data[0][0]!=0    #renvoie True si le join_code existe, False sinon


def addUserToDebate(id_debate,username):
    #Ajoute un utilisateur à un débat privé. Plus précisément, ajoute un lien utilisateur-débat 
    id_user=getUserID(username)
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("INSERT INTO spaces_users(user_id,space_id) VALUES (?,?)",(id_user,id_debate)) #On crée le lien utilisateur-débat 
    con.commit()


def getDebateName(id_debate):
    #Récupère le nom/titre d'un débat à partir de son id
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("SELECT id_debate,debate_name FROM debates")  #On récupère le nom de l'débat
    data=cur.fetchall()
    for u in data:
        if id_debate == u[0]:
            return u[1]

def createDebate(debate_code,debate_title, join_code, author, description):
    #rajoute un débat dans la base de données
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("INSERT INTO debates(id_debate,debate_name,join_code,id_creator,debate_description) VALUES(?,?,?,?,?)",(debate_code,debate_title,join_code,author,description))
    con.commit()

def getUserID(username):
    # fonction permettant de récupérer l'ID d'un user à partir de son username
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id,username FROM userInfo")
    list = cursor.fetchall()
    for u in list:
        if username in u:
            return u[0]


def getUsername(id):
    # fonction permettant de récupérer l'username d'un user à partir de son id
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id,username FROM userInfo")
    list = cursor.fetchall()
    for u in list:
        if id in u:
            return u[1]


def addAudioToDB(path, username, id_debate, title):
    #Ajoute les informations d'un fichier audio d'une proposition à la base de données
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    command = "INSERT INTO messages ( path, id_sender, id_debate, message_title) VALUES (?, ?, ?, ?)"
    cursor.execute(command, ("audio_files/"+path, getUserID(username), id_debate, title))
    con.commit()
    con.close

def addAudioToDBLinked(path, username, id_debate, title, id_linked):
    #Ajoute les informations d'un fichier audio d'un message cité à la base de données
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    command = "INSERT INTO messages ( path, id_sender, id_debate, message_title, id_linked_message) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(command, ("audio_files/"+path, getUserID(username), id_debate, title, id_linked))
    con.commit()
    con.close

def addAudioToDBComment(path, username, id_debate, title, id_linked):
    #Ajoute les informations d'un fichier audio d'un commentaire à la base de données
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    command = "INSERT INTO messages ( path, id_sender, id_debate, message_title,message_type, id_linked_message) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(command, ("audio_files/"+path, getUserID(username), id_debate, title,"comment", id_linked))
    con.commit()
    con.close

def isLinked(id_proposition):
    #Vérifie si la proposition en cite une autre ou pas
    isLink = False
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_linked_message FROM messages WHERE id_message=? ",(id_proposition,))
    if cursor.fetchall()[0][0] != 0:
        isLink = True
    return isLink

def getPropName(id_proposition):
    #Récupère le nom d'une proposition avec son id
    con=sqlite3.connect("kleps.db")
    cur=con.cursor()
    cur.execute("SELECT message_title FROM messages WHERE id_message = ?", (id_proposition,))  #On récupère le nom de l'débat
    data=cur.fetchall()
    return data[0][0]

def getLinkedName(id_proposition):
    #Récupère le nom de la proposition que cite celle représenté par id_proposition
    name = 'error'
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_linked_message FROM messages WHERE id_message=?",(id_proposition,))
    id_link = cursor.fetchall()[0][0]
    if id_link != 0:
        name = getPropName(id_link)
    return name

def getLinkId(id_proposition):
    #Récupère l'id de la proposition que cite celle représenté par id_proposition
    name = 'error'
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_linked_message FROM messages WHERE id_message=?",(id_proposition,))
    return cursor.fetchall()[0][0]

def getPropositionData(id_proposition,id_debate):
    # récupération des infos nécessaires à l'affichage d'une proposition, à partir de son id et de l'id du débat
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT sent_date,path,id_sender,message_title FROM messages WHERE id_message=? AND id_debate=?",(id_proposition,id_debate))
    data = cursor.fetchall()
    if data == []:
        return ('error', 'error', 'error', 'error', 'error', 'error', 'error', id_proposition,id_debate,'error')
    else:
        linked_name='vide'
        linked_id='0'
        if isLinked(id_proposition):
            linked_name = getLinkedName(id_proposition)
            linked_id = getLinkId(id_proposition)
        sent_date,path,id_sender,message_title=data[0]
        author = getUsername(id_sender)
        cursor.execute("SELECT COUNT(*) FROM messages WHERE id_linked_message=? AND id_debate=? AND message_type='comment' ", (id_proposition,id_debate))
        comment_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM messages WHERE id_linked_message=? AND id_debate=? AND message_type='proposition' ", (id_proposition,id_debate))
        linked_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM tokens WHERE id_message=? AND id_debate=?", (id_proposition,id_debate))
        token_count = cursor.fetchall()[0][0]
        return (path, sent_date, author, message_title, comment_count, linked_count, token_count,id_proposition,id_debate,linked_name,linked_id)

def getCommentData(id_comment,id_debate):
    # récupération des infos nécessaires à l'affichage d'un commentaire, à partir de son id et de l'id du débat
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_message,sent_date,path,id_sender,message_title FROM messages")
    list = cursor.fetchall()
    if list == []:
        return ('error', 'error', 'error', 'error', id_comment)
    info = ['none', 'none', 'none', 'none', 'none']
    for i in list:
        if i[0] == id_comment:
            info = i
    path = info[2]
    date = info[1]
    title = info[4]
    author = getUsername(info[3])
    return (path, date, author, title, id_comment)

def getSortingData(id_proposition,id_debate):
    # récupération des infos nécessaires au tri des messages, à partir de son id et de l'id du débat
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT sent_date FROM messages WHERE id_message=? AND id_debate=?",(id_proposition,id_debate))
    data = cursor.fetchall()
    if data == []:
        return ('error', 'error', 'error', 'error', 'error', 'error', 'error', id_proposition,id_debate)
    else:
        sent_date=data[0]
        cursor.execute("SELECT COUNT(*) FROM messages WHERE id_linked_message=? AND id_debate=? AND message_type='comment' ", (id_proposition,id_debate))
        comment_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM messages WHERE id_linked_message=? AND id_debate=? AND message_type='proposition' ", (id_proposition,id_debate))
        linked_count = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM tokens WHERE id_message=? AND id_debate=?", (id_proposition,id_debate))
        token_count = cursor.fetchall()[0][0]
        return (sent_date, comment_count, linked_count, token_count,id_proposition,id_debate)

def getDebatePropositions(id_propositions,id_debate):
    #Récupère toutes les infos nécessaire pour l'affichage des messages caractérisé par les id de la liste id_propositions
    propositions = []
    for id in id_propositions:
        propositions.append(getPropositionData(id,id_debate))
    return propositions

def getPropositionComments(id_comments,id_debate):
    #Récupère toutes les infos nécessaire pour l'affichage des commentaires caractérisé par les id de la liste id_comments
    comments = []
    for id in id_comments:
        comments.append(getCommentData(id,id_debate))
    return comments

def sortByRecent(id_debate):
    #tri des id_message des propositions d'un débat selon leur date de parution
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_message FROM messages WHERE id_debate = ? AND message_type='proposition' ORDER BY sent_date DESC", (id_debate,))
    list = cursor.fetchall()
    if list == []:
        return list
    l = [u[0] for u in list]
    return l


def sortByRecentComments(id_proposition):
    #tri des id_message des commentaires d'une proposition selon leur date de parution
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_message FROM messages WHERE message_type = 'comment' AND id_linked_message = ? ORDER BY sent_date DESC", ( id_proposition,))
    list = cursor.fetchall()
    if list == []:
        return list
    l = [u[0] for u in list]
    return l

def DoubleQuickSort(refList, otherList): #QuickSort classique
    QuickSort0(refList,otherList,0,len(refList)-1)

def QuickSortPartition (refList,otherList, start, end):
    pivot = refList [start]
    low = start + 1
    high = end
    while True:
        while low <= high and refList [high] >= pivot:
            high = high - 1
        while low <= high and refList[low]<= pivot:
            low=low+ 1
        if low <= high:
            refList[low], refList [high] = refList [high], refList[low]
            otherList [low], otherList[high] = otherList [high], otherList [low]
        else:
            break    
    refList[start], refList [high]= refList [high], refList [start]
    otherList [start], otherList [high] = otherList [high], otherList[start]
    return high

def QuickSort0(refList,otherList, start, end):
    if start >= end:
        return
    p = QuickSortPartition ( refList,otherList, start, end)
    QuickSort0(refList, otherList, start, p-1)
    QuickSort0 (refList,otherList, p+1, end)

def difDateInHours( youngest, oldest):
    #calcul la différence en heures entre les dates youngest et oldest
    dur = (youngest - oldest)
    days, seconds = dur.days, dur.seconds
    hours = days*24 + seconds // 3600
    return hours

def sortByPopular(id_debate):
    #tri des id_message des propositions d'un débat selon leur "score" de popularité calculé par (3*jetons+2*commentaires+prop liées)/((temps en heures)^(1/2))
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_message FROM messages WHERE id_debate = ? AND message_type='proposition' ", (id_debate,))
    list = cursor.fetchall()
    if list == []:
        return list
    id = [u[0] for u in list]
    sorting_formula = []
    for i in id:
        data = getSortingData(i, id_debate)
        date1 = datetime.now()
        date2 = datetime.strptime(data[0][0], '%Y-%m-%d %H:%M:%S')
        formula = (3*data[3]+2*data[1]+data[2])/math.sqrt(1+difDateInHours(date1, date2)) #remplacer le 1 par un indicateur de temps
        sorting_formula.append(formula)
    DoubleQuickSort(id, sorting_formula)
    return id


def getAllDebatesData():
    #récupération de toutes les données nécessaires à l'affichage des débats dans l'Espace de débat
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_debate,debate_name,debate_description FROM debates")
    data=cursor.fetchall()
    info=[]
    for i in range(len(data)):
        info.append(data[i]+getDebateStats(data[i][0]))
    return info

def getDebateStats(id_debate):
    #récupère le nombre total de commentaires et jetons d'un débat
    list = sortByRecent(id_debate)
    comments,tokens = 0,0
    for i in list:
        data = getSortingData(i, id_debate)
        comments += data[1]
        tokens += data[3]
    return (comments, tokens)

def getAllDebatesStats():
    #récupère toutes les stats liées aux débats
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT id_debate FROM debates")
    debates_list = cursor.fetchall()
    stats = []
    for i in debates_list:
        stats.append(getDebateStats(i[0]))
    return stats

def getDebateTitleAndDescription(id_debate):
    #renvoie le titre et la description d'un débat
    try:
        con = sqlite3.connect("kleps.db")
        cursor = con.cursor()
        cursor.execute("SELECT debate_name,debate_description FROM debates WHERE id_debate=?",(id_debate,))
        data = cursor.fetchall()[0]
        return data
    except:
        return ('','')

def isInDebatesUsers(username,id_debate):
    #vérifie si un utilisateur a le droit de rejoindre un débat privé
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT user_id,space_id FROM spaces_users")
    list = cursor.fetchall()
    id = getUserID(username)
    if (id,id_debate) in list:
        return True
    return False

def isAdmin(username):
    #vérifie si un utilisateur est administrateur
    con = sqlite3.connect("kleps.db")
    cursor = con.cursor()
    cursor.execute("SELECT is_admin FROM userInfo WHERE username=?",(username,))
    isAdmin = cursor.fetchall()
    return isAdmin[0][0]

#======================================================================================================================
#
#                                                    Route Flask
#
#======================================================================================================================

@app.route("/")
#page d'acceuil, page principale du site
#La page s'affiche avec deux paramètres : Le message d'alerte
#Et une bool pour savoir si l'utilisateur est connecté
def index():
    if "alert_message" in session:  #Si y'a un message d'alerte quelconque
        alert_message=session["alert_message"]
        session.pop("alert_message",None) #On le supprime, pour pas avoir à le ré-afficher la prochaine fois
        return render_template("index.html",alert_message=alert_message,isLoggedIn=isLoggedIn())
        #On affiche la page avec les paramètres correspondants
    return render_template("index.html",isLoggedIn=isLoggedIn())

@app.route("/login")
#doit toujours avoir le "connexion register" dans le header, d'où le isLoggedIn="false"
def login():
    if "username" in session:
    #vérifie si l'utilisateur est connecté, sinon renvoie vers la page connexion
        session["alert_message"]="Vous êtes déjà conecté"
        return redirect(url_for("index"))
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
        return render_template('login.html',alert_message=alert_message, isLoggedIn="false")
    return render_template('login.html', isLoggedIn="false")

@app.route("/logUser", methods=["POST", "GET"])
def logUser():
#renvoie vers la page de connexion puis récupère les données récupérées
#ensuite on vérifie que les informations sont correctes puis on connecte l'utilisateur
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if isLogInfoCorrect(username, password):
            session.pop("alert_message",None)
            session.permanent = True
            session["username"] = username
            session["password"] = password
            return redirect(url_for("user"))
        session["alert_message"]="Nom d'utilisateur ou mot de passe incorrect"
        return redirect(url_for("login"))
    if "username" in session:
        return redirect(url_for("user"))
    session["alert_message"]="Erreur durant la connexion"
    return redirect(url_for("index"))

@app.route("/user")
def user():
#si connecté renvoie vers la page de confirmation
#sinon renvoie vers login pour connexion
    if "username" in session:
        session["alert_message"]="Vous êtes maintenant connecté"
        return redirect(url_for("index"))
    return redirect(url_for("login"))


@app.route("/register")
def register():
#vérifie si l'utilisateur est connecté, sinon renvoie vers la page de création de compte
#doit toujours avoir le "connexion register" dans le header, d'où le isLoggedIn="false"
    if "username" in session:
        session["alert_message"]="Vous êtes déjà connecté"
        return redirect(url_for("index"))
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
        return render_template('register.html',alert_message=alert_message, isLoggedIn="false")
    return render_template('register.html', isLoggedIn="false")


@app.route("/addUser", methods=["POST", "GET"])
#page de création de compte
def addUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        #On récupère les valeurs via un form
        if(password!=confirm_password):
            session["alert_message"]="Les mots de passes ne sont pas les mêmes"
            return redirect(url_for("register"))
        try:
            addNewUser( username, password)  #addNewUser crée un message d'alert si le mail/nom d'utilisateur existe déjà
            if "alert_message" in session :
                return redirect(url_for("register"))
            else:   #Sinon cela créé le compte, donc on informe l'utilisateur
                session["alert_message"]="Compte créé avec succès"
                return redirect(url_for("login"))
        except:
            session["alert_message"]="Erreur durant l'inscription"
            return redirect(url_for("register"))

@app.route("/logout")
def logout():
#Déconnecte l'utilisateur s'il est connecté
    if  "username" in session:
        session.pop("username", None)
        session["alert_message"]="Vous êtes maintenant déconnecté"
    else:
        session["alert_message"]="Vous n'êtes pas connecté"
    return redirect(url_for('index'))


@app.route("/debates_list")
#Page des espaces, l'utilisateur doit être connecté pour y acceder
def debates_list():
    alert_message=""
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
    debatesData = getAllDebatesData()
    #On affiche différentes version de la page en fonction du statut de l'utilisateur
    if "username" in session:
        if isAdmin(session["username"]):
            return render_template('debates_list.html', isLoggedIn=isLoggedIn(), debatesData = debatesData, alert_message=alert_message, is_admin="true")
        else:
            return render_template('debates_list.html', isLoggedIn=isLoggedIn(), debatesData = debatesData, alert_message=alert_message, is_admin="false")
    else:
        return render_template('debates_list.html', isLoggedIn=isLoggedIn(), debatesData = debatesData, alert_message=alert_message, is_admin="false")



@app.route("/about")
#Page à propos
def about():
    return render_template("about.html", isLoggedIn=isLoggedIn())

@app.route('/contact')
#Page Contact
def contact():
    return render_template('contact.html',isLoggedIn=isLoggedIn())

@app.route('/join_debate/<id_debate>/<join_code>')
#permet à un utilisateur de rejoindre un débat grâce à un code donné par l'admin
#pas implémenté
def join_debate(id_debate,join_code):
    if isJoinCodeValid(id_debate,join_code):
        try:
            username = session["username"]
            if isInDebatesUsers(username,id_debate):
                return render_template('debate_joined.html',joined_debate=getDebateName(id_debate))
            addUserToDebate(id_debate,session["username"]) #On ajoute l'utilisateur au débat
            return render_template('debate_joined.html',joined_debate=getDebateName(id_debate)) #On l'informe qu'il a bien rejoint le débat
        except:
            session["alert_message"]="Erreur lors de l'inscription au débat"
            return redirect(url_for("index"))        
    else:
        session["alert_message"]="Code Invalide"
        return redirect(url_for("index"))

@app.route('/add_debate',methods=["GET","POST"])
def add_debate():
    #permet à un administrateur de créer un débat
    if "username" in session:
        if isAdmin(session["username"]):
            if request.method=="GET":
                 #Si la requête est de type GET : on donne les champs pour créer un débat
                        return render_template('add_debate.html')    
            elif request.method=="POST":
                #Si c'est POST : On essaie de créer le débat avec les infos du form
                try:
                    debate_title=request.form["debate_message"]
                    debate_description=request.form["description"]
                    debate_code=generateDebateCode()
                    join_code=generateJoinCode()
                    creator = session["username"]
                    createDebate(debate_code,debate_title,join_code,creator,debate_description)
                    session["alert_message"] = "Débat créé avec succès"
                    return redirect(url_for("debates_list"))
                except:
                    session["alert_message"] = "Erreur lors de la création du débat"
                    return redirect(url_for("debates_list"))
        else:
            session["alert_message"] = "Vous n'êtes pas administrateur"
            return redirect(url_for("debates_list"))            
    else:          
        session["alert_message"] = "Vous n'êtes pas connecté"
        return redirect(url_for("debates_list"))

@app.route("/audioInput/<id_debate>")
#Page de l'enregistrement audio
def audioInput(id_debate):
    return render_template('audiorec.html',id_debate = id_debate, isLoggedIn=isLoggedIn())

@app.route("/getProposition/<id_debate>", methods=["POST", "GET"])
# Récupère les messages audio et les stocks dans le serveur tout en complétant la db
def getProposition(id_debate):
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        file = request.files['audio_file']
        title = request.form['title']
        if file.filename == '':
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username = session['username']
        try:
            addAudioToDB(file.filename, username, id_debate, title) 
            session["alert_message"]="Message posté avec succès"
            return redirect(url_for('debates_list'))
        except:
            session["alert_message"]="Erreur lors du processus"
            return redirect(url_for('debates_list'))

@app.route("/audioInputLinked/<id_debate>/<id_linked>")
#Page de l'enregistrement audio de propositions liées à la proposition
#caratérisée par id_linked
def audioInputLinked(id_linked,id_debate):
    return render_template('audiorec_linked.html',id_linked=id_linked,id_debate = id_debate, message = getPropositionData(int(id_linked),id_debate)[:9], isLoggedIn=isLoggedIn())

@app.route("/getMessageLinked/<id_debate>/<id_linked>", methods=["POST", "GET"])
# Récupère les messages audio liés et les stocks dans le serv tout en complétant la db
def getMessageLinked(id_debate,id_linked):
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        file = request.files['audio_file']
        title = request.form['title']
        if file.filename == '':
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username = session['username']
        try:
            addAudioToDBLinked(file.filename, username, id_debate, title, id_linked) 
            session["alert_message"]="Message posté avec succès"
            return redirect(url_for('debates_list'))
        except:
            session["alert_message"]="Erreur lors du processus"
            return redirect(url_for('debates_list'))
        
@app.route("/audioInputComment/<id_debate>/<id_linked>")
#Page de l'enregistrement audio des commentaires
def audioInputComment(id_linked,id_debate):
    return render_template('audiorec_comment.html',id_linked=id_linked,id_debate = id_debate, message = getPropositionData(int(id_linked),id_debate)[:9], isLoggedIn=isLoggedIn())

@app.route("/getMessageComment/<id_debate>/<id_linked>", methods=["POST", "GET"])
# Récupère les messages audio commentaires et les stocks dans le serv tout en complétant la db
def getMessageComment(id_debate, id_linked):
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        file = request.files['audio_file']
        title = request.form['title']
        if file.filename == '':
            flash('Pas de fichier séléctionné')
            return redirect('audioInput')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        username = session['username']
        try:
            addAudioToDBComment(file.filename, username, id_debate, title, id_linked) 
            session["alert_message"]="Commentaire posté avec succès"
            id_proposition = id_linked
            return redirect(url_for('debates_list'))
        except:
            session["alert_message"]="Erreur lors du processus"
            id_proposition = id_linked
            return redirect(url_for('debates_list'))
            

@app.route("/debate/<id_debate>")
#page affichant tous les propositions d'un débat
def debate(id_debate):
    alert_message=""
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
    id_propositions_sorted=sortByPopular(id_debate)
    (debate_title,debate_description)=getDebateTitleAndDescription(id_debate)
    return render_template("debate.html", propositions = getDebatePropositions(id_propositions_sorted,id_debate),id_debate=id_debate, isLoggedIn=isLoggedIn(), alert_message=alert_message,debate_title=debate_title,debate_description=debate_description)

@app.route("/debateRecent/<id_debate>")
#page affichant tous les propositions d'un débat
def debateRecent(id_debate):
    alert_message=""
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
    id_propositions_sorted=sortByRecent(id_debate)
    (debate_title,debate_description)=getDebateTitleAndDescription(id_debate)
    return render_template("debateRecent.html", propositions = getDebatePropositions(id_propositions_sorted,id_debate),id_debate=id_debate, isLoggedIn=isLoggedIn(), alert_message=alert_message, debate_title=debate_title,debate_description=debate_description)

@app.route("/debate/<id_debate>/<id_proposition>")
#page une proposition et les commentaires associés
def proposition(id_debate,id_proposition):
    alert_message=""
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
    id_comments_sorted = sortByRecentComments(id_proposition)
    return render_template("proposition.html", proposition = getPropositionData(int(id_proposition),id_debate),id_debate=id_debate, comments = getPropositionComments(id_comments_sorted,id_debate), isLoggedIn=isLoggedIn(),alert_message=alert_message)

@app.route("/like/<id_debate>/<id_proposition>")
#permet de donner un token à une proposition
def like(id_debate,id_proposition):
    try:
        id_user=getUserID(session["username"])
        con=sqlite3.connect("kleps.db")
        cur=con.cursor()
        cur.execute("SELECT COUNT(*) FROM tokens WHERE id_liker=? AND id_message=? AND id_debate=?",(id_user,id_proposition,id_debate))
        already_liked=cur.fetchall()[0][0]
        #Vérifier si le token existe pas déjà, et si oui, le supprimé (dislike)
        if(already_liked>=1):
            cur.execute("DELETE FROM tokens WHERE id_liker=? AND id_message=? AND id_debate=?",(id_user,id_proposition,id_debate))
            con.commit()
            session["alert_message"]="Vous avez bien enlevé votre vote !"
            return redirect(url_for('proposition',id_debate=id_debate,id_proposition=id_proposition))
        if(already_liked==0):
            cur.execute("INSERT INTO tokens(id_liker,id_message,id_debate) VALUES(?,?,?)",(id_user,id_proposition,id_debate))
            con.commit()
            session["alert_message"]="Vous avez bien voté !"
            return redirect(url_for('proposition',id_debate=id_debate,id_proposition=id_proposition))
    except:
        session["alert_message"]="Erreur lors du processus"
        return redirect(url_for('debates_list'))

@app.route("/stats/<id_user>")
#Affihce les différentes statistiques des débats créer par un administrateur
def stats(id_user):
    alert_message=""
    if "alert_message" in session:
        alert_message=session["alert_message"]
        session.pop("alert_message",None)
        return render_template("stats.html", isLoggedIn=False,alert_message=alert_message)
    else:
        try:
            id_user=getUserID(session["username"])
            con=sqlite3.connect("kleps.db")
            cur=con.cursor()
            cur.execute("SELECT is_admin FROM userInfo WHERE id=? ",(id_user,))
            already_admin=cur.fetchall()[0][0]
            if(already_admin==0):
                alert_message= "Vous n'êtes pas un admin"
                return redirect(url_for('login'))
            else:
                cur.execute("SELECT id_debate FROM debates WHERE id_creator=? ",(session["username"],))
                id_debates =cur.fetchall()
                liste=[]
                for i in id_debates:
                    liste.append(i[0])
                return render_template("stats.html",stats = getAllDebatesData(),n= len(getAllDebatesData()),id_debates=liste)
        except:
            alert_message= "Erreur lors du processus"
            
            return redirect(url_for('login'))
        
app.run()