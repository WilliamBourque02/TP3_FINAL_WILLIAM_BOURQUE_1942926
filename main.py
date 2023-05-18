# William Bourque 1942926

import codecs
import csv
import pathlib
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import sqlite3
import random
from deep_translator import GoogleTranslator
from tkinter import messagebox
from tkinter.messagebox import showinfo
import os
import sys
from functools import partial
from tkinter import messagebox as msg

#vbvb
# Mise en relation du chemin d'accès pour le dossier de travail 
#path = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD"
db = os.getcwd()
db = "C:/Users/willb\Documents/GitHub/TP3_FINAL_WILLIAM_BOURQUE_1942926/films.db"
Index = 0

# Fonction pour permettre l'utilisation de fonctions SQL ainsi que l'utilisation de
# try / except pour trouver les potentielles erreurs plus facilement
def SQLRequest(Request):
    connection=sqlite3.connect(db, timeout=10)
    cursor=connection.cursor()
    try :
        cursor.execute(Request)
    except Exception as e:
        messagebox.showerror("SQL Request",e)
        print(e)
        print(e.args[0])

    connection.commit()
    result=cursor.fetchall()
    connection.close()
    return (result)
    
# Fonction pour permettre l'utilisation des requetes SQL qui utilisent le SQL VIEW ainsi que l'utilisation de
# try / except pour trouver les potentielles erreurs plus facilement
def SQLRequestView(Request):
    db = os.getcwd()
    db = "C:/Users/willb/Documents/GitHub/TP3_FINAL_WILLIAM_BOURQUE_1942926/films.db"
    connection=sqlite3.connect(db, timeout=10)
    cursor=connection.cursor()

    CreateView='CREATE VIEW IF NOT EXISTS view AS SELECT ROW_NUMBER(),* FROM Films INNER JOIN Realisateurs on Films.RealisateurID=Realisateurs.RealisateurID'       
    try :
        cursor.execute(CreateView)
    except Exception as e:
        messagebox.showerror("SQL Request View CREATE view",e)

    try :
        cursor.execute(Request)
    except Exception as e:
        messagebox.showerror("SQL Request View",e)
        print(e)
    connection.commit()
    result=cursor.fetchall()
    connection.close()
    return result

# Fonction d'exportation exportFile() permettant de faire l'exportation du fichier de la base de données actuelle
def exportFile():
    # Permet d'accepter plusieurs formes de fichier
    type = (('text files', '*.csv'),('All files', '*.*'))
    fileText = filedialog.asksaveasfile(mode='w', defaultextension=".csv",
title='Enregistrer sous:', initialdir='./', filetypes=type)
    if fileText is None: 
        return
# Définition des champs qui seront présents lors de l'exportation
    quoteHeaders = '"Realisateur","Desc","Titre","Synopsis","Date","Mots_cles"\n'
    with open(fileText.name, 'w', newline='',encoding="utf-8") as fileName:
        fileName.write(quoteHeaders)
        for item in table:
            realisateur = item[6]
            if item[7] != None:
                desc = item[7]
                desc = desc.replace("\n"," ")
                desc = desc.replace("\r"," ")
            else:
                desc=""
            if item[1] != None:
                titre=item[1]
                titre=titre.replace("\n"," ")
                titre=titre.replace("\r"," ")
            else:
                titre=""

            if item[2] != None:
                synopsis=item[2]
                synopsis=synopsis.replace("\n"," ")
                synopsis=synopsis.replace("\r"," ")
            else:
                synopsis=""

            if item[3] != None:
                date =item[3]
            else:
                date=""
            if item[4]!= None:
                keywords=item[4]
            else:
                keywords=""


            line='"'+realisateur+'","'+desc+'","'+titre+'","'+synopsis+'","'+date+'","'+keywords+'"\n'
            fileName.write(line)

    head, tail = os.path.split(str(fileText.name))
    showinfo(title='Fichier Exporté', message=tail.upper()+" "+str(len(table))+" fichesexportées")
    Refresh()
    ReadDB(1)

