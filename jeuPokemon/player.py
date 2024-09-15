import pygame


class Player(pygame.sprite.Sprite):# Player va herité de la super classe Sprite
# Sprite element graphique tu jeu (petit personnage du jeu), qui est non static (decor est static)

    def __init__(self,x, y):
        super().__init__()# initialiser le Sprite
        self.sprite_sheet = pygame.image.load('assets\player\Player.png')#recupere le spirte sheet
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0)) # enlever bande noir derriere image
        self.rect = self.image.get_rect()
        self.position = [x, y] # enregistre position par defaut
        self.images = {
            'down' : self.get_image(0, 0),#l'image 0 0 regarde vers le bas donc quand on vers bas on veut cette image
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        } # dictionnaire qui stock les image de chaque direction
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12) # rectangle pour avoir les pied
        self.old_position = self.position.copy() # dupliquer les position, va modif la position d'avant de ce deplacer
        self.speed = 3 #deplacement de combien de case

    def save_location(self): self.old_position = self.position.copy()#on ppeut appler la faonction avant de faire le déplacement pour memoriser l'ancien

    def change_animation(self,name):
        self.image = self.images[name]# changer d'animation a chaque déplacement
        self.image.set_colorkey((0, 0, 0)) # pour que toutes les images n'est pas le fond noir de base
    # modif position en x
    def move_right(self): self.position[0] += self.speed
    def move_left(self): self.position[0] -= self.speed

    # modif position en y
    def move_up(self): self.position[1] -= self.speed
    def move_down(self): self.position[1] += self.speed



    def update(self): # mettre a jour auto le sprite et position du joueur
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):# quand joueur entre en collision il ce replace a la position d'avant la colliqion
        self.position = self.old_position # donc il ce replace en arriere
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_image(self,x ,y):#doneée les coordonée en x et y de l'image en question
        image = pygame.Surface([32, 32])#taille en largeur et hauteur
        image.blit(self.sprite_sheet,(0,0),(x, y, 32, 32))#extraire 1 morceau de l'image
        return image # renvoir l'image qui a été decouper
