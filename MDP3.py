#!/usr/bin/env python3

#Fin du programme à la ligne 365 

#Les modules importés
import sys
import os
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno
import string
from random import randint, choice
from tkinter import *
import pygame
import webbrowser
from hashlib import sha256
import pathlib
import tkinter.filedialog
from cryptography.fernet import Fernet
from hashlib import sha256
from base64 import urlsafe_b64encode



#le démarage
print("Démarage | Bienvenue !")
print("Bonjour ! Toi tu as besoin d'un nouveau mot de passe !")
print("   ****************   ")
print("C'est simple : copie le mot de passe et c'est bon !")
print("Tu peux même l'enregistrer et le retrouver dans le fichier passwords_crypt.txt ! Mais tu ne peut pas l'ouvrir : Il est chiffré !")
print("   *****************   ")

#La fenêtre 
mdp_ver = "2.0"
mdp_release_date = "JJ.MM.2021"
isInDevVersion = True
isInDevVersionText = " | InDev"

"""
La boite de dialogue
""" 
def getConfigDir(appName=''):
    """
    Retourne le dossier de configuration.
    Si le paramètre appName n'est pas vide, on crée un sous-dossier.
    Emplacement par défaut :
        linux : ~/.config
        macOS : ~/Library/Preference
        windows : C:/Users/<USER>/AppData/Roaming
    """
    # on démarre dans le dossier de l'utilisateur (home) :
    configDir = pathlib.Path.home()
    # la suite dépend de l'OS :
    platform = sys.platform
    if platform.startswith('linux'):
        configDir = configDir / '.config'
    elif platform.startswith('win'):
        configDir = configDir / 'AppData/Roaming'
    elif platform.startswith('darwin'):
        configDir = configDir / 'Library/Preferences'
    # si on a passé une valeur à "appName",
    # on crée un sous-dossier :
    if (appName != ''):
        configDir = configDir / appName
        configDir.mkdir(parents=True, exist_ok=True)
    # un print pour vérifier et on renvoie "configDir" :
    print(configDir)
    return configDir

def getAppFileDir(configFile=''):
    """
    Ouvre le fichier "configFile" 
    et y lit l'emplacement du dossier "appFileDir".
    Dans cet exemple "configFile" est un fichier texte ("config.txt")
    et contient une seule ligne.
    Pour un truc plus complet on pourrait utiliser un fichier json.
    """
    # par défaut on sélectionne le home (dossier utilisateur) :
    appFileDir = pathlib.Path.home()
    # on ouvre le fichier "configFile" 
    # et on lit la première ligne :
    if configFile.exists():
        with configFile.open() as f:
            line = f.readline()
            # on vire les éventuels sauts de lignes :
            line = line.replace('\n', '').replace('\r', '').replace('\t', '')
            if line != '':
                appFileDir = pathlib.Path(line)
            # on teste si le dossier est accessible en écriture 
            # (sinon on remet le home) :
            if not(os.access(appFileDir, os.W_OK)):
                appFileDir = pathlib.Path.home()
    # un print pour vérifier et on renvoie "appFileDir" :
    #print(appFileDir)
    return appFileDir



"""
Variables globales du programme.
    * APP_NAME : le nom du programme et donc du dossier à créer pour la configuration.
        À adapter au vrai nom du logiciel
    * CONFIG_DIR : le dossier de configuration du programme.
        Il est calculé par la fonction "getConfigDir"
    * CONFIG_FILE : le fichier dans lequel on enregistre la configuration.
        Ici c'est un fichier texte ("config.txt") placé dans le dossier "CONFIG_DIR"
    * APP_FILE_DIR : le dossier choisi par l'utilisateur.
        Il est enregistré dans le fichier "CONFIG_FILE".
"""
APP_NAME = 'MDP_GENERATOR'
CONFIG_DIR = getConfigDir(APP_NAME)
CONFIG_FILE = CONFIG_DIR / 'config.json'
APP_FILE_DIR = getAppFileDir(CONFIG_FILE)


def chooseAppFileDir():
    """
    Fonction appelée par le bouton "Choisir le dossier".
    On modifie la variable globale "APP_FILE_DIR".
    """
    global APP_FILE_DIR
    newDir = tkinter.filedialog.askdirectory(initialdir=APP_FILE_DIR, mustexist=True)
    if newDir:
        newDir = pathlib.Path(newDir)
        if os.access(newDir, os.W_OK):
            APP_FILE_DIR = newDir
            with CONFIG_FILE.open(mode='w') as f:
                f.write(str(APP_FILE_DIR))
    #print(APP_FILE_DIR)
    

