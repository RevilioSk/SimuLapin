# Axes d'améliorations / boîte à idées :
#     - écrire la fitness dans un fichier ? Faire une courbe ?
#     - modifier le système de reproduction et de survivants ?
#         - peut-être un temps de survie, peut-être une reproduction plus précise et plus poussée
#         - mélanger les différentes génération ? (les lapins n'attendent pas forcément la fin pour commencer à se reproduire)
#     - rendre les loups fonctionnels
#     - ajouter des sprites

# A faire / corriger :
#     - certains lapins se coincent dans les coins
#     - ont du mal à manger les plantes malgré le dash
#     - afficher en temps réel les données sur l'écran (lapins, lapins morts, lapins nourris...)
#     - afficher entre chaque génération un bilan avec : progression directe, progression globale, nombre de lapins survivants...




from tkinter import *
import random
import sys
from threading import Thread
import time
from os import path as os_path


# Creation de la fenetre du jeu
Mafenetre = Tk()
Mafenetre.title('Selection Naturelle')
text = Text(Mafenetre, wrap = 'word')

#Variables Globales
Largeur = Mafenetre.winfo_screenwidth()-150
Hauteur = Mafenetre.winfo_screenheight()-150

Multiple = 1
Compteur = 150
Compteur2 = 100

Temperature = 20

nbl=20  #Nombre de lapins
nbp=int(2*nbl)  #Nombre de plantes : si le nombre de lapins augmente, on augmente le nombre de plantes

##ChampDeVision=random.randint(30,35)
ChampDeVision=random.randint(50,65) # (Alex) j'ai augmenté l'écart entre les champs de vision + j'ai augmenté ce qui fait que les lapins couvrent plus de terrain





###Classes###

class Lapin:
    def __init__(self,posx,posy,faim,faimbase,cdv,direction,vivant,soif,soifbase,fourrure,reproduction):
        self.posx = posx
        self.posy = posy
        self.faim = faim
        self.faimbase = faimbase
        self.cdv = cdv
        self.vivant = vivant
        self.direction = direction
        self.soif = soif
        self.soifbase = soifbase
        self.fourrure = fourrure
        self.reproduction = reproduction

    # Les lapins avancent selon une direction aléatoire (peuvent se déplacer en diagonale)

    def Avancer(self):  

        if self.vivant :
            if self.direction == 0 :
                self.posx += 1.75
            if self.direction == 1 :
                self.posx -= 1.75
            if self.direction == 2 :
                self.posy += 1.75
            if self.direction == 3 :
                self.posy -= 1.75

            if self.direction == 4 :
                self.posx += 1
                self.posy += 1
            if self.direction == 5 :
                self.posx -= 1
                self.posy -= 1
            if self.direction == 6 :
                self.posx -= 1
                self.posy += 1
            if self.direction == 7 :
                self.posx += 1
                self.posy -= 1


        
            
    
    # Vérfie la position des lapins en fonction de bordures et les fait changer de direction

    def Verif(self,Herbe):
        #global NbArret
        if self.vivant:
            if self.posx < 5:
                self.posx = 5
                self.direction = 0
            if self.posx > Largeur-5:
                self.posx = Largeur-5
                self.direction = 1
            if self.posy < 5:
                self.posy =5
                self.direction = 2
            if self.posy > Hauteur-5:
                self.posy = Hauteur-5
                self.direction = 3

        
        
        # Passe l'état du lapin a non vivant si la faim tombe à 0

        if self.faim<=0:
            self.vivant = False

        # Permet de vérifier la présence d'une plante dans le champ de vision du lapin. Si une plante est repérée, le lapin se dirige sur la plante

        if Herbe.posx <= self.posx+self.cdv and Herbe.posx >= self.posx-self.cdv and Herbe.posy <= self.posy+self.cdv and Herbe.posy >= self.posy-self.cdv and self.faim<50 and self.vivant==True:
            if Herbe.posx-self.posx <0:
                self.posx -= 1
            if Herbe.posx-self.posx >0:
                self.posx += 1
            if Herbe.posy-self.posy <0:
                self.posy -= 1
            if Herbe.posy-self.posy >0:
                self.posy += 1
           
            #Pousse le lapin à se diriger vers la plante la plus proche dans son champs de vision.
            if Herbe.posx-self.posx <1 and Herbe.posx-self.posx>-1 :
                self.posx = Herbe.posx
            if Herbe.posy-self.posy <1 and Herbe.posy-self.posy>-1 :
                self.posy = Herbe.posy


            



        



class Herbe:
    def __init__(self,posx,posy):
        self.posx = posx
        self.posy = posy



###Création des entitées###

Population = []

for i in range(nbl):
    startX = random.randint(1,Largeur)
    startY = random.randint(1,Hauteur)
    Dir = random.randint(1,7)
    faimdebut = 100
    soifdebut = 100
    ChanceFurr = random.randint(0,100)
    if ChanceFurr<10:
        Furr = 1
    elif ChanceFurr>90:
        Furr = 3
    else:
        Furr = 2
    l = Lapin(startX,startY,faimdebut,faimdebut,ChampDeVision,Dir,True,soifdebut,soifdebut,Furr,False)
    Population.append(l)



