import pygame
import sys
import time
from sudoku import Sudoku

def main(file):
    #Create game
    pygame.init()
    size = WIDTH, HEIGHT, PAD = 450, 450, 100
    screen = pygame.display.set_mode((WIDTH, HEIGHT+PAD))

    #Colors
    BLACK = (0, 0, 0)
    white = (180, 180, 180)
    WHITE = (255, 255, 255)

    #Game State
    Game = None
    started = False
    
    #fonts
    font = pygame.font.Font("assets/OpenSans-Regular.ttf", 28)

    running = True

    while running:

        #Check if Ended
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit();

        screen.fill(BLACK)

        #Show start menu
        if not started:
            buttonRect = pygame.Rect(WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2)
            buttonText = font.render("Start", True, BLACK)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(screen, WHITE, buttonRect)
            screen.blit(buttonText, buttonTextRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if buttonRect.collidepoint(mouse):
                    started = True
                    Game = Sudoku(file)
                    time.sleep(0.3)
            pygame.display.flip()
            continue
            
        #draw board
        for j in range (9):
            for i in range(9):
                cell = pygame.Rect(int(i*HEIGHT/9), int(j*WIDTH/9), int(WIDTH/9), int(HEIGHT/9))
                pygame.draw.rect(screen, BLACK, cell)
                if Game.isset(i, j):
                    cellText = font.render(str(Game.board[i, j]+1), True, WHITE)
                    cellTextRect = cellText.get_rect()
                    cellTextRect.center = cell.center
                    screen.blit(cellText, cellTextRect)
                pygame.draw.rect(screen, WHITE, cell, 1)
        for i in range(0, HEIGHT, int(HEIGHT/3)):
            for j in range(0, WIDTH, int(WIDTH/3)):
                rect = pygame.Rect(j, i, int(WIDTH)/3, int(HEIGHT/3))
                pygame.draw.rect(screen, WHITE, rect, 4)
        nextbut = pygame.Rect(int(WIDTH/2/4), HEIGHT+int(PAD/3), int(WIDTH/2   /2), int(PAD/3))
        nextbutText = font.render("Next", True, BLACK)
        nextbutTextRect = nextbutText.get_rect()
        nextbutTextRect.center = nextbut.center
        pygame.draw.rect(screen, WHITE, nextbut)
        screen.blit(nextbutText, nextbutTextRect);
        restartbut = pygame.Rect(int(WIDTH*5/8), HEIGHT+int(PAD/3), int(WIDTH/2/2), int(PAD/3))
        restartbutText = font.render("Restart", True, BLACK)
        restartbutTextRect = restartbutText.get_rect()
        restartbutTextRect.center = restartbut.center
        pygame.draw.rect(screen, WHITE, restartbut)
        screen.blit(restartbutText, restartbutTextRect)
        pygame.display.flip()

        if len(Game.fixed) == 81:
            print('Game has ended')
            break

        #clicks
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if nextbut.collidepoint(mouse):
                Game.makemove()
            elif restartbut.collidepoint(mouse):
                print('RESTART')
                started = False
                continue
            time.sleep(0.2)

if __name__ == '__main__':
    #try:
    file = sys.argv[1] if len(sys.argv)>1 else 'puzzle.txt'
    main(file)
    #except Exception as e:
    #    input(e)
