import pygame
import random
import word_library as wl

pygame.font.init()

#Display Settings
WIN_W, WIN_H = 900, 600 #game window height and width
WIN = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
FPS = 60

#Fonts
WORD_FONT100 = pygame.font.SysFont('Comic Sans', 100)
WORD_FONT20 = pygame.font.SysFont('Comic Sans', 20)
#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)

#User Input
INPUT_RECT = pygame.Rect(WIN_W/2 - 200, WIN_H/2 + 100, 300, 100)

def draw_window(current_word,user_text,word_score, char_score):
    WIN.fill(BLACK)
    #Display current word
    WIN.blit(current_word,(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2))

    #Display Text Box
    pygame.draw.rect(WIN, GRAY, INPUT_RECT)
    text_surface = WORD_FONT100.render(user_text, 1, BLACK)
    WIN.blit(text_surface, (INPUT_RECT.x+5, INPUT_RECT.y+5))
    INPUT_RECT.w = max(100, text_surface.get_width() + 10)

    #Display Scores
    wscore = WORD_FONT20.render("Words Typed: "+str(word_score), 1, WHITE)
    cscore = WORD_FONT20.render("Characters Typed: "+str(char_score), 1, WHITE)
    WIN.blit(wscore, (10, 10))
    WIN.blit(cscore, (10, 30))
    pygame.display.update()

# def handle_typing(word, key_press):



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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INPUT_RECT.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN and event.key != pygame.K_RETURN:
                #[:-1 removes \n]
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                print(user_text)

                if user_text == word_text: #if equal to the word make a new word
                    word_score += 1
                    char_score += len(word_text)
                    word_text = random.choice(diction.get_library())[:-1]
                    current_word = WORD_FONT100.render(word_text,1,WHITE)
                    user_text = ''
                # if event.key == pygame.K_RETURN:
                #     new_word = random.choice(diction.get_library())[:-1]
                #     wanted_key_press = pygame.key.key_code(new_word[0])
                #     #make a function that handles these inputs
                #     handle_typing(new_word, event.key)
                #     current_word = WORD_FONT100.render(new_word,1,WHITE)
                #     if wanted_key_press == event.key:
                #         print("YES")
        if not run:
            break
        draw_window(current_word, user_text, word_score, char_score)
    print('Game Over')


if __name__ == "__main__":
    main()
