import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from time import sleep

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        img_folder = path.join(self.game_folder, 'img')
        music_folder = path.join(self.game_folder, 'music')
        snd_folder = path.join(self.game_folder, 'snd')
        self.title_font = path.join(img_folder, 'font.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((BEIGE))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.spell_img = pg.image.load(path.join(img_folder, SPELL_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.rock = pg.image.load(path.join(img_folder, ROCK)).convert_alpha()
        self.rock = pg.transform.scale(self.rock, (30, 30))
        self.logo = pg.image.load(path.join(img_folder, LOGO)).convert_alpha()
        self.wand_flashes = []
        for img in WAND_FLASHES:
            self.wand_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.wand_sounds = {}
        self.wand_sounds['wand'] = []
        for snd in SPELL_SOUND:
            self.wand_sounds['wand'].append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.spells = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.game_folder, 'ForgottenPath.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 7,
                             tile_object.y + tile_object.height / 7)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'monster':
                Monster(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
        # self.player = Player(self, 5, 5)
        self.paused = False
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.mobs) == 0:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)

        hits = pg.sprite.groupcollide(self.mobs, self.spells, False, True)
        for hit in hits:
            hit.health -= SPELL_DAMAGE
            hit.vel = vec(0, 0)

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)

        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def check_mobs(self):
        pg.fill(BEIGE)

    def draw(self):
        pg.display.set_caption('Wiki Wizard')
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            if isinstance(sprite, Monster):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('MONSTERS: {}'.format(len(self.mobs)), self.title_font, 30, WHITE,  WIDTH - 10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.screen.blit(self.logo, (10, 650))
            self.draw_text('WIKI WIZARD', self.title_font, 50, BLACK, WIDTH / 2, HEIGHT / 3, align="center")
            self.draw_text('GAME PAUSED', self.title_font, 105, BLACK, WIDTH / 2, HEIGHT / 2, align="s")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        self.screen.fill(BEIGE)
        self.draw_text("WIKI WIZARD", self.title_font, 100, BLACK, WIDTH / 2, HEIGHT / 3, align="n")
        self.draw_text('PRESS A KEY TO START', self.title_font, 75, BLACK, WIDTH / 2, HEIGHT / 2, align='center')
        self.screen.blit(self.logo, (10, 650))
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if len(self.mobs) == 0:
            self.screen.fill(BEIGE)
            self.draw_text("LEVEL CLEARED", self.title_font, 100, BLACK, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text('PRESS A KEY TO START', self.title_font, 75, BLACK, WIDTH / 2, HEIGHT * 3 / 4, align='center')
            pg.display.flip()
            self.wait_for_key()
        if self.player.health == 0:
            self.screen.fill(BEIGE)
            self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
            self.draw_text('PRESS A KEY TO START', self.title_font, 75, RED, WIDTH / 2, HEIGHT *3 / 4, align='center')
            pg.display.flip()
            self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait(1000)
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()