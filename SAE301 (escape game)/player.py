import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # initialiser le Sprite
        self.sprite_sheet = pygame.image.load('assets\player\Player.png')
        self.image = self.get_image(0, 0)

    def get_image(self, x, y):  # doneée les coordonée en x et y de l'image en question
        image = pygame.Surface([32, 32])  # taille en largeur et hauteur
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))  # extraire 1 morceau de l'image
        return image  # renvoir l'image qui a été decouper