# Refresh les citations lors des changement a l'écran ou des manipulations quelquonques où cela est nécessaire 
def Refresh():
    realisateur,naissance,desc,titre,date, synopsis, trailer, keywords, realisateurID = ReadDB(Index)

    ID=GetID(realisateurID, titre, synopsis)

    # Regarde si la citation est vide
    film=CheckifFilmEmpty(ID)

    # Changement de la langue de la citation
    #citation=""
    #if varLanguage.get() == "fr":
    #    citation=citation_fr
   # elif varLanguage.get() == "en":
      #  citation=citation_en

    CheckPhoto(realisateur)
    
    #synopsis = ""
    # Si la citation est trop grande, ces conditions s'occuperons d'ajuster cette dernière afin d'éviter des débordements
    if len(synopsis) > 610:
        labelSynopsis.config(font=("Arial", 12,"italic"))
        labelSynopsis.config(height="15", width= "85")
    elif len(synopsis) > 480:
        labelSynopsis.config(font=("Arial", 13,"italic"))
        labelSynopsis.config(height="15", width= "70")
    elif len(synopsis) > 200:
        labelSynopsis.config(font=("Arial", 15,"italic"))
        labelSynopsis.config(height="11", width= "56")
    else:
        labelSynopsis.config(font=("Arial", 15, "italic"))
        labelSynopsis.config(height="11", width= "56")


    # Association de valeurs aux nouvelles variables  
    # realisateur,naissance,desc,titre,date, synopsis, trailer, keywords, realisateurid = ReadDB(Index)
    varID.set(realisateurID)
    varRealisator.set(realisateur)
    varBirth.set(naissance)
    varDescription.set(desc)
    varTitle.set(titre)
    varDate.set(date)
    varSynopsis.set(synopsis)
    varTrailer.set(trailer)
    varKeyword.set(keywords)





def CheckifFilmEmpty(id):
    pass
        


# Fonction permettant de vérifier si la photo est la bonne, sinon il retourne une photo anonymous
def CheckPhoto(realisateur):
    global photo
    chemin="./photos/"
    realisateur=realisateur.replace("-","")
    realisateur=realisateur.replace(" ","")
    realisateur=realisateur.replace(".","")
    realisateur=realisateur.replace(",","")
    realisateur=realisateur.replace("é","e")
    realisateur=realisateur.replace("â","a")
    realisateur=realisateur.replace("à","a")
    realisateur=realisateur.replace("è","e")
    filelist = [file for file in os.listdir(chemin) if file.startswith(realisateur) and file.endswith((".png",".PNG",".gif",".GIF",".jpg",".JPG","jpeg",",JPEG"))]
    if len(filelist)>0:
        imgRealisator= Image.open(chemin+filelist[0])
    else:
        imgRealisator = Image.open(chemin+"anonymous.png")
    photo = imgRealisator.resize((150,150))
    photo = ImageTk.PhotoImage(photo)
    labelPhoto.config(image=photo)


# Fonction permettant de vérifier si la photo est la bonne, sinon il retourne une photo anonymous
# MÊME CHOSE POUR FICHE DE FILM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#def CheckPhoto(film):
 #   global photo
  #  chemin="./photos/"
   # film=film.replace("-","")
    #film=film.replace(" ","")
   # film=film.replace(".","")
    #film=film.replace(",","")
    #film=film.replace("é","e")
    #film=film.replace("â","a")
    #film=film.replace("à","a")
    #film=film.replace("è","e")
    #filelist = [file for file in os.listdir(chemin) if file.startswith(film) and file.endswith((".png",".PNG",".gif",".GIF",".jpg",".JPG","jpeg",",JPEG"))]
    #if len(filelist)>0:
     #   imgFilm= Image.open(chemin+filelist[0])
    #else:
     #   imgFilm = Image.open(chemin+"anonymous.png")
    #photo = imgFilm.resize((150,150))
    #photo = ImageTk.PhotoImage(photo)
    #labelPhoto.config(image=photo)    
# Fonction permettant de passer à la citation suivante
def Next():
    global Index
    Index+=1
    if Index >= len(table):
        Index= len(table)-1
    Refresh()

# Fonction permettant de retourner la citation précédente
def Previous():
    global Index
    Index-=1
    if Index >= len(table):
        Index= len(table)-1
    Refresh()

# Fonction permettant de retourner une citation au hasard
def randomFilm():
    global Index
    Index = random.randint(0, len(table))
    if Index >= len(table):
        Index= len(table)
    Refresh()


