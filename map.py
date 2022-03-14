from os import name
import pygame as pg
import pytmx
from objects import *
from settings import *

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.rocks = pg.sprite.Group()
        self.lava = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.torchs = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()

    def render(self, surface):
        # draw map data on screen
        for object in self.tmxdata.objects:
            if object.name == 'Rock':
                rock = Rock(object.x, object.y, object.width, object.height)
                self.rocks.add(rock)
                self.allSprites.add(rock)
            elif object.name == 'Lava':
                lava = Lava(object.x, object.y, object.width, object.height)
                self.lava.add(lava)
                self.allSprites.add(lava)
            elif object.name == 'Coin':
                coin = Coin(object.x, object.y)
                self.coins.add(coin)
                self.allSprites.add(coin)
                continue
            elif object.name == "Torch":
                torch = Torch(object.x, object.y)
                self.torchs.add(torch)
                continue
            elif object.name == 'Chest':
                chest = Chest(object.x, object.y, object.width, object.height)
                self.allSprites.add(chest)
                continue

            if object.image:

                img = object.image
                
                if object.width > 64 or object.height > 64:
                    img = pg.transform.scale(object.image, (int(object.width), int(object.height)))

                surface.blit(img, (int(object.x), int(object.y)))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface