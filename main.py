#main.py by Stephan Green and Ronak Bhagia
#The main file for the game.
import pygame, random, os, math
from enum import Enum
#from pygame import mixer

import heart, other_screens, player
import word_library as wl
import enemy as e
import button as b

pygame.init()
pygame.font.init()
pygame.mixer.init()

#Game State Enum
class Game_State(Enum):
    TITLE = 1
    MAIN = 2
    OVER = 3

#Display Settings
WIN_W, WIN_H = 900, 600 #game window height and width
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
        place_x += 150
        enemy = e.Enemy(place_x,150,os.path.join('Assets', filename))
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
    for h in range(len(health_bar)):
        get_sprite(health_bar, h).set_active()

def draw_health(health_bar, curr_health):
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

#User Input
#INPUT_RECT = pygame.Rect(WIN_W/2 - 70, WIN_H/2 + 100, 300, 100)

#Called every frame to redraw the window every frame
counter = 0
def draw_window(current_word,user_text,word_score, char_score, sprite_id, ch,current_time,tl):
    global counter
    #WIN.fill(BLACK)
    WIN.blit(BACKGROUND,(0,0))
    draw_health(health_bar, ch)
    #drawing enemy on screen
    #example of an ememy sprite moving
    #get_sprite(enemy_sprites,3).movement(-2,-1)
    if counter <= 15 and counter > -1:
        counter += 1
        get_sprite(enemy_sprites, sprite_id).movement(0, 1)
    elif counter > 15:
        counter += 1
        get_sprite(enemy_sprites, sprite_id).movement(0, -1)
    if counter >30:
        counter = 0

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
    tscore = WORD_FONT40.render("Time Elapsed: " + str(current_time), 1, WHITE)
    t_left = WORD_FONT40.render("Time Left: " + str(tl), 1, WHITE)
    WIN.blit(wscore, (10, 10))
    WIN.blit(cscore, (10, 50))
    WIN.blit(tscore, (10, 90))
    WIN.blit(t_left, (10,WIN_H - 50))
    pygame.display.update()

def main():
    pygame.display.set_caption("Typing Game")
    pygame.mixer.music.play(-1)
    #diction = wl.Word_Library('words_common.txt')
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

    #Game State
    game_state = Game_State.TITLE
    run = True

    #Buttons
    #TileScreen
    easy_button = b.Button((0,200,200), 150, 300, 250, 100, 'Easy')
    hard_button = b.Button((0,200,200), 150, 450, 250, 100, 'Hard')

    #GameOverScreen
    retry_button = b.Button((0,200,200), 400, 225, 250, 100, 'Retry')
    title_button = b.Button((0,200,200), 150, 400, 250, 100, 'Title')

    can_gain = True
    input_active = True
    user_text = ''

    word_score = 0
    char_score = 0
    sprite_id = 0
    while run:
        clock.tick(FPS) #Sets how many Frames Per Second the game will run at
        print(start_time)
        if game_state == Game_State.MAIN:
            current_time = math.floor((pygame.time.get_ticks()-start_time)/SECS)
            time_for_word -= 20
            if time_for_word <= 0:
                user.lose_health()
                time_for_word = max(MIN_TIME,(len(word_text)-2)) * SECS
                HIT_SOUND.play()
            if word_score % 10 == 0 and user.get_health() < MAX_HEALTH and can_gain:
                user.gain_health()
                can_gain = False
                GET_SOUND.play()
                # pygame.event.post(pygame.event.Event(GAIN_HEALTH))
            if user.get_health() <= 0:
                pygame.time.wait(SECS)
                game_state = Game_State.OVER
                start_time = pygame.time.get_ticks()

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
                        sprite_id,user.get_health(),current_time,math.ceil(time_for_word/SECS))
        elif game_state == Game_State.TITLE or game_state == None:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if easy_button.isActive(pos):
                        difficulty = 'words_common.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
                    if hard_button.isActive(pos):
                        difficulty = 'words_alpha.txt'
                        diction = wl.Word_Library(difficulty)
                        game_state = Game_State.MAIN
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
            other_screens.draw_title(easy_button,hard_button)
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
                    if retry_button.isActive(pos):
                        game_state = Game_State.MAIN
                    elif title_button.isActive(pos):
                        game_state = Game_State.TITLE
            if not run:
                break
            other_screens.draw_gameover(retry_button, title_button)
    print('Game Over')


if __name__ == "__main__":
    main()
