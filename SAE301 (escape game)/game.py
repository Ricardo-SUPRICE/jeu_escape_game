import pygame
import pyscroll
import pytmx

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((320,635))
        pygame.display.set_caption('Jeu')

        tmx_data = pytmx.util_pygame.load_pygame('vladivostok.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2


        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)


    def run(self):
        running = True

        while running:

            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # le joueur a tenter de quitter en cliquant sur la croix
                    running = False
        pygame.quit()