Plantes = []

for i in range(nbp):
    t = Herbe(random.randint(100,Largeur-100),random.randint(100,Hauteur-100))
    Plantes.append(t)








###Fonction###



def VerifMort():
    global Population,nbl,PionL
    for elem in Population:
        if elem.vivant == False:
            elem.posx=-20
            elem.posx=-20
            

# Fait repousser les plantes

def RegenPlante():
    global Plantes
    Plantes = []

    for i in range(nbp):
        t = Herbe(random.randint(100,Largeur-100),random.randint(100,Hauteur-100))
        Plantes.append(t)
        





# Gère l'affichage de toutes les entités à l'écran

def Affichage():
    global Population,Plantes
    for i in range(nbl):
        Canevas.coords(PionL[i],Population[i].posx -4, Population[i].posy -4, Population[i].posx  +4, Population[i].posy +4)
        #Canevas.coords(ChampDV[i],Population[i].posx -Population[i].cdv, Population[i].posy -Population[i].cdv, Population[i].posx  +Population[i].cdv, Population[i].posy +Population[i].cdv)
        if Population[i].vivant == False:
            Canevas.itemconfig(PionL[i], fill='black')
        if Population[i].fourrure == 1:
            Canevas.itemconfig(PionL[i], outline='black')
        if Population[i].fourrure == 3:
            Canevas.itemconfig(PionL[i], outline='#21E418')
    for j in range(nbp): 
        Canevas.coords(PionsH[j],Plantes[j].posx -2, Plantes[j].posy -2, Plantes[j].posx  +2, Plantes[j].posy +2)
        
# Gère le mouvement de tous les lapins

def Mouvement():
    global Population,Plantes
    for i in range(nbl):
        Population[i].Avancer()
        for j in range(nbp):
            Population[i].Verif(Plantes[j])


def AMange():
    global Population,Plantes

    for i in range(nbl):
        for j in range(nbp):
            if Population[i].posx > Plantes[j].posx-1.5 and Population[i].posx < Plantes[j].posx+1.5 and Population[i].posy > Plantes[j].posy-1.5 and Population[i].posy < Plantes[j].posy+1.5 and Population[i].faim<50:
                Plantes[j].posx = -50
                Plantes[j].posy= -50
                Population[i].faim=100







# Démarre une nouvelle génération de lapins

def Controlleur():
    global Population,Plantes
    global Compteur,nbl,Compteur2
    

    

    Mouvement()
    AMange()
    Compteur -= 1
    if Compteur<=0:
        for i in range(nbl):
            Population[i].direction = random.randint(0,7)
            if Temperature < 10:
                if Population[i].fourrure!=1:
                    Population[i].faim -=1
            if Temperature > 25:
                if Population[i].fourrure!=3:
                    Population[i].faim -=1
            Population[i].faim -=1
        Compteur2 -= 1
        Compteur = 50/Multiple
    if Compteur2<=0:
        RegenPlante()
        VerifMort()
        Compteur2 = 100
        Canevas.delete("display")

        display = Canevas.create_text(Largeur/2,(Hauteur/15)*14, text=str(Population[1].vivant) + " | " + str(Population[2].vivant) + " | "+ str(Population[3].vivant) + " | " + str(Population[4].vivant) + " | " +str(Population[5].vivant) + " | ", tag = "display", fill="#000", font="Helvetica", width=Largeur-10)
    

    Affichage()
    Mafenetre.after(1,Controlleur)










# Creation d'un widget Canvas (zone graphique)

Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='#11651C')
Canevas.pack(padx=5,pady=5)

display = Canevas.create_text(Largeur/2,Hauteur/2, text="")

PionL = []
for i in range(nbl):
    PionLapin = Canevas.create_oval(Population[i].posx-2,Population[i].posy-2,Population[i].posx+2,Population[i].posy+2,width=2,outline='#0564E5',fill='#0564E5')
    PionL.append(PionLapin)



PionsH = []
for i in range(nbp):
    PionHerbe = Canevas.create_oval(Plantes[i].posx-2,Plantes[i].posy-2,Plantes[i].posx+2,Plantes[i].posy+2,width=2,outline='#0AB604',fill='#0CFF00')
    PionsH.append(PionHerbe)


Canevas.focus_set()

spamVar = StringVar()



Controlleur()

#Button(Mafenetre, text ='Exit', bd=0, bg='#DC4C4C', activebackground='#E51717',fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X1',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois1).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X2',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois2).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X5',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois5).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X10',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois10).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X20',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois20).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='X50',bd=0, bg='#3985DD', activebackground='#04438C', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = fois50).pack(side=LEFT,padx=5,pady=5)
#Button(Mafenetre, text ='New gen',bd=0, bg='#21BA0C', activebackground='#1A9708', fg="#ffffff", activeforeground="#fff", font="Helvetica", height=2, command = Restart).pack(side=LEFT,padx=5,pady=5)
#Checkbutton(Mafenetre, text ='Disable auto mode', bg="#fff", offrelief='groove', command = autoMode, selectcolor="#DC4C4C", height=2, font="Helvetica", indicatoron=0, variable=auto, offvalue=0, onvalue=1).pack(side=LEFT,padx=5,pady=5)


