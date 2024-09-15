
import pygame
import pytmx
import pyscroll
#from pygame.examples.sprite_texture import clock

from player import Player


class Game:#Créationn d'une classe Game

    def __init__(self):#fonction qui ce fait au chargement du jeu

        # crée la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))  # largeur, hauteur
        pygame.display.set_caption('Pokemon - Aventure')  # changer le titre de la fenêtre

        #charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) #charger les different calque de la carte regroupé
        map_layer.zoom = 2

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")#en gros recup le position qui a le nom "player" dans tiled (logiciel pour map et object)
        self.player = Player(player_position.x, player_position.y)#nouvel instance de player avec la position par defaut

        #definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects: # récup tout les object de la carte
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=5)
        self.group.add(self.player)#ajoute le dessin du joueur

        # definir le rectangle de collision pour entrer dans maison
        self.map = 'world'
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
        pressed = pygame.key.get_pressed()# recupere les touche tapé au clavier

        if pressed[pygame.K_UP]:
            self.player.move_up() # pour bouger en haut
            self.player.change_animation('up') # changer l'animation vers le haut
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()# pour bouger en haut
            self.player.change_animation('down')  # changer l'animation vers le haut
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            # pour bouger en haut
            self.player.change_animation('left')  # changer l'animation vers le haut
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            # pour bouger en haut
            self.player.change_animation('right')  # changer l'animation vers le haut

    def switch_house(self): # pour rentrer dans la maison
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('inside_house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())  # charger les different calque de la carte regroupé
        map_layer.zoom = 2

        # definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:  # récup tout les object de la carte
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)  # ajoute le dessin du joueur

        # definir le rectangle de collision pour sortir dans maison
        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self): # pour sortir dans la maison
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())  # charger les different calque de la carte regroupé
        map_layer.zoom = 2

        # definir une liste qui va stocker les rectangles de collision
        self.walls = []
        for obj in tmx_data.objects:  # récup tout les object de la carte
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)  # ajoute le dessin du joueur

        # definir le rectangle de collision pour rentrer de la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recuperer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name("spawn_house_exit")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20

    def update(self):
        self.group.update() # va actualiser le group

        #if self.player.feet.collide(self.enter_house_rect):
        #    self.switch_house()

        # verifier l'entrer dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # verifier sortie dans la maison
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        #verification de la collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):#autre méthode pour lancer la fenetre

        clock = pygame.time.Clock() # fixer le nombre de fps a chaque tour de boucle

        # boucle du jeu
        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect) # centrer la caméra sur le joueur
            self.group.draw(self.screen) #dessiner les calques sur la fenetre
            pygame.display.flip() # pour accualiser la map

            for event in pygame.event.get():  # pygame.event.get --> liste de tout les evenements
                if event.type == pygame.QUIT:  # le joueur a tenter de quitter en cliquant sur la croix
                    running = False  # donc on arrete le jeu

            clock.tick(60) # 60 fps

        pygame.quit()  # et on quitter le jeu