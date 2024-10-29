
import pygame
import pyscroll
import pytmx

from player import Player


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((320,635))
        pygame.display.set_caption('Jeu')

        tmx_data = pytmx.util_pygame.load_pygame('vladivostok.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x,player_position.y)
        self.map = "vladivostok"
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        enter_osaka = tmx_data.get_object_by_name("enter_osaka_from_vladi")
        self.enter_osaka_rect = pygame.Rect(enter_osaka.x,enter_osaka.y,enter_osaka.width,enter_osaka.height)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_osaka(self):
        tmx_data = pytmx.util_pygame.load_pygame('osaka.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        enter_vladi = tmx_data.get_object_by_name("enter_vladi_from_osaka")
        self.enter_vladi_rect = pygame.Rect(enter_vladi.x, enter_vladi.y, enter_vladi.width, enter_vladi.height)

        spawn_osaka = tmx_data.get_object_by_name("spawn_osaka")
        self.player.position[0] = spawn_osaka.x
        self.player.position[1] = spawn_osaka.y - 20

    def switch_vladi(self):
        tmx_data = pytmx.util_pygame.load_pygame('vladivostok.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        enter_osaka = tmx_data.get_object_by_name("enter_osaka_from_vladi")
        self.enter_osaka_rect = pygame.Rect(enter_osaka.x, enter_osaka.y, enter_osaka.width, enter_osaka.height)

        spawn_vladi = tmx_data.get_object_by_name("enter_osaka_from_vladi_exit")
        self.player.position[0] = spawn_vladi.x
        self.player.position[1] = spawn_vladi.y + 15


    def update(self):
        self.group.update()

        if  self.map == "vladivostok" and self.player.feet.colliderect(self.enter_osaka_rect):
            self.switch_osaka()
            self.map = "osaka"

        if  self.map == "osaka" and self.player.feet.colliderect(self.enter_vladi_rect):
            self.switch_vladi()
            self.map = "vladivostok"


        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self):

        clock = pygame.time.Clock()
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # le joueur a tenter de quitter en cliquant sur la croix
                    running = False

            clock.tick(60)
        pygame.quit()