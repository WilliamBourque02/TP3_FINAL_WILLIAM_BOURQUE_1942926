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
db = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD/quotes.db"
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
    db = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD/quotes.db"
    connection=sqlite3.connect(db, timeout=10)
    cursor=connection.cursor()

    CreateView='CREATE VIEW IF NOT EXISTS view AS SELECT ROW_NUMBER(),* FROM Citations INNER JOIN Auteurs on Citations.AuteurID=Auteurs.AuteurID'       
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
    quoteHeaders = '"Auteur","Desc","Citation_en","Citation_fr","Source","Mots_cles"\n'
    with open(fileText.name, 'w', newline='',encoding="utf-8") as fileName:
        fileName.write(quoteHeaders)
        for item in table:
            auteur = item[6]
            if item[7] != None:
                desc = item[7]
                desc = desc.replace("\n"," ")
                desc = desc.replace("\r"," ")
            else:
                desc=""
            if item[1] != None:
                citation_fr=item[1]
                citation_fr=citation_fr.replace("\n"," ")
                citation_fr=citation_fr.replace("\r"," ")
            else:
                citation_fr=""

            if item[2] != None:
                citation_en=item[2]
                citation_en=citation_en.replace("\n"," ")
                citation_en=citation_en.replace("\r"," ")
            else:
                citation_en=""

            if item[3] != None:
                source =item[3]
            else:
                source=""
            if item[4]!= None:
                keywords=item[4]
            else:
                keywords=""


            line='"'+auteur+'","'+desc+'","'+citation_fr+'","'+citation_en+'","'+source+'","'+keywords+'"\n'
            fileName.write(line)

    head, tail = os.path.split(str(fileText.name))
    showinfo(title='Fichier Exporté', message=tail.upper()+" "+str(len(table))+" citationsexportées")
    Refresh()

# Fonction d'importation importFile() permettant de faire l'importation d'un fichier d'une base de donnée
def importFile():
    fileText = filedialog.askopenfile(mode='r', defaultextension=".csv",title='Ouvrir :', initialdir='./')
    #code = ['ISO-8859-1', 'utf-8']
    with open(fileText.name, 'w', newline='',encoding="ISO-8859-1") as fileCSV:
        fileCSV = list(csv.reader(fileCSV, delimiter=";"))
        print(fileCSV[0])
        if fileCSV[0] == ["Auteur"]:
            fileCSV.pop(0)
            for champ in fileCSV:
                varImportAuthor.set(champ[0])
                varImportDescription.set(champ[1])
                varImportCit_fr.set(champ[2])
                varImportCit_en.set(champ[3])
                varImportSource.set(champ[4])
                varImportSource.set(champ[5])
                Refresh()
                ReadDB(1)

        else:  
            showinfo(title='erreur', message= "mauvais entête")
            #Refresh()
    return champ [0,1,2,3,4,5]


# Refresh les citations lors des changement a l'écran ou des manipulations quelquonques où cela est nécessaire 
def Refresh():
    auteur,desc,citation_fr,citation_en,source,keywords,auteurid = ReadDB(Index)

    ID=GetID(auteurid,citation_fr,citation_en)

    # Regarde si la citation est vide
    citation=CheckifQuoteEmpty(ID)

    # Changement de la langue de la citation
    citation=""
    if varLanguage.get() == "fr":
        citation=citation_fr
    elif varLanguage.get() == "en":
        citation=citation_en

    CheckPhoto(auteur)
    
    # Si la citation est trop grande, ces conditions s'occuperons d'ajuster cette dernière afin d'éviter des débordements
    if len(citation) > 610:
        labelQuote.config(font=("Arial", 12,"italic"))
        labelQuote.config(height="15", width= "85")
    elif len(citation) > 480:
        labelQuote.config(font=("Arial", 13,"italic"))
        labelQuote.config(height="15", width= "70")
    elif len(citation) > 200:
        labelQuote.config(font=("Arial", 15,"italic"))
        labelQuote.config(height="11", width= "56")
    else:
        labelQuote.config(font=("Arial", 15, "italic"))
        labelQuote.config(height="11", width= "56")


    # Association de valeurs aux nouvelles variables  
    varID.set(auteurid)
    varQuote.set(citation)
    varAuthor.set(auteur)
    varDescription.set(desc)
    varSource.set(source)
    varKeyword.set(keywords)





