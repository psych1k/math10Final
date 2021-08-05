import pygame
class Heart(pygame.sprite.Sprite):
    def __init__(self, a, i, th,x,y): #a = activeheart i= inactive heart
        super().__init__()
        self.active_sprite = pygame.image.load(a)
        self.inactive_sprite = pygame.image.load(i)
        self.image = self.active_sprite
        self.rect = self.image.get_rect()
        self.total_hearts = th
        self.rect.topleft = [x,y]
    def set_inactive(self):
        self.image = self.inactive_sprite
    def set_active(self):
        self.image = self.active_sprite