# Lit le contenu de la base de données dans une liste(table) et retourne l'information dans la présente citation dans une fonction ReadDB
# realisateur,naissance,desc,titre,date, synopsis, trailer, keywords, realisateurid = ReadDB(Index)
def ReadDB(Index):
    global table
    db = os.getcwd()
    db = "C:/Users/willb/Documents/GitHub/TP3_FINAL_WILLIAM_BOURQUE_1942926/films.db"
    table = Fetch(varFilter.get())

    # Si la table est vide, le programme va chercher le filtre
    if table==None:
        table = Fetch(varFilter.get())

        #SearchString1=SearchString.replace(';','%" OR Mots_Clés LIKE "%')
        #SearchString2=SearchString.replace(';','%" OR Realisateur LIKE "%')
        #SearchString3=SearchString.replace(';','%" OR Desc LIKE "%')
        #SearchString4=SearchString.replace(';','%" OR Titre LIKE "%')
        #SearchString5=SearchString.replace(';','%" OR Synopsis LIKE "%')
        #SearchString6=SearchString.replace(';','%" OR Date "%')
        
    Fields=table[Index]
    realisateurID=Fields[0]
    titre=Fields[1]
    synopsis=Fields[3]
    trailer=Fields[4]
    date=Fields[2]
    keywords=Fields[5]
    realisateur=Fields[7]
    naissance=Fields[8]
    desc=Fields[9]
    
 # Si le synopsis est vide, le programme s'assure que c'est bel et bien le cas
    if synopsis==None:
        synopsis=""

    return realisateur,naissance,desc,titre,date, synopsis, trailer, keywords, realisateurID


# Attribution de la valeur Filter dans la fonction SetFilter() pour filtrer dans la base de données
def SetFilter(Filter):
    global table, Index
    # Fetch le contenu de la base de données pour le filtre suivant
    table = Fetch(Filter)
    if len(table)==0:
        messagebox.showwarning("Set Filter, 'Aucun Film ne correspond à : '"+Filter)
        varFilter.set('')
        table = Fetch("")
    Index = 0
    varFilter.set(Filter)
    Refresh()

# Attribution de la valeur Filter dans la fonction SetFilterAuthor() pour filtrer dans la base de données à partir de l'auteur
def SetFilterRealisator():
    global table
    Filter=varRealisator.get()
    varFilter.set(Filter)
    SetFilter(Filter)


# Fetch le contenu de la base de données pour le filtre suivant
def Fetch(Filter=""):
    SelectedFields=[]
    if Filter=="": # si valeur par défaut, pas de sélection
         Resultat=SQLRequestView('SELECT * FROM view')
    else:
        # Construction de la requête du filtre permettant de rechercher par Mots_Clés, Realisateur, Desc, Titre, Synopsis et Date de publication du film.
        # realisateur,naissance,desc,titre,date, synopsis, trailer, keywords, realisateurid
        ListofValues=Filter.replace(',','')
        Values=ListofValues.split(' ')
        SearchString=";".join(Values)
        SearchString1=SearchString.replace(';','%" OR Mots_Clés LIKE "%')
        SearchString2=SearchString.replace(';','%" OR Realisateur LIKE "%')
        SearchString3=SearchString.replace(';','%" OR Desc LIKE "%')
        SearchString4=SearchString.replace(';','%" OR Titre LIKE "%')
        SearchString5=SearchString.replace(';','%" OR Synopsis LIKE "%')
        SearchString6=SearchString.replace(';','%" OR Date "%')
        SearchString7=SearchString.replace(';','%" OR Trailer "%')
        SearchString8=SearchString.replace(';','%" OR Naissance "%')
        Resultat=SQLRequestView('SELECT * FROM view WHERE Mots_clés LIKE "%'+SearchString1+'%" OR Realisateur LIKE "%'+SearchString2+'%" OR Desc LIKE "%'+SearchString3+'%" OR Titre LIKE "%'+SearchString4+'%" OR Synopsis LIKE "%'+SearchString5+'%" OR Date LIKE "%'+SearchString6+'%" OR Trailer LIKE "%'+SearchString7+'%"OR Naissance LIKE "%'+SearchString8+'%"')
        Index= 0

    return Resultat