def CheckifQuoteEmpty(id):
    pass
        


# Fonction permettant de vérifier si la photo est la bonne, sinon il retourne une photo anonymous
def CheckPhoto(auteur):
    global photo
    chemin="./photos/"
    auteur=auteur.replace("-","")
    auteur=auteur.replace(" ","")
    auteur=auteur.replace(".","")
    auteur=auteur.replace(",","")
    auteur=auteur.replace("é","e")
    auteur=auteur.replace("â","a")
    auteur=auteur.replace("à","a")
    auteur=auteur.replace("è","e")
    filelist = [file for file in os.listdir(chemin) if file.startswith(auteur) and file.endswith((".png",".PNG",".gif",".GIF",".jpg",".JPG","jpeg",",JPEG"))]
    if len(filelist)>0:
        imgAuthor= Image.open(chemin+filelist[0])
    else:
        imgAuthor = Image.open(chemin+"anonymous.png")
    photo = imgAuthor.resize((150,150))
    photo = ImageTk.PhotoImage(photo)
    labelPhoto.config(image=photo)
    
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
def randomQuote():
    global Index
    Index = random.randint(0, len(table))
    if Index >= len(table):
        Index= len(table)
    Refresh()


# Lit le contenu de la base de données dans une liste(table) et retourne l'information dans la présente citation dans une fonction ReadDB
def ReadDB(Index):
    global table
    db = os.getcwd()
    db = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD/quotes.db"
    table = Fetch(varFilter.get())

    # Si la table est vide, le programme va chercher le filtre
    if table==None:
        table = Fetch(varFilter.get())
        
    Fields=table[Index]
    auteurID=Fields[0]
    citation_fr=Fields[1]
    citation_en=Fields[2]
    source=Fields[3]
    keywords=Fields[4]
    auteur=Fields[6]
    desc=Fields[7]
 # Si la citation_fr est vide, le programme s'assure que c'est bel et bien le cas
    if citation_fr==None:
        citation_fr=""
# Si la citation_en est vide, le programme s'assure que c'est bel et bien le cas
    if citation_en==None:
        citation_en=""
  
    return auteur, desc, citation_fr, citation_en, source, keywords, auteurID


# Attribution de la valeur Filter dans la fonction SetFilter() pour filtrer dans la base de données
def SetFilter(Filter):
    global table, Index
    # Fetch le contenu de la base de données pour le filtre suivant
    table = Fetch(Filter)
    if len(table)==0:
        messagebox.showwarning("Set Filter, 'Aucune citation ne correspond à : '"+Filter)
        varFilter.set('')
        table = Fetch("")
    Index = 0
    varFilter.set(Filter)
    Refresh()

# Attribution de la valeur Filter dans la fonction SetFilterAuthor() pour filtrer dans la base de données à partir de l'auteur
def SetFilterAuthor():
    global table
    Filter=varAuthor.get()
    varFilter.set(Filter)
    SetFilter(Filter)