def addPassword():
    """
    Fonction appelée par le bouton "Ajouter une ligne au fichier password.txt".
    """
    passwordsFile = APP_FILE_DIR / 'asuprimer.txt'
    #print(passwordsFile)
    with passwordsFile.open(mode='a+') as f:
        f.write(password_entry.get() + '\n')
"""
***************************************************
***************************************************
Fin de la boite de dialogue 
***************************************************
***************************************************
"""

# La fenêtre !
window = Tk()
#Retirer le: ' | Dev Version' avant de publier
window.title("MDP GENERATOR - " + mdp_ver)
window.geometry('720x480')
window.config(bg='#ffd8a8')

# frame principale
frame = Frame(window, bg='#ffd8a8')

#musique !
pygame.mixer.init()
pygame.mixer.music.load("musiqueGDMDP3.ogg")
while pygame.mixer.get_busy():
  pass
pygame.mixer.music.play(10,0.0)
#stop muisique
def stop_musique():
    pygame.mixer.music.stop()
#pause
def pause_musique():
    pygame.mixer.music.pause()
#reprendre
def play_musique():
    pygame.mixer.music.unpause()


#Fonction Indev
def openInDevWindow():
    indevWindow = Tk()
    indevWindow.title('MDP GEN - InDev')
    indevWindow.geometry('200x90')
    iw_label = Label(indevWindow, text="MDP-VER: " + mdp_ver + isInDevVersionText)
    iw_label.pack()
    iw_label = Label(indevWindow, text="MDP-RELEASE-DATE: " + mdp_release_date)
    iw_label.pack()
    iw_button = Button(indevWindow, text="Chiffrer", command=crypt_mdp)
    iw_button.pack(expand=YES)
    indevWindow.mainloop()



#Fonction de génération du mot de passe
def generate_password():
    if password_entry.get() == "InDev":
        isInDevVersion = True
        window.title("MDP GENERATOR - " + mdp_ver + isInDevVersionText)
        openInDevWindow()
    else:
        password_min = 6
        password_max = 12
        all_chars = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(all_chars) for x in range(randint(password_min, password_max)))
        password_entry.delete(0, END)
        password_entry.insert(1, password)
    
#déchifrement
def decrypt3():
    import sys
    import os
    # on démarre dans le bon dossier :
    HERE = os.path.dirname(sys.argv[0])
    APPDIR = os.path.abspath(HERE)
    sys.path.insert(0, APPDIR)
    os.chdir(APPDIR)

    mdp = 'test'
    mdp_crypt = sha256(mdp.encode('utf-8')).digest()
    key = urlsafe_b64encode(mdp_crypt)
    fernet = Fernet(key)


    # on lit le fichier à déchiffrer :
    message_crypt = ''
    with open(APP_FILE_DIR /'passwords_crypt.txt', mode='r') as f:
        message_crypt = f.read()

    # on déchiffre :
    message = fernet.decrypt(message_crypt.encode('utf-8')).decode('utf-8')
    print(message)

    def afficheMessage():
        messagebox.showinfo('information', message)

    mdp = 'test'
    mdp_crypt = sha256(mdp.encode('utf-8')).digest()
    key = urlsafe_b64encode(mdp_crypt)
    fernet = Fernet(key)


    from tkinter import messagebox

    main = Tk()
    main.iconbitmap('logo_mdpg.ico')
    main.config(bg='#ffd8a8')
    main.title("Déchifrage...")
    main.geometry('250x250')

    def afficheMessage():
        messagebox.showinfo('information', message)

    button = Button(main, text="Déchiffrer", bg='#ffd8a8', font=('Book Antiqua', 20), command=afficheMessage)
    button.pack(expand=YES)

    main.mainloop()


#Chifrement 

def crypt():
    
    mdp = 'test'
    mdp_crypt = sha256(mdp.encode('utf-8')).digest()
    key = urlsafe_b64encode(mdp_crypt)
    fernet = Fernet(key)

    # on lit le fichier à chiffrer :
    message = ''
    with open(APP_FILE_DIR /'asuprimer.txt', mode='r') as f:
        message = f.read()

    # on chiffre :
    message_crypt = fernet.encrypt(message.encode('utf-8')).decode('utf-8')

    # et on enregistre le fichier passwords_crypt.txt :
    with open(APP_FILE_DIR /'passwords_crypt.txt', mode='w') as f:
        f.write(message_crypt)
    
