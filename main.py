#main.py by Stephan Green and Ronak Bhagia
#The main file for the game.
#8/12/2021
import pygame, random, os, math
from enum import Enum

import heart, other_screens, player
import word_library as wl
import enemy as e
import button as b

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

#Game State Enum
class Game_State(Enum):
    TITLE = 1
    MAIN = 2
    OVER = 3
    PAUSE = 4

#Display Settings
 #game window height and width
pygame.display.Info()
WIN_W = max(900, pygame.display.Info().current_w)
WIN_H = max(600, pygame.display.Info().current_h)
WIN = pygame.display.set_mode((WIN_W, WIN_H))
FPS = 60
SECS = 1000 #multiplied to get desired time in seconds

#Fonts
WORD_FONT100 = pygame.font.SysFont('Comic Sans', 100)
WORD_FONT40 = pygame.font.SysFont('Comic Sans', 40)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
LIGHT_BLUE = (0,200,200)
RED = (255,0,0)
YELLOW = (255, 255,0)
GREEN = (0,255,0)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIN_W, WIN_H))
#Sounds
pygame.mixer.music.load(os.path.join('Assets','music.wav'))
pygame.mixer.music.set_volume(0.5)
HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))
GET_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'collect.wav'))

#Custom Events
GAIN_HEALTH = pygame.USEREVENT + 1
LOSE_HEALTH = pygame.USEREVENT + 2

MIN_TIME = 2

#Enemy Sprites
enemy_sprites = pygame.sprite.Group()
place_x = 0
for filename in os.listdir('Assets'):
    if filename[len(filename)-5:] == 'd.png': #enemy sprites end with this
        place_x += WIN_W/7
        enemy = e.Enemy(place_x,random.randint(50,150),os.path.join('Assets', filename), int(WIN_H/6))
        enemy_sprites.add(enemy)

#Player Settings
MAX_HEALTH = 5

#Health System
place_x = 0
health_bar = pygame.sprite.Group()
for h in range(MAX_HEALTH):
    place_x += 55
    hearts = heart.Heart(os.path.join('Assets','hud_heartFull.png'),
                os.path.join('Assets','hud_heartEmpty.png'), MAX_HEALTH,place_x,WIN_H-100)
    health_bar.add(hearts)

def refill_health(health_bar):
    assert health_bar.has
    for h in range(len(health_bar)):
        get_sprite(health_bar, h).set_active()

def draw_health(health_bar, curr_health):
    assert health_bar.has
    i = MAX_HEALTH
    while i > curr_health:
        get_sprite(health_bar, i-1).set_inactive()
        i -= 1
    i = 0
    while i < curr_health:
        get_sprite(health_bar, i).set_active()
        i+=1
    health_bar.draw(WIN)
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

#Called every frame to redraw the window every frame
counter = 0
def draw_window(current_word,user_text,word_score, char_score, sprite_id, ch,current_time,tl):
    global counter
    WIN.blit(BACKGROUND,(0,0))
    draw_health(health_bar, ch)

    if counter <= 15 and counter > -1:
        counter += 1
        get_sprite(enemy_sprites, sprite_id).movement(0, 1)
    elif counter > 15:
        counter += 1
        get_sprite(enemy_sprites, sprite_id).movement(0, -1)
    if counter > 30:
        counter = 0

    WIN.blit(get_sprite_image(enemy_sprites, sprite_id),
        (get_sprite(enemy_sprites,sprite_id).rect.x,get_sprite(enemy_sprites,sprite_id).rect.y))

    #Display current word
    WIN.blit(current_word,(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2))

    #Display Text Box
    input_rect = pygame.Rect(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2 + 100, current_word.get_width(), 100)
    pygame.draw.rect(WIN, GRAY, input_rect)
    text_surface = WORD_FONT100.render(user_text, 1, BLACK)
    WIN.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    #Display Scores
    wscore = WORD_FONT40.render("Words Typed: " + str(word_score), 1, WHITE)
    cscore = WORD_FONT40.render("Characters Typed: " + str(char_score), 1, WHITE)
    tscore = WORD_FONT40.render("Time Elapsed: " + str(current_time), 1, WHITE)
    t_left = WORD_FONT40.render("Time Left: " + str(tl), 1, WHITE)
    WIN.blit(wscore, (10, 10))
    WIN.blit(cscore, (10, 50))
    WIN.blit(tscore, (10, 90))
    WIN.blit(t_left, (10, WIN_H - 50))
    pygame.display.update()