# Fetch le contenu de la base de données pour le filtre suivant
def Fetch(Filter=""):
    #SelectedFields=[]
    if Filter=="": # si valeur par défaut, pas de sélection
         Resultat=SQLRequestView('SELECT * FROM view')
    else:
        # Construction de la requête du filtre permettant de rechercher par tous les champs de la base de données
        ListofValues=Filter.replace(',','')
        Values=ListofValues.split(' ')
        SearchString=";".join(Values)
        SearchString1=SearchString.replace(';','%" OR Mots_Clés LIKE "%')
        SearchString2=SearchString.replace(';','%" OR Auteur LIKE "%')
        SearchString3=SearchString.replace(';','%" OR Desc LIKE "%')
        SearchString4=SearchString.replace(';','%" OR Source LIKE "%')
        SearchString5=SearchString.replace(';','%" OR Citation_fr LIKE "%')
        SearchString6=SearchString.replace(';','%" OR Citation_en LIKE "%')
        Resultat=SQLRequestView('SELECT * FROM view WHERE Mots_clés LIKE "%'+SearchString1+'%" OR Auteur LIKE "%'+SearchString2+'%" OR Desc LIKE "%'+SearchString3+'%" OR Source LIKE "%'+SearchString4+'%" OR Citation_fr LIKE "%'+SearchString5+'%" OR Citation_en LIKE "%'+SearchString6+'%"')
        #Index= 0

    return Resultat



# Fonction retournant le ID de la citation à l'intérieur de la base de données
def GetID(auteurid,citation_fr,citation_en):
    
    if len(citation_fr) >0:
        result=SQLRequest('SELECT rowid from Citations WHERE AuteurID='+str(auteurid)+' AND Citation_fr LIKE "%'+citation_fr+'%";')
    if len(citation_en) >0:
        result=SQLRequest('SELECT rowid from Citations WHERE AuteurID='+str(auteurid)+' AND Citation_en LIKE "%'+citation_en+'%";')
    if len(result)==0:
        return -1
    else:
        return result[0][0]
    

# Variable global pour déterminer le début de la seconde fenêtre (ajouter)   
global second
db = os.getcwd()
db = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD/quotes.db"
# Cette Fonction contrôle la fenêtre pour ajouter des citations dans la base de données
def addNewQuoteWindow():
    connection=sqlite3.connect(db, timeout=10)

   # Creating a second Level (avec positionnement et valeurs des nouveaux frames)
    second = Toplevel()
    second.title("Ajouter citations")
    second.geometry("1000x700")

    FrameTopSecond = Frame(second,borderwidth=1,width=1000,background="blue",height=120)
    FrameTopSecond.grid(row=0,column=0,sticky="we")
    FrameTopSecond.grid_propagate(0)

    FrameInput = Frame(second,borderwidth=1,width=1000,background="black",height=600)
    FrameInput.grid(row=1,column=0,sticky="we")
    FrameInput.grid_propagate(0)

    buttonRetour = Button(FrameInput,text="Quitter", command=second.destroy)
    buttonRetour.grid(row=5,column=0,pady=550,padx=600,sticky="se")
    
    # Cette Fonction contrôle l'ajout des nouvelles citations dans la base de données
    def insertData():
        AuteurID = " "
        Auteur = entryInputAuthor.get()
        Desc = entryInputDesc.get()
        Citation_fr = entryInputCit_fr.get()
        Citation_en = entryInputCit_en.get()
        Source = entryInputSource.get()
        Mots_clés = entryInputKeyword.get()


        sql1 = SQLRequest(f"INSERT INTO `Auteurs`(`Auteur`, `Desc`) VALUES ('{Auteur}','{Desc}')")
        args1 = (Auteur, Desc)
        print(sql1, args1)

        AuteurID = SQLRequest(f"SELECT AuteurID FROM Auteurs WHERE `Auteur` = '{Auteur}'")
        print(AuteurID[0][0])


        sql3 = SQLRequest(f"INSERT INTO `Citations`(`AuteurID`, `Citation_fr`, `Citation_en`, `Source`, `Mots_clés`) VALUES ('{AuteurID[0][0]}','{Citation_fr}','{Citation_en}','{Source}','{Mots_clés}')")
        args3 = (AuteurID[0][0], Citation_fr, Citation_en, Source, Mots_clés)
        print(sql3, args3)

        second.destroy()
        showUI()
        ReadDB(1)
        Refresh()
        
        
    # Tous les différents labels, bouton et entry de l'écran modifier   
    # Positionnement ainsi que les valeurs des label, entry et du bouton save pour l'écran ajouter 
    buttonSave = Button(FrameInput,text="Save", command=insertData)
    buttonSave.grid(row=5,column=0,pady=550,padx=700,sticky="se")
    
    labelLogoAdd = Label(FrameTopSecond,text="Ajouter une citation", font=("Verdana", 36), anchor="center", background="blue", foreground="white")
    labelLogoAdd.place(x=180,y=30)

    labelInputAuthor = Label(FrameInput, text="Auteur Nom :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputAuthor.place(x=180, y=30)
    labelInputDesc = Label(FrameInput, text="Description :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputDesc.place(x = 180, y=90)
    labelInputCit_fr = Label(FrameInput, text="Citation_fr :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputCit_fr.place(x = 180, y=150)
    labelInputCit_en = Label(FrameInput, text="Citation_en :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputCit_en.place(x = 180, y=210)
    labelInputSource = Label(FrameInput, text="Les Sources :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputSource.place(x = 180, y=270)
    labelInputKeyword = Label(FrameInput, text="Keywords :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputKeyword.place(x = 180, y=330)

    entryInputAuthor = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputAuthor.place(x=330, y=30)

    entryInputDesc = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputDesc.place(x=330, y=90)

    entryInputCit_fr = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputCit_fr.place(x=330, y=150)

    entryInputCit_en = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputCit_en.place(x=330, y=210)

    entryInputSource = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputSource.place(x=330, y=270)

    entryInputKeyword = Entry(FrameInput, font=('verdana',12), width=60)
    entryInputKeyword.place(x=330, y=330)



# Variable global pour déterminer le début de la troisième fenêtre (modifier)   
global third
db = os.getcwd()
db = "C:/Users/willb/Documents/GitHub/TP2_Native_WilliamBourque_GOOD/quotes.db"
# Cette Fonction contrôle la fenêtre de modification des citations dans la base de données
def modifyQuoteWindow():
    connection=sqlite3.connect(db, timeout=10)
    
   # Creating a third Level (avec positionnement et valeurs des nouveaux frames)
    second = Toplevel()
    second.title("Modifier citations")
    second.geometry("1000x700")

    FrameTopSecond = Frame(second,borderwidth=1,width=1000,background="blue",height=120)
    FrameTopSecond.grid(row=0,column=0,sticky="we")
    FrameTopSecond.grid_propagate(0)

    FrameInput = Frame(second,borderwidth=1,width=1000,background="black",height=600)
    FrameInput.grid(row=1,column=0,sticky="we")
    FrameInput.grid_propagate(0)

    buttonRetour = Button(FrameInput,text="Quitter", command=second.destroy)
    buttonRetour.grid(row=5,column=0,pady=550,padx=600,sticky="se")
    
    # Cette Fonction contrôle le fait de modifier une des citations dans la base de données
    def updateData():
        
        entryInputCit_fr.configure(textvariable=varUpdateCit_fr)
        entryInputCit_en.configure(textvariable=varUpdateCit_en)
        entryInputKeyword.configure(textvariable=varUpdateKeywords)
        entryInputSource.configure(textvariable=varUpdateSource)

        Auteur, Desc, Citation_fr, Citation_en, Source, Mots_clés, AuteurID, = ReadDB(Index)

        ID = GetID(AuteurID, Citation_fr, Citation_en)

        Citation_fr = varUpdateCit_fr.get()
        Citation_en = varUpdateCit_en.get()
        Source = varUpdateSource.get()
        Mots_clés = varUpdateKeywords.get()


        SQLRequest(f'UPDATE Citations SET Citation_fr = "{Citation_fr}", Citation_en = "{Citation_en}", Source = "{Source}", Mots_clés = "{Mots_clés}" WHERE rowid ="{ID}"')
        second.destroy()
        Next()
    
    
    # Tous les différents labels de l'écran modifier   
    # Positionnement ainsi que les valeurs des label et du bouton save pour l'écran modifier 
    buttonSave = Button(FrameInput,text="Save", command=updateData)
    buttonSave.grid(row=5,column=0,pady=550,padx=700,sticky="se")
    
    labelLogoModify = Label(FrameTopSecond,text="Modifier une citation", font=("Verdana", 36), anchor="center", background="blue", foreground="white")
    labelLogoModify.place(x=180,y=30)
    labelInputAuthor = Label(FrameInput, text="(Désactivé) :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputAuthor.place(x=180, y=30)
    labelInputDesc = Label(FrameInput, text="(Désactivé) :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputDesc.place(x = 180, y=90)
    labelInputCit_fr = Label(FrameInput, text="Citation_fr :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputCit_fr.place(x = 180, y=150)
    labelInputCit_en = Label(FrameInput, text="Citation_en :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputCit_en.place(x = 180, y=210)
    labelInputSource = Label(FrameInput, text="Les Sources :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputSource.place(x = 180, y=270)
    labelInputKeyword = Label(FrameInput, text="Keywords :", font=("Verdana", 14), anchor="center", background="blue", foreground="white")
    labelInputKeyword.place(x = 180, y=330)

    # Assignation des valeurs de la base de données dans des variables pour les entrybox afin que le texte y soit automatiquement inscrit
    Auteur, Desc, Citation_fr, Citation_en, Source, Keywords, AuteurID, = ReadDB(Index)
    ID = GetID(AuteurID, Citation_fr, Citation_en)
    
    varUpdateCit_fr.set(Citation_fr)
    varUpdateCit_en.set(Citation_en)
    varUpdateKeywords.set(Keywords)
    varUpdateSource.set(Source)
    
    # Positionnement ainsi que les valeurs des entrybox pour l'écran modifier 
    entryInputAuthor = Entry(FrameInput, font=('verdana',12), width=60, state=DISABLED)
    entryInputAuthor.place(x=330, y=30)
    entryInputDesc = Entry(FrameInput, font=('verdana',12), width=60, state=DISABLED)
    entryInputDesc.place(x=330, y=90)

    entryInputCit_fr = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateCit_fr)
    entryInputCit_fr.place(x=330, y=150)

    entryInputCit_en = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateCit_en)
    entryInputCit_en.place(x=330, y=210)

    entryInputSource = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateSource)
    entryInputSource.place(x=330, y=270)

    entryInputKeyword = Entry(FrameInput, font=('verdana',12), width=60, textvariable=varUpdateKeywords)
    entryInputKeyword.place(x=330, y=330)


# Define a function to clear the Entry Widget Content



# Cette Fonction contrôle le fait de delete une des citations dans la base de données
def deleteQuote():

    Auteur, Desc, Citation_fr, Citation_en, Source, Keywords, AuteurID, = ReadDB(Index)

    ID = GetID(AuteurID, Citation_fr, Citation_en)

    WarningBoxDelete = messagebox.askquestion(title="warning", message="Delete ?")

    # Si on répond oui à la warning box
    if WarningBoxDelete == "yes":
        SQLRequest(f"DELETE FROM Citations WHERE rowid = '{ID}'")
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
    buttonEn.place(x=75,y=5)

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
    buttonImport.grid(row=2,column=0,pady=10,padx=182,sticky="w")

    # Tous les différents labels de l'écran principal    
    labelKeyword.grid(row=1,column=0,sticky="w",padx=5)
    labelID.grid(row=0,column=0,padx=150)
    labelQuote.place(x=180,y=30)
    labelSource.place(x=245,y=320)
    labelAuthor.place(x=45,y=210)
    labelDescription.place(x=10,y=250)
    labelPhoto.place(x=11,y=50)
    labelKeywordQuote.place(x=305,y=380)
    labelLogo.place(x=500,y=5)

# Affichage de l'écran principal et les options qui entourent cet affichage
root=Tk()
root.title("Citations")
logoQuotes =Image.open("QuotesLogo.png")
logoQuotes = ImageTk.PhotoImage(logoQuotes)
root.geometry("1000x700")
root.resizable(width=False,height=False)
root.configure(background='black')

# Définition de toutes les variables pour une citation dans la base de données
# Variables principales
varID = StringVar()
varAuthor = StringVar()
varQuote = StringVar()
varSource = StringVar()
varDescription = StringVar()
varKeyword = StringVar()
varLanguage = StringVar()
varLanguage.set("fr")
varFilter = StringVar()

# Nouvelles Variables pour la fonction Import
varImportAuthor = StringVar()
varImportDescription = StringVar()
varImportCit_fr = StringVar()
varImportCit_en = StringVar()
varImportKeywords = StringVar()
varImportSource = StringVar()

# Nouvelles Variables pour la fonction update
varUpdateCit_fr = StringVar()
varUpdateCit_en = StringVar()
varUpdateKeywords = StringVar()
varUpdateSource = StringVar()

# Définition des différents frames présents dans l'écran principal
FrameTop = Frame(root,borderwidth=1,width=1000,background="blue",height=120)
FrameQuote = Frame(root,borderwidth=1,height=600,background="black",width=1000)
FrameButton = Frame(root,borderwidth=1,height=25,width=1000, background="black")
FrameTop.grid(row=0,column=0,sticky="we")
FrameTop.grid_propagate(0)
FrameQuote.grid(row=2,column=0, pady=10)
FrameQuote.grid_propagate(0)
FrameButton.grid(row=1,column=0,sticky="s")
FrameButton.grid_propagate(0)

# Radio Button pour sélectionner la langue de la citation
buttonFr = Radiobutton(FrameTop, text="Français",value="fr",variable=varLanguage,command=partial(Refresh))
buttonEn = Radiobutton(FrameTop,text="English", value="en",variable=varLanguage,command=partial(Refresh))

# Entry pour que l'utilisateur y inscrit ses mots clées
keywordTextInput = Entry(FrameTop,textvariable=varFilter, x = 100)

# Définitions des Différents boutons de l'écran principal ainsi que leurs associations à leurs fonctions respectives
buttonNext = Button(FrameButton,text="Next",padx=50,command=partial(Next))
buttonPrevious = Button(FrameButton,text="Previous",padx=50,command=partial(Previous))
buttonGenerate = Button(FrameButton,text="Generate",padx=50,command=partial(randomQuote))
buttonAdd = Button(FrameTop,text="Add", command=partial(addNewQuoteWindow))
buttonModify = Button(FrameTop,text="Modify",command=partial(modifyQuoteWindow))
buttonDelete = Button(FrameTop,text="Delete", command=partial(deleteQuote))
buttonExport = Button(FrameTop, text="Export",command=partial(exportFile))
buttonImport = Button(FrameTop,text="Import", command=partial(importFile))
buttonKeyword = Button(FrameTop,text="Filtrer", padx= -100,command=partial(Refresh))

#Définition des labels de l'écran principal où la plupart des options cocernant leurs affichages y sont situées
labelID = Label(FrameButton,text="ID de l'auteur", textvariable=varID)
labelKeyword = Label(FrameTop,text="Mot(s) :")
labelKeywordQuote = Label(FrameQuote,text="Mot Clé de la citation",textvariable=varKeyword,wraplength=500,height=3,width=60)
labelQuote = Label(FrameQuote,textvariable=varQuote,height=20,width=80,wraplength=650)
labelSource = Label(FrameQuote,text="source",textvariable=varSource,wraplength=650,height=3,width=80)
labelAuthor = Label(FrameQuote,text="auteur",textvariable=varAuthor)
labelDescription = Label(FrameQuote,text="Description",textvariable=varDescription,wraplength=150,height=11,width=20)
labelPhoto = Label(FrameQuote,height=150,width=150)
labelLogo= Label(FrameTop,image=logoQuotes)

# Répétition des fonctions importantes au bon déroulement du programme 
ReadDB(1)
Refresh()
showUI()
root.mainloop()