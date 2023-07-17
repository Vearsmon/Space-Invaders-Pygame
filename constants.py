import os

LASER_WIDTH = 10
LASER_HEIGHT = 30
BLACK = (0, 0, 0)
HEIGHT = 960
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_LASER_SPD = -30
PLAYER_SPD = 8
WHITE = (255, 255, 255)
WIDTH = 1080
ALIEN_WIDTH = 60
ALIEN_HEIGHT = 40
ALIEN_HORIZONTAL_GAPS = 5
ALIEN_VERTICAL_GAPS = 5
ALIEN_SPD = 2
ALIEN_LASER_SPD = 6
FPS = 60
WALL_WIDTH = 15
WALL_HEIGHT = 15
ALIEN_COLS = 11
ALIEN_ROWS = 5
APPROACH_SPD = 8
WALL_COUNT = 4
WALL_GAPS = 80
POINTS_PER_ALIEN = 10

WALL_SHAPE = [
    '  XXXXXXX  ',
    ' XXXXXXXXX ',
    'XXXXXXXXXXX',
    'XXXXXXXXXXX',
    'XXXXXXXXXXX',
    'XXX     XXX',
    'XX       XX'
]

game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, 'sprites')
images_folder = os.path.join(sprites_folder, 'images')
laser_image_1 = os.path.join(images_folder, 'laser_type_1.png')
ship_image_1 = os.path.join(images_folder, 'ship_type_1.png')
alien_image_1 = os.path.join(images_folder, 'alien_type_1.png')
alien_image_2 = os.path.join(images_folder, 'alien_type_2.png')
alien_image_3 = os.path.join(images_folder, 'alien_type_3.png')
wall_image = os.path.join(images_folder, 'wall.png')
background_image = os.path.join(images_folder, 'background.png')
bonus_image = os.path.join(images_folder, 'bonus_alien.png')
