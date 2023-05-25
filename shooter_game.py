from pygame import *
from random import randint
from time import time as timer
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15,20,15)
        bullets.add(bullet)

lost = 0
score = 0
life = 99
num_fire = 0
real_time = False
fire_sound = mixer.Sound('fire.ogg')

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()



img_bullet = 'bullet.png'
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load('galaxy.jpg'),
    (win_width, win_height))

raketa = Player('rocket.png',50,400,80,65,10)

monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,7))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
font.init()
font2 = font.SysFont('Arial', 26)
font3 = font.SysFont('Arial', 36)
font10 = font.SysFont('Arial', 20)
finish = False
run = True

bullets = sprite.Group()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    raketa.fire()
                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True
    if not finish:
        window.blit(background,(0,0))
        
        raketa.reset()
        raketa.update()

        monsters.draw(window)
        monsters.update()

        bullets.update()
        bullets.draw(window)
        
        asteroids.update()
        asteroids.draw(window)
        text_lose = font2.render("Пропущено:" + str(lost), 1 ,(255,255,255))
    
        scored = font2.render("Счет:" + str(score),1, (255,255,255))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        if real_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload1 = font2.render('Wait, reload...',1,(150,0,0))
                window.blit(reload1, (260,460))
            else:
                num_fire = 0
                real_time = False       
        for i in sprites_list:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,7))
            monsters.add(monster)
        window.blit(text_lose,(0,0))
        window.blit(scored,(0,30))
        if sprite.spritecollide(raketa,monsters, False) or sprite.spritecollide(raketa,asteroids, False):
            sprite.spritecollide(raketa, asteroids, True)
            sprite.spritecollide(raketa, monsters, True)
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,7))
            monsters.add(monster)
            asteroid = Enemy('asteroid.png', randint(30, win_width - 30),-40,80,50,randint(1,7))
            asteroids.add(asteroid)
            life -= 1
        if score >= 10:
            text_win = font3.render("PABEDA", 1 ,(255,255,255))
            window.blit(text_win,(100,50))
            finish = True
        if life == 0 or lost >= 90:
            text_sack = font3.render("GG", 1 ,(255,255,255))
            window.blit(text_sack,(100,50))
            finish = True
        if life >= 3:
            life_color = (0,150,0)
        if life >= 2:
            life_color = (150,150,0)  
        if life >= 1:
            life_color = (150,0,0)
        text_life = font10.render(str(life),1, life_color)
        window.blit(text_life, (650,10))
        display.update()
    time.delay(15)
    display.update()