#Main function
def main():
    pygame.display.set_caption("Typing Game")
    pygame.mixer.music.play(-1)

    difficulty = "words_common.txt"
    diction = wl.Word_Library(difficulty)
    word_text = "start"
    current_word = WORD_FONT100.render(word_text,1,WHITE)
    user = player.Player(MAX_HEALTH)

    #Clock and Time
    clock = pygame.time.Clock()
    current_time = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()
    time_for_word = 5 * SECS

    #Game States
    game_state = Game_State.TITLE
    run = True
    is_muted = False

    #Buttons Constructor|color, x, y, w, h, text="Button"
    #TileScreen
    easy_button = b.Button(GREEN, WIN_W/2 -150, WIN_H/2, 250, 100, 'Easy')
    hard_button = b.Button(YELLOW, WIN_W/2 -150, WIN_H/2+200, 250, 100, 'Hard')
    exit_button = b.Button(RED, WIN_W/2 -150, WIN_H/2+400, 250, 100, 'Exit Game')
    mute_button = b.Button(LIGHT_BLUE, WIN_W - 150, WIN_H - 100, 100, 100, 'Mute')

    #GameOverScreen
    retry_button = b.Button(GREEN, WIN_W/2 -150, WIN_H/2, 250, 100, 'Retry')
    title_button = b.Button(LIGHT_BLUE, WIN_W/2 -150, WIN_H/2+200, 250, 100, 'Title')

    #PauseScreen
    unpause_button = b.Button(LIGHT_BLUE, WIN_W/2 -150, WIN_H/2, 250, 100, 'Resume')
    quit_button = b.Button(RED, WIN_W/2 -150, WIN_H/2+200, 250, 100, 'Quit')

    can_gain = True
    input_active = True
    user_text = ''

    word_score = 0
    char_score = 0
    sprite_id = 0
    while run:
        clock.tick(FPS) #Sets how many Frames Per Second the game will run at
        if game_state == Game_State.MAIN:
            current_time = math.floor((pygame.time.get_ticks()-start_time)/SECS)
            time_for_word -= 20
            if time_for_word <= 0:
                user.lose_health()
                time_for_word = max(MIN_TIME,(len(word_text)-MIN_TIME)) * SECS
                HIT_SOUND.play()
            if word_score % 10 == 0 and user.get_health() < MAX_HEALTH and can_gain:
                user.gain_health()
                can_gain = False
                GET_SOUND.play()

            if user.get_health() <= 0:
                game_state = Game_State.OVER

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = Game_State.PAUSE
                        break
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

                if user_text == word_text: #if equal to the word make a new word
                    if word_score % 11 == 0:
                        can_gain = True
                    word_score += 1
                    char_score += len(word_text)
                    word_text = random.choice(diction.get_library())[:-1]
                    current_word = WORD_FONT100.render(word_text,1,WHITE)
                    user_text = ''
                    sprite_id = random.randint(0,len(enemy_sprites) - 1)
                    time_for_word = max(MIN_TIME,(len(word_text)-2)) * SECS
            if not run:
                break
            draw_window(current_word, user_text, word_score, char_score,
                        sprite_id,user.get_health(),current_time,
                        math.ceil(time_for_word/SECS))
        elif game_state == Game_State.TITLE or game_state == None:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.isActive(pos):
                        difficulty = 'words_common.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
                    if hard_button.isActive(pos):
                        difficulty = 'words_alpha.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
                    if exit_button.isActive(pos):
                        run = False
                        pygame.quit()
                        break
                    if mute_button.isActive(pos) and not is_muted:
                        pygame.mixer.music.pause()
                        is_muted = True
                    elif mute_button.isActive(pos) and is_muted:
                        pygame.mixer.music.unpause()
                        is_muted = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        difficulty = 'words_common.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
                    if event.key == pygame.K_h:
                        difficulty = 'words_alpha.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
            if not run:
                break
            other_screens.draw_title(easy_button,hard_button,mute_button,exit_button)
        elif game_state == Game_State.OVER:
            user.set_health(MAX_HEALTH)
            refill_health(health_bar)
            user_text = ''
            word_score = 0
            char_score = 0
            sprite_id = 0
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start_time = pygame.time.get_ticks()
                    if retry_button.isActive(pos):
                        game_state = Game_State.MAIN
                    elif title_button.isActive(pos):
                        game_state = Game_State.TITLE

            if not run:
                break
            other_screens.draw_gameover(retry_button, title_button)
        elif game_state == Game_State.PAUSE:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if unpause_button.isActive(pos):
                        game_state = Game_State.MAIN
                    elif quit_button.isActive(pos):
                        game_state = Game_State.OVER
                    if mute_button.isActive(pos) and not is_muted:
                        pygame.mixer.music.pause()
                        is_muted = True
                    elif mute_button.isActive(pos) and is_muted:
                        pygame.mixer.music.unpause()
                        is_muted = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = Game_State.MAIN
            other_screens.draw_pause(unpause_button, quit_button, mute_button)

if __name__ == "__main__":
    main()