# Fonction retournant le ID du film à l'intérieur de la base de données
def GetID(Realisateurid,Titre,Synopsis):
    
    if len(Titre) >0:
        result=SQLRequest('SELECT rowid from Films WHERE RealisateurID='+str(Realisateurid)+' AND Titre LIKE "%'+Titre+'%";')
    if len(Synopsis) >0:
        result=SQLRequest('SELECT rowid from Films WHERE RealisateurID='+str(Realisateurid)+' AND Synopsis LIKE "%'+Synopsis+'%";')
    if len(result)==0:
        return -1
    else:
        return result[0][0]
    

# Variable global pour déterminer le début de la seconde fenêtre (ajouter)   
global second
db = os.getcwd()
db = "C:/Users/willb/Documents/GitHub/TP3_FINAL_WILLIAM_BOURQUE_1942926/films.db"
# Cette Fonction contrôle la fenêtre pour ajouter des films dans la base de données
def addNewQuoteWindow():
    connection=sqlite3.connect(db, timeout=10)

   # Creating a second Level (avec positionnement et valeurs des nouveaux frames)
    second = Toplevel()
    second.title("Ajouter films")
    second.geometry("1000x700")

    FrameTopSecond = Frame(second,borderwidth=1,width=1000,background="orange",height=120)
    FrameTopSecond.grid(row=0,column=0,sticky="we")
    FrameTopSecond.grid_propagate(0)

    FrameInput = Frame(second,borderwidth=1,width=1000,background="black",height=600)
    FrameInput.grid(row=1,column=0,sticky="we")
    FrameInput.grid_propagate(0)

    buttonRetour = Button(FrameInput,text="Quitter", command=second.destroy)
    buttonRetour.grid(row=5,column=0,pady=550,padx=600,sticky="se")
    
    # Cette Fonction contrôle l'ajout des nouvelles citations dans la base de données
    def insertData():
        RealisateurID = " "
        Realisateur = entryInputRealisator.get()
        Naissance = entryInputBirth.get()
        Desc = entryInputDesc.get()
        Titre = entryInputTitle.get()
        Date = entryInputDate.get()
        Synopsis = entryInputSynopsis.get()
        Trailer = entryInputTrailer.get()
        Mots_clés = entryInputKeyword.get()


        sql1 = SQLRequest(f"INSERT INTO `Realisateurs`(`Realisateur`, `Naissance`,`Desc`) VALUES ('{Realisateur}', '{Naissance}','{Desc}')")
        args1 = (Realisateur, Naissance,Desc)
        print(sql1, args1)

        RealisateurID = SQLRequest(f"SELECT RealisateurID FROM Realisateurs WHERE `Realisateur` = '{Realisateur}'")
        print(RealisateurID[0][0])


        sql3 = SQLRequest(f"INSERT INTO `Films`(`RealisateurID`, `Titre`, `Date`, `Synopsis`, `Trailer`,`Mots_clés`) VALUES ('{RealisateurID[0][0]}','{Titre}','{Date}','{Synopsis}','{Trailer}','{Mots_clés}')")
        args3 = (RealisateurID[0][0], Titre, Date, Synopsis, Trailer, Mots_clés)
        print(sql3, args3)

        second.destroy()
        showUI()
        ReadDB(1)
        Refresh()
        
        
    # Tous les différents labels, bouton et entry de l'écran ajouter   
    # Positionnement ainsi que les valeurs des label, entry et du bouton save pour l'écran ajouter 
    buttonSave = Button(FrameInput,text="Save", command=insertData)
    buttonSave.grid(row=5,column=0,pady=550,padx=700,sticky="se")
    
    labelLogoAdd = Label(FrameTopSecond,text="Ajouter un film", font=("Verdana", 36,), anchor="center", background="orange", foreground="white")
    labelLogoAdd.place(x=180,y=30)

    labelInputRealisator = Label(FrameInput, text=" Realisateur :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputRealisator.place(x=180, y=30)
    labelInputBirth = Label(FrameInput, text="Naissance :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputBirth.place(x = 180, y=60)
    labelInputDesc = Label(FrameInput, text="Description :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputDesc.place(x = 180, y=90)
    labelInputTitle = Label(FrameInput, text="Titre :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputTitle.place(x = 180, y=120)
    labelInputDate = Label(FrameInput, text="Date :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputDate.place(x = 180, y=150)
    labelInputSynopsis = Label(FrameInput, text="Synopsis :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputSynopsis.place(x = 180, y=180)
    labelInputTrailer = Label(FrameInput, text="Trailer :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputTrailer.place(x = 180, y=210)
    labelInputKeyword = Label(FrameInput, text="Keywords :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputKeyword.place(x = 180, y=240)


    entryInputRealisator = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputRealisator.place(x=330, y=30)
    entryInputBirth = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputBirth.place(x=330, y=60)
    entryInputDesc = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputDesc.place(x=330, y=90)
    entryInputTitle = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputTitle.place(x=330, y=120)
    entryInputDate = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputDate.place(x=330, y=150)
    entryInputSynopsis = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputSynopsis.place(x=330, y=180)
    entryInputTrailer = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputTrailer.place(x=330, y=210)
    entryInputKeyword = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputKeyword.place(x=330, y=240)



# Variable global pour déterminer le début de la troisième fenêtre (modifier)   
global third
db = os.getcwd()
db = "C:/Users/willb/Documents/GitHub/TP3_FINAL_WILLIAM_BOURQUE_1942926/films.db"
# Cette Fonction contrôle la fenêtre de modification des citations dans la base de données
def modifyQuoteWindow():
    connection=sqlite3.connect(db, timeout=10)
    
   # Creating a third Level (avec positionnement et valeurs des nouveaux frames)
    second = Toplevel()
    second.title("Modifier film ")
    second.geometry("1000x700")

    FrameTopSecond = Frame(second,borderwidth=1,width=1000,background="orange",height=120)
    FrameTopSecond.grid(row=0,column=0,sticky="we")
    FrameTopSecond.grid_propagate(0)

    FrameInput = Frame(second,borderwidth=1,width=1000,background="black",height=600)
    FrameInput.grid(row=1,column=0,sticky="we")
    FrameInput.grid_propagate(0)

    buttonRetour = Button(FrameInput,text="Quitter", command=second.destroy)
    buttonRetour.grid(row=5,column=0,pady=550,padx=600,sticky="se")
    
    # Cette Fonction contrôle le fait de modifier une des citations dans la base de données
    def updateData():
        
        entryInputTitle.configure(textvariable=varUpdateTitle)
        entryInputDate.configure(textvariable=varUpdateDate)
        entryInputSynopsis.configure(textvariable=varUpdateSynopsis)
        entryInputTrailer.configure(textvariable=varUpdateTrailer)
        entryInputKeyword.configure(textvariable=varUpdateKeywords)

        realisateur, naissance, desc, titre, date, synopsis, trailer, keywords, realisateurID = ReadDB(Index)

        ID = GetID(realisateurID, titre, synopsis)

        titre = varUpdateTitle.get()
        date = varUpdateDate.get()
        synopsis = varUpdateSynopsis.get()
        trailer = varUpdateTrailer.get()
        keywords = varUpdateKeywords.get()


        SQLRequest(f'UPDATE Films SET Titre = "{titre}", Date = "{date}", Synopsis = "{synopsis}", Trailer = "{trailer}", Mots_clés = "{keywords}" WHERE rowid ="{ID}"')
        second.destroy()
        Next()
    
    
    # Tous les différents labels de l'écran modifier   
    # Positionnement ainsi que les valeurs des label et du bouton save pour l'écran modifier 
    buttonSave = Button(FrameInput,text="Save", command=updateData)
    buttonSave.grid(row=5,column=0,pady=550,padx=700,sticky="se")
    
    labelLogoModify = Label(FrameTopSecond,text="Modifier un film", font=("Verdana", 36), anchor="center", background="orange", foreground="white")
    labelLogoModify.place(x=180,y=30)
    labelInputTitle = Label(FrameInput, text="Titre :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputTitle.place(x=180, y=30)
    labelInputDate = Label(FrameInput, text="Date :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputDate.place(x = 180, y=90)
    labelInputSynopsis = Label(FrameInput, text="Synopsis :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputSynopsis.place(x = 180, y=150)
    labelInputTrailer = Label(FrameInput, text="Trailer :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputTrailer.place(x = 180, y=210)
    labelInputKeywords = Label(FrameInput, text="Mots clés :", font=("Verdana", 14), anchor="center", background="orange", foreground="white")
    labelInputKeywords.place(x = 180, y=270)
    

    # Assignation des valeurs de la base de données dans des variables pour les entrybox afin que le texte y soit automatiquement inscrit
    realisateur, naissance, desc, titre, date, synopsis, trailer, keywords, realisateurID = ReadDB(Index)
    #ID = GetID(AuteurID, Citation_fr, Citation_en)
    
    varUpdateTitle.set(titre)
    varUpdateDate.set(date)
    varUpdateSynopsis.set(synopsis)
    varUpdateTrailer.set(trailer)
    varUpdateKeywords.set(keywords)
    
    
    # Positionnement ainsi que les valeurs des entrybox pour l'écran modifier 
    entryInputTitle = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateTitle)
    entryInputTitle.place(x=330, y=30)
    entryInputDate = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateDate)
    entryInputDate.place(x=330, y=90)

    entryInputSynopsis = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateSynopsis)
    entryInputSynopsis.place(x=330, y=150)

    entryInputTrailer = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateTrailer)
    entryInputTrailer.place(x=330, y=210)

    entryInputKeyword = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateKeywords)
    entryInputKeyword.place(x=330, y=270)


# Cette Fonction contrôle le fait de delete une des citations dans la base de données
def deleteQuote():

    Auteur, Desc, Titre, Date, Synopsis, Trailer, Keywords, RealisateurID, = ReadDB(Index)

    ID = GetID(RealisateurID, Titre, Synopsis)

    WarningBoxDelete = messagebox.askquestion(title="warning", message="Delete ?")

    # Si on répond oui à la warning box
    if WarningBoxDelete == "yes":
        SQLRequest(f"DELETE FROM Films WHERE rowid = '{ID}'")
        keywordTextInput.delete(0, END)
        Next()
        Refresh() # refresh the window with new records

# sinon on continu
    else:
        pass

# Affichage par la fonction showUI() des différents widgets et leurs dispositions sur l'écran principal (Boutons, Étiquettes, etc...)
def showUI():

    # Radiobuttons de langues
    buttonFr.grid(row=0,column=0,sticky="w",pady=5,padx=5)
    buttonEn.place(x=120,y=5)

    # Entry et button pour le filtre
    keywordTextInput.place(x=65,y=38)
    buttonKeyword.place(x=200,y=38)

    # Boutons (Next, Previous et Generate(Random))
    buttonNext.grid(row=0,column=3,sticky="s")
    buttonPrevious.grid(row=0,column=1,sticky="s")
    buttonGenerate.grid(row=0,column=2,sticky="s")

    # Boutons qui jouent avec la base de données
    buttonAdd.grid(row=2,column=0,pady=10,padx=3,sticky="w")
    buttonModify.grid(row=2,column=0,pady=10,padx=38,sticky="w")
    buttonDelete.grid(row=2,column=0,pady=10,padx=90,sticky="w")
    buttonExport.grid(row=2,column=0,pady=10,padx=135,sticky="w")
    #buttonImport.grid(row=2,column=0,pady=10,padx=182,sticky="w")

    # Tous les différents labels de l'écran principal    
    labelKeyword.grid(row=1,column=0,sticky="w",padx=5)
    labelID.grid(row=0,column=0,padx=150)
    labelTitle.place(x=180,y=30)
    labelSynopsis.place(x=180,y=60)
    labelTrailer.place(x=245,y=350)
    labelRealisator.place(x=45,y=210)
    labelDescription.place(x=10,y=250)
    labelDate.place(x=580,y=30)
    labelPhoto.place(x=11,y=50)
    labelKeywordQuote.place(x=305,y=420)
    labelLogo.place(x=500,y=5)
    labelBirth.place(x=10,y=450)

# Affichage de l'écran principal et les options qui entourent cet affichage
root=Tk()
root.title("Films de William")
logoQuotes =Image.open("QuotesLogo.png")
logoQuotes = ImageTk.PhotoImage(logoQuotes)
root.geometry("1000x1000")
root.resizable(width=False,height=False)
root.configure(background='black')

# Définition de toutes les variables pour une citation dans la base de données
# Variables principales
varID = StringVar()
varRealisator = StringVar()
varBirth = StringVar()
varDescription = StringVar()
varTitle = StringVar()
varDate = StringVar()
varSynopsis = StringVar()
varTrailer = StringVar()
varKeyword = StringVar()
varFilter = StringVar()

# Nouvelles Variables pour la fonction Import
#varImportAuthor = StringVar()
#varImportDescription = StringVar()
#varImportCit_fr = StringVar()
#varImportCit_en = StringVar()
#varImportKeywords = StringVar()
#varImportSource = StringVar()

# Nouvelles Variables pour la fonction update
varUpdateTitle = StringVar()
varUpdateDate = StringVar()
varUpdateSynopsis = StringVar()
varUpdateTrailer = StringVar()
varUpdateKeywords = StringVar()


# Définition des différents frames présents dans l'écran principal
FrameTop = Frame(root,borderwidth=1,width=1000,background="orange",height=120)
FrameQuote = Frame(root,borderwidth=1,height=600,background="black",width=1000)
FrameButton = Frame(root,borderwidth=1,height=25,width=1000, background="black")
FrameTop.grid(row=0,column=0,sticky="we")
FrameTop.grid_propagate(0)
FrameQuote.grid(row=2,column=0, pady=10)
FrameQuote.grid_propagate(0)
FrameButton.grid(row=1,column=0,sticky="s")
FrameButton.grid_propagate(0)

# Radio Button pour sélectionner la langue de la citation
buttonFr = Radiobutton(FrameTop, text="William Bourque",value="fr",command=partial(Refresh))
buttonEn = Radiobutton(FrameTop,text="1942926", value="en",command=partial(Refresh))

# Entry pour que l'utilisateur y inscrit ses mots clées
keywordTextInput = Entry(FrameTop,textvariable=varFilter, x = 100)

# Définitions des Différents boutons de l'écran principal ainsi que leurs associations à leurs fonctions respectives
buttonNext = Button(FrameButton,text="Next",padx=50,command=partial(Next))
buttonPrevious = Button(FrameButton,text="Previous",padx=50,command=partial(Previous))
buttonGenerate = Button(FrameButton,text="Generate",padx=50,command=partial(randomFilm))
buttonAdd = Button(FrameTop,text="Add", command=partial(addNewQuoteWindow))
buttonModify = Button(FrameTop,text="Modify",command=partial(modifyQuoteWindow))
buttonDelete = Button(FrameTop,text="Delete", command=partial(deleteQuote))
buttonExport = Button(FrameTop, text="Export",command=partial(exportFile))
#buttonImport = Button(FrameTop,text="Import", command=partial(importFile))
buttonKeyword = Button(FrameTop,text="Filtrer", padx= -100,command=partial(Refresh))



#Définition des labels de l'écran principal où la plupart des options cocernant leurs affichages y sont situées

labelID = Label(FrameButton,text="ID du réalisateur", textvariable=varID)

labelSynopsis = Label(FrameQuote,text="synopsis",textvariable=varSynopsis,height=20,width=80,wraplength=650)

labelTrailer = Label(FrameQuote,text="trailer",textvariable=varTrailer,wraplength=650,height=3,width=80)

labelRealisator = Label(FrameQuote,text="réalisateur",textvariable=varRealisator)

labelTitle = Label(FrameQuote,text="titre",textvariable=varTitle, wraplength=500, height=1,width=55)

labelDescription = Label(FrameQuote,text="Description",textvariable=varDescription,wraplength=150,height=11,width=20)

labelPhoto = Label(FrameQuote,height=150,width=150)

labelLogo= Label(FrameTop, text="Films de Will", font=("Verdana", 48,), anchor="center", background="orange", foreground="white")


#    labelLogoAdd.place(x=180,y=30)

labelKeyword = Label(FrameTop,text="Mot(s) :")

labelKeywordQuote = Label(FrameQuote,text="Mot Clé du film",textvariable=varKeyword,wraplength=500,height=3,width=60)

labelDate = Label(FrameQuote,text="date",textvariable=varDate, wraplength=500, height=1,width=39)

labelBirth = Label(FrameQuote, text="Naissance", textvariable=varBirth, wraplength=500, height=3,width=20)

# Répétition des fonctions importantes au bon déroulement du programme 
ReadDB(0)
Refresh()
showUI()
root.mainloop()

#test