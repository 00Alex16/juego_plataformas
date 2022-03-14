import pygame as pg
import sys
from pygame.locals import *
from os import path
from settings import *
from objects import *
from map import *

# Variables globales
height_menu_buttons = 60
width_menu_buttons = 125

################################## CREATE CLASS HUD ###############################################
class hud:
    ################################# LOAD HUD ########################################
    def __init__(self, map):
        self.start_coins = len(map.coins)
        self.current_coins = 0
        self.current_time = 0
        self.last_time = pg.time.get_ticks() // 1000
        self.font = pg.font.SysFont(FONT_NAME, 40)
        self.coins = None
        self.time = None

################################## CREATE CLASS GAME ###############################################
class Game:
    def __init__(self):
        ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
        pg.init()
        self.current_level = 1
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pg.time.Clock()
        self.surface.fill(WHITE)
        self.dt = self.clock.tick(60) * .00015 * FPS

    def load_data(self):
        ################################# LOAD PLAYER AND SPRITESHEET###################################
        self.player = Player()
        #################################### LOAD THE LEVEL #######################################
        self.game_folder = path.dirname(__file__)
        self.map_folder = path.join(self.game_folder, 'maps', f"{'level' + str(self.current_level)}")
        self.map_dir = path.join(self.map_folder, f"{'level' + str(self.current_level) + '.tmx'}")
        self.map = TiledMap(self.map_dir)
        self.map_img = self.map.make_map()
        self.player.rect.x, self.player.rect.y = 450, 400
        self.hud = hud(self.map)

    def win(self):
        img = pg.image.load("images/win.png")
        img = pg.transform.scale(img, (WIDTH,HEIGHT))
        sound_win = pg.mixer.Sound('sounds/win.wav')
        sound_win.play()
        self.window.blit(img, (0,0))
        pg.display.flip()
        pg.time.delay(5000)
        if self.current_level == 2:
            self.current_level = 1
            self.menu()
        self.current_level += 1
        self.load_data()

    def lose(self):
        img = pg.image.load("images/lose.png")
        img = pg.transform.scale(img, (WIDTH,HEIGHT))
        sound_lose = pg.mixer.Sound('sounds/lose.wav')
        sound_lose.play()
        self.window.blit(img, (0,0))
        pg.display.flip()
        pg.time.delay(5000)
        self.load_data()

    def events(self):
        ################################# CHECK PLAYER INPUT #################################
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.LEFT_KEY = True
                elif event.key == pg.K_RIGHT:
                    self.player.RIGHT_KEY = True
                elif event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.player.LEFT_KEY = False
                elif event.key == pg.K_RIGHT:
                    self.player.RIGHT_KEY = False
                elif event.key == pg.K_UP:
                    if self.player.is_jumping:
                        self.player.velocity.y *= .25
                        self.player.is_jumping = False

        ################### CHECK IF PLAYER WIN OR LOSE ####################
        if self.player.winner and len(self.map.coins) == 0:
            self.win()
            self.hud.last_time = pg.time.get_ticks() // 1000
        elif self.player.loser:
            self.lose()
            self.hud.last_time = pg.time.get_ticks() // 1000
        else:
            self.player.winner = False

    def update(self):
        ################################# UPDATE/ Animate SPRITE #################################
        self.player.update(self.dt, self.map)
        self.surface.blit(self.map_img, (0, 0))
        for coin in self.map.coins:
            coin.updateSprite()
            self.surface.blit(coin.img, coin.rect)
        for torch in self.map.torchs:
            torch.updateSprite()
            self.surface.blit(torch.img, torch.rect)
        ################################# UPDATE HUD #################################
        if self.hud.start_coins > len(self.map.coins):
            self.hud.current_coins += 1
            self.hud.start_coins -= 1
        self.hud.coins = self.hud.font.render(f'Coins: {self.hud.current_coins}', False, WHITE)
        self.hud.current_time = pg.time.get_ticks()//1000
        self.hud.time = self.hud.font.render(f'Time: {self.hud.current_time - self.hud.last_time}', False, WHITE)
        ################################# UPDATE WINDOW AND DISPLAY #################################
        self.player.draw(self.surface)
        self.surface.blit(self.hud.coins, (10, 10))
        self.surface.blit(self.hud.time, (1190, 10))
        self.window.blit(self.surface, (0,0))
        pg.display.flip()

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        result = False

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(self.surface, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                if action == Game:
                    result = True
                else:
                    result = action() 
        else:
            pg.draw.rect(self.surface, ic,(x,y,w,h))

        smallText = pg.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText, WHITE)
        textRect.center = ( (x+(w//2)), (y+(h//2)) )
        self.surface.blit(textSurf, textRect)

        return result

    def quitgame(self):
        pg.quit()
        sys.exit()

    def instructions(self):
        pg.display.set_caption("Instructions")
        img = pg.image.load("images/instructions.png")
        img = pg.transform.scale(img, (WIDTH, HEIGHT))
        self.surface.fill(WHITE)
        self.surface.blit(img, (0,0))

        return True

    def menu(self):
        pg.display.set_caption("The Game")

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.surface.fill(BLUE)

            titleText = pg.font.SysFont(FONT_NAME, 72)

            title, titleRect = self.text_objects('The Game', titleText, BLACK)

            titleRect.center = ((WIDTH // 2), HEIGHT // 5)

            self.surface.blit(title, titleRect)

            play_button = self.button('Play', (WIDTH - width_menu_buttons) // 2, (HEIGHT // 2) - (height_menu_buttons + 20), width_menu_buttons, height_menu_buttons, BGCOLOR, RED, Game)
            instructions_button = self.button('Instructions', (WIDTH - width_menu_buttons) // 2, HEIGHT // 2, width_menu_buttons, height_menu_buttons, BGCOLOR, RED, self.instructions)
            if not instructions_button:
                exit_button = self.button('Exit', (WIDTH - width_menu_buttons) // 2, (HEIGHT // 2) + (height_menu_buttons) + 20, width_menu_buttons, height_menu_buttons, BGCOLOR, RED, self.quitgame)

            self.window.blit(self.surface, (0, 0))

            pg.display.flip()

            if instructions_button:
                pg.time.wait(10000)
            elif play_button:
                break

           
if __name__ == '__main__':
    ################################ CREATE GAME #########################
    g = Game()

    ################################ SHOW MENU ###########################
    g.menu()

    ################################ LOAD LEVEL ##########################
    g.load_data()

    ################################ DRAW LEVEL ##########################
    g.update()

    ################################# GAME LOOP ##########################
    while g.running:
        g.events()
        if g.player.loser == False:
            g.update()