#Создай собственный Шутер!

from pygame import *
mixer.init()
font.init()
from random import randint


#Окно игры
window = display.set_mode((700, 500))
display.set_caption('Shooter')

lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, w, h, img, x, y, speed = 0):
        super().__init__()
        self.width = w
        self.height = h
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.right = True
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(50, 50, 'bullet.png', self.rect.x, self.rect.y, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.speed = randint(0, 3)
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            x = randint(100, 550)
            self.rect.x = x
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

#Фон сцены
bg = transform.scale(image.load('galaxy.jpg'), (900, 600))

#Спрайт

font1 = font.SysFont('Arial', 50)

rocket = Player(90, 110, 'rocket.png', 280, 380, 5)

ufos = sprite.Group()
for i in range(6):
    x = randint(100, 550)
    ufo = Enemy(120, 80, 'ufo.png', x, 0, 2)
    ufos.add(ufo)

bullets = sprite.Group()

#Музыка
mixer.music.load('space.ogg')
mixer.music.play()

kick = mixer.Sound('fire.ogg')

run = True
finish = False
clock = time.Clock()
FPS = 60
font2 = font.SysFont('Arial', 60)

while run:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                kick.play()
    
    if not finish:
        window.blit(bg, (0, 0))
        lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(lose, (10, 10))
        rocket.reset()
        rocket.move()
        
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        sprites_group = sprite.groupcollide(ufos, bullets, True, True)
        if sprites_group:
            score += 1
            x = randint(100, 550)
            ufo = Enemy(120, 80, 'ufo.png', x, 0, 2)
            ufos.add(ufo)
        count = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(count, (10, 50))

    if score >= 10:
        win = font2.render('Ты выиграл!!!', True, (255, 255, 255))
        window.blit(win, (200, 200))
        finish = True

    if lost >= 3:
        gameover = font2.render('Ты проиграл!!!', True, (255, 255, 255))
        window.blit(gameover, (200, 200))
        finish = True

    sprites_list = sprite.spritecollide(rocket, ufos, False)
    if sprites_list:
        gameover = font2.render('Ты проиграл!!!', True, (255, 255, 255))
        window.blit(gameover, (200, 200))
        finish = True

    display.update()