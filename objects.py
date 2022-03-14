import pygame as pg
from settings import *
vec = pg.math.Vector2

class Rock(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)

class Lava(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)

class Chest(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(x, y, width, height)

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = list()
        for i in range(1, 11):
            img = pg.image.load(f"{'images/Items/coin' + str(i) + '.png'}")
            self.images.append(img)
        self.figure = 0
        self.img = self.images[self.figure]
        self.rect = self.img.get_rect()
        self.rect.top = y
        self.rect.left = x
    
    def get_figure(self, states):
        self.figure += 1
        if self.figure >= (len(states)):
            self.figure = 0
        return states[self.figure]
    
    def updateSprite(self):
        self.img = self.get_figure(self.images)

class Torch(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.images = list()
        for i in range(1, 5):
            img = pg.image.load(f"{'images/Details/torch2_' + str(i) + '.png'}")
            self.images.append(img)
        self.figure = 0
        self.img = self.images[self.figure]
        self.rect = self.img.get_rect()
        self.rect.top = y + 10
        self.rect.left = x
    
    def get_figure(self, states):
        self.figure += 1
        if self.figure >= (len(states)):
            self.figure = 0
        return states[self.figure]
    
    def updateSprite(self):
        self.img = self.get_figure(self.images)

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.player = pg.image.load('images/character.png')
        self.player.set_clip(pg.Rect(0,0,52,76))
        self.clipping = self.player.subsurface(self.player.get_clip())
        self.rect = self.clipping.get_rect()
        self.rect.height -= 16
        self.position, self.velocity = pg.math.Vector2(0,0), pg.math.Vector2(0,0)
        self.acceleration = pg.math.Vector2(0,self.gravity)
        self.figure = 0
        self.statesLeft = {0: (5,78,47,54), 1: (73,78,47,54), 2: (210,78,47,54)}
        self.statesRight = {0: (5,150,47,54), 1: (78,150,47,54), 2: (217,150,47,54)}
        self.statesUp = {0: (10,220,47,54), 1: (77,220,47,54), 2: (217,220,47,54)}
        self.statesDown = {0: (10,5,47,54), 1: (75,5,47,54), 2: (213,5,47,54) }
        self.loser = False
        self.winner = False

    def draw(self, display):
        display.blit(self.clipping, self.rect)

    def update(self, dt, objects):
        self.horizontal_movement(dt)
        self.checkCollisionsx(objects)
        self.vertical_movement(dt)
        self.checkCollisionsy(objects)

    def get_figure(self, states):
        self.figure += 1
        if self.figure >= (len(states)):
            self.figure = 0
        return states[self.figure]
    
    def cut(self, rectClipping):
        if type(rectClipping) is dict:
            self.player.set_clip(pg.Rect(self.get_figure(rectClipping)))
        else:
            self.player.set_clip(pg.Rect(rectClipping))
        return rectClipping

    def updateSprite(self, direction):
        if direction == "left":
            self.cut(self.statesLeft)
            self.rect.x -= self.velocity.x
        elif direction == "right":
            self.cut(self.statesRight)
            self.rect.x += self.velocity.x
        elif direction == "stopLeft":
            self.cut(self.statesLeft[0])
        elif direction == "stopRight":
            self.cut(self.statesRight[0])

        self.clipping = self.player.subsurface(self.player.get_clip())

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
            self.updateSprite('left')
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
            self.updateSprite('right')
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def get_hits(self, map):
        hits = []
        for object in map.allSprites:
            if self.rect.colliderect(object):
                if type(object) == Lava:
                    self.loser = True
                    continue
                elif type(object) == Coin:
                    sound_coin = pg.mixer.Sound('sounds/coin.wav')
                    sound_coin.play()
                    map.allSprites.remove(object)
                    map.coins.remove(object)
                    continue
                elif type(object) == Chest:
                    self.winner = True
                    continue
                else:
                    hits.append(object)
        return hits

    def checkCollisionsx(self, objects):
        collisions = self.get_hits(objects)
        for object in collisions:
            if self.velocity.x > 0:  # Hit object moving right
                self.position.x = object.rect.left - self.rect.w
                self.rect.x = self.position.x
                self.figure = 2
                self.updateSprite('right')
            elif self.velocity.x < 0:  # Hit object moving left
                self.position.x = object.rect.right
                self.rect.x = self.position.x
                self.figure = 2
                self.updateSprite('left')

    def checkCollisionsy(self, objects):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(objects)
        for object in collisions:
            if self.velocity.y > 0:  # Hit object from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = object.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit object from the bottom
                self.velocity.y = 0
                self.position.y = object.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