#Fonction avec une touche !
#Génération du mdp
def password_gen(event):
    generate_password()

window.bind("<space>", password_gen)

#enregistrement
def enreg_key(vent):
    save_password()

window.bind('<Control_L>' + '<s>', enreg_key)
window.bind('<Control_R>' + '<s>', enreg_key)

#Sauvegarde du mdp
def save_password():
    if os.path.exists(CONFIG_DIR / 'config.json'):
        addPassword(),
        crypt()
    else:
        chooseAppFileDir(),
        addPassword(),
        crypt()   
#Fin du bouton 

# images canva
width = 300
height = 300
#image
image = PhotoImage(file="LOGO2.png")
canvas = Canvas(frame, width=width, height=height, bg='#ffd8a8', bd=0, highlightthickness=0)
canvas.create_image(width/2, height/2, image=image)
canvas.grid(row=0, column=0, sticky=W)

# sous boite(frame)
right_frame = Frame(frame, bg='#ffd8a8')
#une sousous boite
second_frame = Frame(frame, bg='White')

# Un titre
label_title = Label(right_frame, text="Le mot de passe généré s'affiche ici ! Prend garde de bien le noter quelque-part !", font=("Book Antiqua", 20), bg='#ffd8a8', fg='Black')
label_title.pack()

# Un champs/entrée/input
password_entry = Entry(right_frame, font=("Book Antiqua", 20), bg='White', fg='Black')
password_entry.pack()

# Un bouton
generate_password_button = Button(
    right_frame,
    text="Générer un mot de passe",
    font=("Book Antiqua", 20),
    bg='#ffd8a8',
    fg='Black',
    activebackground='#ffc8a8',
    command=generate_password) 
generate_password_button.pack(fill=X)

#Bouton de sauvegarde
save_password_button = Button(
    right_frame,
    text="Sauvegarder le mot de passe",
    font=("Book Antiqua", 20),
    bg='#ffd8a8',
    fg='Black',
    activebackground='#ffc8a8',
    command=save_password)

save_password_button.pack(fill=X)


#Un menu
#1
def bonj():
    showinfo("Informations Légales", "Ce logiciel a été réalisé en 2020 (pour la première version), suite au projet QS--C DEVELOPEMENT®. Toute copie est interdite.")

menubar = Menu(window)
#2
def UPDA():
    showinfo("Un petit mot du créateur","Bonjour, merci de nous faire confiance. Si vous rencontrer une erreur n'importe laquel prévener moi en allant dans le menu et puis dans Aide et tout en bas de la page web vous trouverez des informations.")
#4
def Quit():
    if askyesno('MDP_GENERATOR', 'Voulez vous vraiment quitter ?'):
        window.quit()

#5
def help():
    webbrowser.open_new('qsoftware.raidghost.com/Mes_logiciels.html')

#6
def decrypt2():
    decrypt3()

#7
def crypt2():
    crypt()



#menubar
menubar.config(bg='White')

menu0 = Menu(menubar, tearoff=0)
menu0.add_command(label="Chiffrer", command=crypt)
menu0.add_command(label="Déchiffrer", command=decrypt2)
menubar.add_cascade(label="Gestion des Mots de passe", menu=menu0)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Informations légales", command=bonj)
menu1.add_command(label="Un petit mot du créateur", command=UPDA)


menubar.add_cascade(label="A Propos ", menu=menu1)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="Page web d'aide", command=help)
menubar.add_cascade(label="Aide", menu=menu4)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Stoper la musique", command=stop_musique)
menubar.add_cascade(label="Musique", menu=menu2)
menu2.add_command(label="Mettre en pause la musique", command=pause_musique)
menu2.add_command(label="Reprendre la musique ", command=play_musique)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Quitter le logiciel", command=Quit)
menubar.add_cascade(label="Quiter", menu=menu3)

window.config(menu=menubar)





""""
Affichage...
"""
#une sousous boite
second_frame.grid(row=1, column=0, sticky=W)
#sous boite à droite de la frame principale
right_frame.grid(row=0, column=1, sticky=W)
# affichage de la frame pricipale
frame.pack(expand=YES)
 # affichage de la fenêtre



window.mainloop()

print("   *******   ")
print("Au revoir ! ")
#Fin du programme