#other_screens.py by Stephan Green
#used to draw the title and game over windows
import pygame
import os
import button
from main import *

def display_title(title):
    title = WORD_FONT100.render(title,1,WHITE)
    WIN.blit(BACKGROUND,(0,0))
    WIN.blit(title, (WIN_W/2 - title.get_width()/2, WIN_H/2- title.get_height()/2 - 100))
def draw_title(button, hbtn, mbtn, qbtn):
    display_title('Typing Game')
    button.draw(WIN, WORD_FONT40)
    hbtn.draw(WIN, WORD_FONT40)
    mbtn.draw(WIN, WORD_FONT40)
    qbtn.draw(WIN, WORD_FONT40)
    pygame.display.update()

def draw_gameover(retry_button, title_button):
    display_title('Game Over')
    retry_button.draw(WIN, WORD_FONT40)
    title_button.draw(WIN, WORD_FONT40)
    pygame.display.update()

def draw_pause(unpause_btn, title_btn, mbtn):
    display_title('Paused')
    unpause_btn.draw(WIN, WORD_FONT40)
    title_btn.draw(WIN, WORD_FONT40)
    mbtn.draw(WIN, WORD_FONT40)
    pygame.display.update()
# def main():
#     run = True
#     start_button = button.Button((0,200,200), 150, 225, 250, 100, 'Click')
#     while run:
#         for event in pygame.event.get():
#             pos = pygame.mouse.get_pos()
#             if event.type == pygame.QUIT:
#                     run = False
#                     pygame.quit()
#                     break
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if start_button.isActive(pos):
#                     print('clicked!')
#                     run = False
#         draw_title(start_button)
# #         #return 1
# if __name__ == "__main__":
#     main()
