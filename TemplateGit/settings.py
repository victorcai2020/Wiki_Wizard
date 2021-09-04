import pygame as pg
vec = pg.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BEIGE = (240, 230, 140)

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Wiki Wizard"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_HEALTH = 100
PLAYER_SPEED = 350
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'wiki.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
WAND_OFFSET = vec(30, 12.5)

SPELL_IMG = 'spell.png'
SPELL_SPEED = 500
SPELL_LIFETIME = 1900
SPELL_RATE = 350
KICKBACK = 5
WAND_SPREAD = 15
SPELL_DAMAGE = 10


MOB_IMG = 'monster.png'
MOB_SPEEDS = [125, 125, 125, 150, 150, 175]
MOB_HIT_RECT = pg.Rect(0, 0, 35, 35)
MOB_HEALTH = 50
MOB_DAMAGE = 5
MOB_KNOCKBACK = 20
AVOID_RADIUS = 75
DETECT_RADIUS = 300
ROCK = 'rock.png'

WAND_FLASHES = ['magic_03.png', 'magic_04.png', 'magic_05.png']
FLASH_DURATION = 100
DAMAGE_ALPHA = [i for i in range(0, 255, 20)]

WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
SPELL_LAYER = 3
EFFECTS_LAYER = 4


ITEM_IMAGES = {'health': 'health.png'}
HEALTH_PACK_AMOUNT = 10
BOB_RANGE = 15
BOB_SPEED = 0.4

BG_MUSIC = 'Forest 03.ogg'
SPELL_SOUND = ['Spell_01.mp3']

LOGO = 'pygame_powered.gif'
