import pygame
import random
import word_library as wl

pygame.font.init()

#Display Settings
WIN_W, WIN_H = 900, 600 #game window height and width
WIN = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
FPS = 15

#Fonts
WORD_FONT100 = pygame.font.SysFont('Comic Sans', 100)
WORD_FONT40 = pygame.font.SysFont('Comic Sans', 40)
#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)

#User Input
#INPUT_RECT = pygame.Rect(WIN_W/2 - 70, WIN_H/2 + 100, 300, 100)

#Called every frame to redraw the window every frame
def draw_window(current_word,user_text,word_score, char_score):
    WIN.fill(BLACK)
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
    wscore = WORD_FONT40.render("Words Typed: "+str(word_score), 1, WHITE)
    cscore = WORD_FONT40.render("Characters Typed: "+str(char_score), 1, WHITE)
    WIN.blit(wscore, (10, 10))
    WIN.blit(cscore, (10, 50))
    pygame.display.update()

def main():
    pygame.display.set_caption("Typing Game")
    diction = wl.Word_Library('words_alpha.txt')
    word_text = "start"
    current_word = WORD_FONT100.render(word_text,1,WHITE)
    clock = pygame.time.Clock()
    run = True

    input_active = True
    user_text = ''

    word_score = 0
    char_score = 0
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break;
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     # if INPUT_RECT.collidepoint(event.pos):
            #     #     input_active = True
            #     # else:
            #     #     input_active = False

            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                #[:-1 removes \n]
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
        if not run:
            break
        draw_window(current_word, user_text, word_score, char_score)
    print('Game Over')


if __name__ == "__main__":
    main()
