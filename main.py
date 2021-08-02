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

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)



def draw_window(current_word):
    WIN.fill(BLACK)
    WIN.blit(current_word,(WIN_W/2 - current_word.get_width()/2,
        WIN_H/2 - current_word.get_height()/2))

    pygame.display.update()


def main():
    pygame.display.set_caption("Typing Game")
    diction = wl.Word_Library('words_alpha.txt')

    current_word = WORD_FONT100.render("Enter to start",1,WHITE)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break;

            if event.type == pygame.KEYDOWN:
                #[:-1 removes \n]
                new_word = random.choice(diction.get_library())[:-1]
                wanted_key_press = pygame.key.key_code(new_word[0])
                if wanted_key_press in pygame.key.get_pressed():
                    print("YES")
                if event.key == pygame.K_RETURN:
                    current_word = WORD_FONT100.render(new_word,1,WHITE)
        if not run:
            break;
        draw_window(current_word)
    print('Game Over')




if __name__ == "__main__":
    main()
