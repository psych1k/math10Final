#main.py by Stephan Green and Ronak Bhagia
#The main file for the game.
import pygame
import random
import os
from enum import Enum

import other_screens
import word_library as wl
import enemy as e
import button as b


pygame.init()
pygame.font.init()
#Enum structure to manage what screen gets shown
class Game_State(Enum):
    TITLE = 1
    MAIN = 2
    OVER = 3
#Display Settings
WIN_W, WIN_H = 900, 600 #game window height and width
WIN = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
FPS = 60

#Fonts
WORD_FONT100 = pygame.font.SysFont('Comic Sans', 100)
WORD_FONT40 = pygame.font.SysFont('Comic Sans', 40)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)

#Enemy Sprites
enemy_sprites = pygame.sprite.Group()
place_x = 0

for filename in os.listdir('Assets'):
    if filename[len(filename)-5:] == 'd.png': #enemy sprites end with this
        place_x += 150
        enemy = e.Enemy(place_x,50,os.path.join('Assets', filename))
        enemy_sprites.add(enemy)

#Takes in a sprite group and an index and returns the sprite image at that given
#index.
def get_sprite_image(group, index):
    assert group.has
    try:
        return group.sprites()[index].image
    except IndexError:
        return group.sprites()[0].image
#Takes in a sprite group and an index and returns the sprite at that given
#index.
def get_sprite(group, index):
    assert group.has
    try:
        return group.sprites()[index]
    except IndexError:
        return group.sprites()[0]

#User Input
#INPUT_RECT = pygame.Rect(WIN_W/2 - 70, WIN_H/2 + 100, 300, 100)

#Called every frame to redraw the window every frame
def draw_window(current_word,user_text,word_score, char_score, sprite_id):
    WIN.fill(BLACK)
    #drawing enemy on screen
    #example of an ememy sprite moving
    #get_sprite(enemy_sprites,3).movement(-2,-1)
    WIN.blit(get_sprite_image(enemy_sprites, sprite_id),
        (get_sprite(enemy_sprites,sprite_id).rect.x,get_sprite(enemy_sprites,sprite_id).rect.y))

    #Display current word
    WIN.blit(current_word,(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2))

    #Display Text Box
    INPUT_RECT = pygame.Rect(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2 + 100, current_word.get_width(), 100)
    pygame.draw.rect(WIN, GRAY, INPUT_RECT)
    text_surface = WORD_FONT100.render(user_text, 1, BLACK)
    WIN.blit(text_surface, (INPUT_RECT.x+5, INPUT_RECT.y+5))
    INPUT_RECT.w = max(100, text_surface.get_width() + 10)

    #Display Scores
    wscore = WORD_FONT40.render("Words Typed: " + str(word_score), 1, WHITE)
    cscore = WORD_FONT40.render("Characters Typed: " + str(char_score), 1, WHITE)
    WIN.blit(wscore, (10, 10))
    WIN.blit(cscore, (10, 50))
    pygame.display.update()

def main():
    pygame.display.set_caption("Typing Game")
    diction = wl.Word_Library('words_common.txt')
    word_text = "start"
    current_word = WORD_FONT100.render(word_text,1,WHITE)
    clock = pygame.time.Clock()
    run = True

    #Game State
    game_state = Game_State.TITLE

    #Buttons
    start_button = b.Button((0,200,200), 150, 300, 250, 100, 'Start')
    retry_button = b.Button((0,200,200), 400, 225, 250, 100, 'Retry')
    title_button = b.Button((0,200,200), 150, 400, 250, 100, 'Title')

    input_active = True
    user_text = ''

    word_score = 0
    char_score = 0
    sprite_id = 0
    while run:
        clock.tick(FPS) #Sets how many Frames Per Second the game will run at
        if game_state == Game_State.MAIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

                    if user_text == word_text: #if equal to the word make a new word

                        word_score += 1
                        char_score += len(word_text)
                        word_text = random.choice(diction.get_library())[:-1]
                        current_word = WORD_FONT100.render(word_text,1,WHITE)
                        user_text = ''
                        sprite_id = random.randint(0,len(enemy_sprites) - 1)

            if not run:
                break
            draw_window(current_word, user_text, word_score, char_score, sprite_id)
        elif game_state == Game_State.TITLE or game_state == None:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.isActive(pos):
                        print('clicked!')
                        game_state = Game_State.MAIN
            other_screens.draw_title(start_button)
        elif game_state == Game_State.OVER:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.isActive(pos):
                        print('clicked!')
                        game_state = Game_State.MAIN
                    elif title_button.isActive(pos):
                        print('clicked!')
                        game_state = Game_State.TITLE
            other_screens.draw_gameover(retry_button, title_button)
    print('Game Over')


if __name__ == "__main__":
    main()
