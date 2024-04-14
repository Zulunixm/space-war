from pygame import *
from random import randint
win_width = 700
win_height = 500

img_back = 'galaxy.jpg'
img_ship = 'rocket.png'
img_bullet = 'bullet.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, p_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
score = 0 
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont("verdana",36)

bullets = sprite.Group()
ship = player("rocket.png", 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(3):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
for i in range(2):
    monster = Enemy("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back),(win_width, win_height))

finish = False
run = True
clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))
        luser_text = font2.render('Пропущено:'+str(lost), 1, (255,255,255))
        window.blit(luser_text, (10, 50))

        text = font2.render('Cчет:'+str(score), 1, (255,255,255))
        window.blit(text, (10, 20))  

        ship.update()

        bullets.update()
        monsters.update()

        ship.reset()

        monsters.draw(window)
        bullets.draw(window)

        display.update()
    time.delay(50)