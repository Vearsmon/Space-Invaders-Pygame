import pygame
import os
import Game
from constants import WHITE, BLACK, WIDTH, HEIGHT, background_image

pygame.init()

ARIAL_50 = pygame.font.SysFont('arial', 50)
menu_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


def accept_and_start(username):
    game = Game.Game(username)
    game.run()


def run_name_insertion_menu():
    current_button_index = 0
    buttons = ['ACCEPT']
    running = True
    username = ''
    while running:
        menu_screen.fill(BLACK)
        background = pygame.image.load(background_image).convert()
        menu_screen.blit(background, background.get_rect())
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    running = False
                    accept_and_start(username)
                if e.key == pygame.K_BACKSPACE:
                    if len(username) > 0:
                        username = username[:-1]
                else:
                    try:
                        if chr(e.key) in '1234567890qwertyuiopasdfghjklzxcvbnm':
                            username += chr(e.key).upper()
                    except:
                        pass
        draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 100, 'ENTER YOUR NAME:')
        draw_text(menu_screen, WIDTH / 2, HEIGHT / 2 - 25, username)
        draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 + 50, 75)
        pygame.display.flip()


def run_leaderboard_menu():
    leaderboard = []
    with open(os.path.join(os.path.dirname(__file__), 'records.txt'), 'r') as f:
        records = f.readlines()
        for record in records:
            if record != '\n':
                leaderboard.append(record)
        leaderboard = sorted(leaderboard, key=lambda rec: int(rec.split(':')[1].strip()), reverse=True)

    current_button_index = 0
    buttons = ['BACK TO MENU']
    running = True
    while running:
        menu_screen.fill(BLACK)
        background = pygame.image.load(background_image).convert()
        menu_screen.blit(background, background.get_rect())

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_ESCAPE:
                    running = False
                    run_main_menu()
        if not running:
            break
        draw_text(menu_screen, WIDTH / 2, 50, 'TOP 10 PLAYERS')
        for i, option in enumerate(leaderboard):
            if i > 9:
                break
            draw_text(menu_screen, WIDTH / 2, 50 + (i+1)*75, (str(i + 1) + '. ' + option)
                      .replace('\n', '')
                      .replace('\'s record', ''))
        draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT - 50, 75)
        pygame.display.flip()


def run_main_menu():
    current_button_index = 0
    buttons = ['START GAME', 'LEADERBOARD', 'QUIT']
    options = [lambda: run_name_insertion_menu(), lambda: run_leaderboard_menu(), lambda: exit()]
    running = True
    while running:
        menu_screen.fill(BLACK)
        background = pygame.image.load(background_image).convert()
        menu_screen.blit(background, background.get_rect())
        draw_text(menu_screen, WIDTH / 2, 150, '=SPACE INVADERS=')
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    current_button_index = max(0, min(current_button_index - 1, len(buttons) - 1))
                if e.key == pygame.K_s:
                    current_button_index = max(0, min(current_button_index + 1, len(buttons) - 1))
                if e.key == pygame.K_SPACE:
                    running = False
                    options[current_button_index]()
                if e.key == pygame.K_ESCAPE:
                    exit()
        draw_buttons(buttons, menu_screen, current_button_index, WIDTH / 2, HEIGHT / 2 - 100, 75)
        pygame.display.flip()


def draw_buttons(buttons, surf, current_button_index, x, y, option_y_padding):
    for i, button_text in enumerate(buttons):
        button_surf = ARIAL_50.render(button_text, True, WHITE)
        button_rect = button_surf.get_rect()
        button_rect.center = (x, y + i * option_y_padding)
        if i == current_button_index:
            pygame.draw.rect(surf, BLACK, button_rect)
        surf.blit(button_surf, button_rect)


def draw_text(surf, x, y, text):
    text_surf = ARIAL_50.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surf, text_rect)
