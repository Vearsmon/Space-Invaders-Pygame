import pygame
import os
import random
import Ship
import Alien
import Wall
import Menu
from constants import WIDTH, HEIGHT, FPS, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_COLS, ALIEN_ROWS, ALIEN_VERTICAL_GAPS, \
    ALIEN_HORIZONTAL_GAPS, APPROACH_SPD, WALL_COUNT, WALL_WIDTH, WALL_HEIGHT, WALL_GAPS, WALL_SHAPE, BLACK, \
    alien_image_1, alien_image_2, alien_image_3, background_image


class Game:
    def __init__(self, username):
        self.running = True
        self.username = username
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.game_folder = os.path.dirname(__file__)
        if not os.path.isfile(os.path.join(self.game_folder, 'records.txt')):
            my_file = open(os.path.join(self.game_folder, 'records.txt'), "w+")
            my_file.close()
        self.background_image = pygame.image.load(background_image).convert()
        self.ship = Ship.Ship(WIDTH / 2, HEIGHT * 0.9)
        self.ship_group = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ship_laser = pygame.sprite.Group()
        self.alien_laser = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bonus_alien = pygame.sprite.Group()
        self.alien_speed = 1
        self.alien_approach_speed = 0
        self.levels = [self.load_level_1, self.load_level_2, self.load_level_3]
        self.current_level = 0
        self.score = 0
        self.should_spawn_bonus = True
        self.alien_timer = random.randint(50, 150)
        self.bonus_timer = random.randint(400, 800)
        self.font = pygame.font.match_font('arial')
        self.win = False
        self.exit = False

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= WIDTH:
                self.alien_speed = -1
                self.alien_approach_speed = APPROACH_SPD
            elif alien.rect.left <= 0:
                self.alien_speed = 1
                self.alien_approach_speed = APPROACH_SPD

    def update_game_cycle(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, self.background_image.get_rect())
        self.ship_group.update()
        self.alien_position_checker()
        self.aliens.update((ALIEN_COLS * ALIEN_ROWS) / (len(self.aliens) + 1) * 0.5,
                           self.alien_speed, self.alien_approach_speed)
        self.alien_approach_speed = 0
        self.ship_laser.update()
        self.walls.update()
        self.alien_laser.update()
        self.bonus_alien.update()
        self.alien_timer -= 1
        self.bonus_timer -= 1

    def draw_sprites(self):
        self.ship_group.draw(self.screen)
        self.aliens.draw(self.screen)
        self.ship_laser.draw(self.screen)
        self.walls.draw(self.screen)
        self.alien_laser.draw(self.screen)
        self.bonus_alien.draw(self.screen)

    def check_collision(self):
        hits = pygame.sprite.groupcollide(self.ship_laser, self.walls, True, False)
        for hit in hits.values():
            for wall in hit:
                wall.kill()
                self.walls.remove(wall)
        hits = pygame.sprite.groupcollide(self.alien_laser, self.walls, True, False)
        for hit in hits.values():
            for wall in hit:
                wall.kill()
                self.walls.remove(wall)
        pygame.sprite.groupcollide(self.alien_laser, self.ship_laser, True, True)
        hits = pygame.sprite.groupcollide(self.bonus_alien, self.ship_laser, True, True)
        if hits:
            self.should_spawn_bonus = False
            self.score += 500
        hits = pygame.sprite.spritecollide(self.ship, self.aliens, False)
        if hits:
            self.ship.live_count -= 1
            if self.ship.live_count <= 0:
                self.running = False
                self.write_record()
                Menu.run_main_menu()
        if len(self.aliens) == 0:
            self.show_win_screen()
        hits = pygame.sprite.groupcollide(self.ship_laser, self.aliens, True, True)
        for hit in hits.values():
            for alien in hit:
                self.score += alien.cost
        hits = pygame.sprite.groupcollide(self.ship_group, self.alien_laser, False, True)
        if hits:
            self.ship.live_count -= 1
            if self.ship.live_count <= 0:
                self.running = False
                self.write_record()
                Menu.run_main_menu()

    def spawn_aliens(self, alien_rows, alien_cols):
        if ALIEN_COLS % 2 == 0:
            aliens_start_pos = WIDTH / 2 - (ALIEN_COLS / 2 - 0.5) * (ALIEN_WIDTH + ALIEN_HORIZONTAL_GAPS)
        else:
            aliens_start_pos = WIDTH / 2 - (ALIEN_COLS / 2 - 0.5) * (ALIEN_WIDTH + ALIEN_HORIZONTAL_GAPS)
        for i in range(alien_rows):
            for j in range(alien_cols):
                spawn_pos_x = aliens_start_pos + j * (ALIEN_WIDTH + ALIEN_HORIZONTAL_GAPS)
                spawn_pos_y = i * (ALIEN_HEIGHT + ALIEN_VERTICAL_GAPS) + HEIGHT / 8
                if i == 0:
                    m = Alien.Alien(spawn_pos_x, spawn_pos_y, pygame.image.load(alien_image_1).convert(), 30)
                if 1 <= i <= 2:
                    m = Alien.Alien(spawn_pos_x, spawn_pos_y, pygame.image.load(alien_image_2).convert(), 20)
                if i > 2:
                    m = Alien.Alien(spawn_pos_x, spawn_pos_y, pygame.image.load(alien_image_3).convert(), 10)
                self.aliens.add(m)

    def spawn_walls(self):
        if WALL_COUNT % 2 == 0:
            walls_start_pos = WIDTH / 2 - (WALL_COUNT / 2 - 0.5) * WALL_GAPS - WALL_WIDTH * len(WALL_SHAPE[0]) * \
                              WALL_COUNT / 2 + WALL_WIDTH / 2
        else:
            walls_start_pos = WIDTH / 2 - int(WALL_COUNT / 2) * WALL_GAPS - WALL_WIDTH * len(WALL_SHAPE[0]) * \
                                WALL_COUNT / 2 + WALL_WIDTH / 2
        for wall in range(WALL_COUNT):
            line_number = 0
            for line in WALL_SHAPE:
                char_number = 0
                for char in line:
                    if char == 'X':
                        next_wall_pos = walls_start_pos + wall * (len(line) * WALL_WIDTH + WALL_GAPS)
                        w = Wall.Wall(next_wall_pos + char_number * WALL_WIDTH, HEIGHT * 0.6 + line_number *
                                      WALL_HEIGHT)
                        self.walls.add(w)
                    char_number += 1
                line_number += 1

    def pause_game(self):
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_pause = False
                    if event.key == pygame.K_x:
                        self.write_record()
                        is_pause = False
                        Menu.run_main_menu()
                        self.running = False
            Menu.draw_text(self.screen, WIDTH / 2, HEIGHT / 2 - 150, 'PAUSE')
            Menu.draw_text(self.screen, WIDTH / 2 - 5, HEIGHT / 2 - 75, '\'ESC\' - BACK TO GAME')
            Menu.draw_text(self.screen, WIDTH / 2 - 10, HEIGHT / 2, '\'X\' - MENU')
            pygame.display.flip()

    def show_win_screen(self):
        is_pause = True
        self.win = True
        while is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.write_record()
                        is_pause = False
                        Menu.run_main_menu()
                        self.running = False
                    if event.key == pygame.K_e:
                        if self.current_level + 1 < len(self.levels):
                            self.levels[self.current_level + 1]()
                            self.current_level += 1
                            is_pause = False
                        else:
                            self.write_record()
                            is_pause = False
                            Menu.run_main_menu()
                            self.running = False
            Menu.draw_text(self.screen, WIDTH / 2, HEIGHT / 2 - 150, 'YOU WIN!')
            Menu.draw_text(self.screen, WIDTH / 2 - 5, HEIGHT / 2 - 75, '\'ESC\' - MENU')
            Menu.draw_text(self.screen, WIDTH / 2 - 10, HEIGHT / 2,'\'E\' - NEXT LEVEL')
            pygame.display.flip()

    def write_record(self):
        records = open(os.path.join(self.game_folder, 'records.txt'), 'r').readlines()
        found = False
        for record in records:
            if record != '\n':
                if self.username in record and int(record.split(':')[1].strip()) < self.score:
                    with open(os.path.join(self.game_folder, 'records.txt'), 'r') as f:
                        old_data = f.read()
                    new_data = old_data.replace(record, record.split(':')[0].strip() + ': ' + str(self.score) + '\n')
                    with open(os.path.join(self.game_folder, 'records.txt'), 'w') as f:
                        f.write(new_data)
                    found = True
        if not found:
            with open(os.path.join(self.game_folder, 'records.txt'), 'r') as f:
                old_data = f.read()
            new_data = old_data + self.username + '\'s record: ' + str(self.score) + '\n'
            with open(os.path.join(self.game_folder, 'records.txt'), 'w') as f:
                f.write(new_data)

    def make_sprite_groups(self):
        self.aliens = pygame.sprite.Group()
        self.ship_laser = pygame.sprite.Group()
        self.alien_laser = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bonus_alien = pygame.sprite.Group()
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_game()
                if event.key == pygame.K_SPACE and len(self.ship_laser) == 0:
                    self.ship_laser.add(self.ship.shoot_ship_laser())
            if event.type == pygame.MOUSEBUTTONDOWN and len(self.ship_laser) == 0:
                if event.button == 1:
                    self.ship_laser.add(self.ship.shoot_ship_laser())

    def choose_shooting_alien(self):
        if self.aliens.sprites():
            shooting_alien = random.choice(self.aliens.sprites())
            if self.alien_timer <= 0:
                self.alien_laser.add(shooting_alien.shoot_alien_laser())
                self.alien_timer = random.randint(50, 150)

    def spawn_bonus_alien(self):
        if not self.bonus_alien.sprites() and self.should_spawn_bonus:
            if self.bonus_timer <= 0:
                if random.randint(1, 2) % 2 == 0:
                    bonus_alien = Alien.Bonus(WIDTH + ALIEN_WIDTH, HEIGHT / 10, direction=-1)
                else:
                    bonus_alien = Alien.Bonus(-ALIEN_WIDTH, HEIGHT / 10, direction=1)
                self.bonus_alien.add(bonus_alien)
                self.should_spawn_bonus = False
                self.bonus_timer = random.randint(400, 800)
        else:
            for bonus in self.bonus_alien:
                if bonus.rect.right <= -ALIEN_WIDTH - 1 or bonus.rect.left >= WIDTH + ALIEN_WIDTH + 1:
                    self.should_spawn_bonus = False
                    self.bonus_alien.remove(bonus)
                    bonus.kill()
            self.bonus_timer = random.randint(400, 800)

    def run_game(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.check_events()
            self.choose_shooting_alien()
            self.spawn_bonus_alien()
            self.update_game_cycle()
            self.draw_sprites()
            self.check_collision()
            if self.win:
                self.win = False
                return
            Menu.draw_text(self.screen, WIDTH / 2, 32, str(self.score))
            Menu.draw_text(self.screen, 20, 32, str(self.ship.live_count))
            pygame.display.flip()
        pygame.quit()

    def load_level_1(self):
        self.make_sprite_groups()
        self.spawn_aliens(5, 5)
        self.spawn_walls()
        self.run_game()
        return

    def load_level_2(self):
        self.make_sprite_groups()
        self.spawn_aliens(6, 8)
        self.spawn_walls()
        self.run_game()
        return

    def load_level_3(self):
        self.make_sprite_groups()
        self.spawn_aliens(7, 11)
        self.spawn_walls()
        self.run_game()
        return

    def run(self):
        self.levels[0]()