Mafenetre.mainloop()




































































"""E = 0.25
Compteur = 150/Multiple # Multiple sert à gérer la vitesse de déplacement des lapins
nblp=int(0.1*nbl) #Nombre de loups
NbArret = 0 # Permet de savoir quand appeler Restart (quand tous les lapins sont arrêtés : nourris ou morts)

Alexisse = 0 # Nombre de lapins qui ont mangé

sommeEndDepart = 0
sommeCdvDepart = 0

numGeneration = 0

auto = True


a= "./fichier.txt" """






"""ChampDV = []
for i in range(nbl):
    Cercle = Canevas.create_oval(Population[i].posx-Population[i].cdv,Population[i].posy-Population[i].cdv,Population[i].posx+Population[i].cdv,Population[i].posy+Population[i].cdv,width=1,outline='black')
    ChampDV.append(Cercle)"""

"""PionLp = []
for i in range(nblp):
    PionLoup = Canevas.create_oval(Meute[i].posx-2,Meute[i].posy-2,Meute[i].posx+2,Meute[i].posy+2,width=2,outline='#F60707',fill='#F60707')
    PionLp.append(PionLoup)"""


"""class Loup:
    def __init__(self,posx,posy,cdv,direction,nourrit):
        self.posx = posx
        self.posy = posy
        self.cdv = cdv
        self.direction = direction
        self.nourrit = nourrit

    # Les Loups avancent selon une direction aléatoire (peuvent se déplacer en diagonale)

    def Avancer(self):  

        if not self.nourrit:
            if self.direction == 0 :
                self.posx += 1.25*Multiple
            if self.direction == 1 :
                self.posx -= 1.25*Multiple
            if self.direction == 2 :
                self.posy += 1.25*Multiple
            if self.direction == 3 :
                self.posy -= 1.25*Multiple

            if self.direction == 4 :
                self.posx += 1*Multiple
                self.posy += 1*Multiple
            if self.direction == 5 :
                self.posx -= 1*Multiple
                self.posy -= 1*Multiple
            if self.direction == 6 :
                self.posx -= 1*Multiple
                self.posy += 1*Multiple
            if self.direction == 7 :
                self.posx += 1*Multiple
                self.posy -= 1*Multiple


            
    
    # Vérfie la position des Loups en fonction de bordures et les fait changer de direction

    def Verif(self,Lapin):
        global NbArret
        if self.posx < 5:
            self.posx = 5
            self.direction = 0
        if self.posx > Largeur-5:
            self.posx = Largeur-5
            self.direction = 1
        if self.posy < 5:
            self.posy =5
            self.direction = 2
        if self.posy > Hauteur-5:
            self.posy = Hauteur-5
            self.direction = 3



        # Permet de vérifier le champ de vision du Loup. Si un Lapin est repéré, le Loup se dirige ve le Lapin

        if Lapin.posx <= self.posx+self.cdv and Lapin.posx >= self.posx-self.cdv and Lapin.posy <= self.posy+self.cdv and Lapin.posy >= self.posy-self.cdv and Lapin.nourrit==False and Lapin.vivant==True and not self.nourrit:
            if Lapin.posx-self.posx <0:
                self.posx -= 0.5*Multiple
            if Lapin.posx-self.posx >0:
                self.posx += 0.5*Multiple
            if Lapin.posy-self.posy <0:
                self.posy -= 0.5*Multiple
            if Lapin.posy-self.posy >0:
                self.posy += 0.5*Multiple

            if Lapin.posx-self.posx <Multiple and Lapin.posx-self.posx>-Multiple :
                self.posx = Lapin.posx
            if Lapin.posy-self.posy <Multiple and Lapin.posy-self.posy>-Multiple :
                self.posy = Lapin.posy
        #Pousse le Loup à se diriger vers le Lapin le plus proche dans son champs de vision."""

"""sommeEndDepart += Population[i].endubase
    sommeCdvDepart += Population[i].cdv

numGeneration += 1
moyenneEndDepart = sommeEndDepart/nbl
moyenneCdvDepart = sommeCdvDepart/nbl"""
"""def Fuite(self,Loup):
        if Loup.posx <= self.posx+self.cdv and Loup.posx >= self.posx-self.cdv and Loup.posy <= self.posy+self.cdv and Loup.posy >= self.posy-self.cdv and self.vivant==True:
            if Loup.posx-self.posx <0:
                self.posx += 1
            if Loup.posx-self.posx >0:
                self.posx -= 1
            if Loup.posy-self.posy <0:
                self.posy += 1
            if Loup.posy-self.posy >0:
                self.posy -= 1"""



# Passe l'état du lapin a non vivant si l'endurance tombe à 0

"""if self.endurance<=0:
            self.endurance=1 # Evite un bug
            self.vivant = False
            NbArret += 1"""

# Permet de diminuer l'endurance des lapins quand ils avancent

"""if not self.nourrit and self.vivant:
            self.endurance -= E *Multiple"""