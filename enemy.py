#Enemy class by Stephan Green
#Inherits from pygame's sprite class
import pygame
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, i):
        super().__init__()
        self.sprite = pygame.image.load(i)
        self.image = self.sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    #simple movement. takes in x and y velocity and the sprite will move
    #accordingly in pixels. currently, y value is not required.
    def movement(self, velocity_x, velocity_y=0):
        self.rect.x += velocity_x
        self.rect.y += velocity_y

    def idle_anim(self):
        for y in range(0,10):
            self.movement(0,y)
        for y in range(0,-10):
            print(y)
            self.movement(0, y)
