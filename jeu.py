# Import and initialize the pygame library
#Python version 3.8.1
#pour pouvoir executer le code suivant veuillez installer les bibliothèques suivantes
import pygame #pour dessiner 
import numpy as np #pour le calcul matriciel 
import matplotlib.pyplot as plt #pour dessiner un graphe  

class Marchand:
    def __init__(self, id_marchand, color, X, Y, prix, gain, nbr_clients): #Constructeur du marchand
        self.color = color
        self.X = X
        self.Y = Y
        self.id_marchand = id_marchand
        self.prix = prix 
        self.gain = gain
        self.nbr_clients = nbr_clients
    def draw(self, screen):  #dessiner un marchand
        image = pygame.image.load("marchand.jpg").convert()
        image = pygame.transform.scale(image, (60, 60))
        screen.blit(image, (self.X, self.Y))
    def set_pos(self, X, Y): #changer la position d'un marchand en restant dans la fenetre
        if X <= 700: self.X = X
        else : self.X = 0
        if Y <= 700 : self.Y = Y
        else : self.Y = 0
    def calcul_nbr_clients(self, list_clients, list_marchands): #calcul le nombre de clients des marchands
        for c in list_clients:
            choix = c.choice_marchand(list_marchands)
            list_marchands[choix].nbr_clients += 1
    def choice_pos(self, list_clients, list_marchands, indx):  #choisir la direction d'un marchand adéquate pour augmenter le nombre de clients
        #définir les 4 directions possibles pour le déplacement : gauche, droite, en haut, en bas
        direction = [[list_marchands[indx].X-10, list_marchands[indx].Y],
                    [list_marchands[indx].X+10, list_marchands[indx].Y],
                    [list_marchands[indx].X, list_marchands[indx].Y+10],
                    [list_marchands[indx].X, list_marchands[indx].Y-10]]
        c_max = 0 
        indx_pos = 0
        #pour chaque direction on calcul le nombre de clients et apres on prend la direction qui a amené plus de clients
        for i in range(len(direction)-1):   
            list_marchands[indx].nbr_clients = 0
            list_marchands_tst = list_marchands
            list_marchands_tst[indx].X = direction[i][0]
            list_marchands_tst[indx].Y = direction[i][1]  
            self.calcul_nbr_clients(list_clients, list_marchands_tst)
            if c_max<list_marchands_tst[indx].nbr_clients:
                c_max = list_marchands_tst[indx].nbr_clients
                list_marchands[indx].nbr_clients = c_max
                indx_pos = i
        list_marchands[indx].set_pos(direction[indx_pos][0], direction[indx_pos][1])
        list_marchands[indx].gain.append(list_marchands[indx].prix*list_marchands[indx].nbr_clients)
    def update_marchands(list_clients, list_marchads): #choisir la direction des marchands
        for marchand in list_marchands:
            marchand.choice_pos(list_clients, list_marchads, marchand.id_marchand)
                
class Client:
    def __init__(self, color, X, Y): #constructeur du client
        self.color = color
        self.X = X
        self.Y = Y
    def draw(self): #dessiner un client
        pygame.draw.circle(screen, self.color, (self.X, self.Y), 3)
    def choice_marchand(self, list_marchands): #choisir un marchand en minimisant (la distance + prix) et prendre sa couleur
        choix = 0 #id_marchand num 0
        min_dist = self.dist(list_marchands[0])
        for i in range(len(list_marchands)) : 
            if self.dist(list_marchands[i]) <= min_dist:
                choix = i
                min_dist = self.dist(list_marchands[i])
                self.color = list_marchands[i].color
        return list_marchands[choix].id_marchand
    def dist(self, marchands): #calucul de (la distance + prix) en un marchand et un client
        return marchands.prix + np.sqrt((self.X-marchands.X)**(2) +(self.Y-marchands.Y)**(2))

#---------------------
pygame.init()

# Define the screen width and height
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🍧 Le jeu des marchands de glace 🍧")
icone = pygame.image.load("icone.png").convert()
pygame.display.set_icon(icone)

# creation des marchands
M1 = Marchand(0, (255, 0, 0), 100, 100, 200, [], 0)
M2 = Marchand(1, (0, 255, 0), 650, 300, 200, [], 0)
M3 = Marchand(2, (0, 0, 255), 350, 550, 200, [], 0)

list_marchands = [M1, M2, M3] 

#creation des clients
list_clients = []
position_client = np.random.randint(700, size=(100, 2)) #matrice pour definir les positions (X,Y) de 100 clients
for i in range(100) : 
    c = Client((128,84,43), position_client[i, 0], position_client[i, 1])
    list_clients.append(c)
    list_marchands[c.choice_marchand(list_marchands)].nbr_clients += 1

#faire 55 deplacements
for i in range(55):
    # Run until the user asks to quit
    running = True
    while running: 
        # Fill the background with white
        screen.fill((255, 255, 255))
        #dessiner les clients
        for c in list_clients:
            c.draw() 
        #dessiner les marchands
        for m in list_marchands:
            m.draw(screen)
        
        pygame.time.wait(200)
        if i < 54 : 
            running = False
        else : running =  True
        
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Flip the display
        pygame.display.flip()
    Marchand.update_marchands(list_clients, list_marchands)

# Done! Time to quit.
pygame.quit()

#déssiner les coubes de gain de chaque marchand durant les 55 déplacements
plt.figure(figsize=(10,7))
col = ["red", "green", "blue"]
for k in range(3):
    plt.plot(list_marchands[k].gain, c=col[k])
plt.xlabel("Déplacement")
plt.ylabel("Gain")
plt.title("Les coubes de gain de chaque marchand")
plt.show()
