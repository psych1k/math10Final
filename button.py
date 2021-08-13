#button.py
#Used to create button objects for a Pygame game
#Heavily inspired by Tech With Tim's implementation of the button class
#8/12/2021
import pygame

class Button(object):
    def __init__(self, color, x, y, w, h, text="Button"):
        self.d_color = color #default color
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def draw(self, win, font):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.w,self.h),0)
        text = font.render(self.text, 1, (0,0,0)) #(0,0,0) = Black
        win.blit(text,(self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def set_color(self, color):
        self.color = color
    def isActive(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False
