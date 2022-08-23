# Разработай свою игру в этом файле!
from pygame import*
init()
window = display.set_mode((700, 500))
display.set_caption('Космические сражения')

class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        #transform.scale - загружает в себя картинку, передаём в неё ширину и высоту
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player_ship(GameSprite):
    def __init__(self, picture, width, height, x, y, x_speed, y_speed):
        super().__init__(picture, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        platforms_touched = sprite.spritecollide(self, barriers, False)
        self.rect.x += self.x_speed
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        platforms_touched = sprite.spritecollide(self, barriers, False)
        self.rect.y += self.y_speed
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    def fire(self):
        bullet = Bullets('Bullet.png', 50, 50, self.rect.right, self.rect.centery, 15)
        rockets.add(bullet)
class Bullets(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 700:
            self.kill()
class Enemy(GameSprite):
    direction = 'left'
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
    def update(self):
        right_point = 650
        left_point = 420
        if self.rect.x >= right_point:
            self.direction = 'left'            
        if self.rect.x <= left_point:
            self.direction = 'right'
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
            
wall3 = GameSprite('Wall.png', 80, 280, 320, 225)
wall2 = GameSprite('Wall.png', 80, 300, 320, 125)
wall = GameSprite('Wall.png', 280, 80, 120, 220)
wall4 = GameSprite('Wall.png', 240, 80, 320, 300)
space_ship = Player_ship('Player.png', 100, 100, 120, 400, 0, 0)
flag = GameSprite('Flag.png', 100, 100, 400, 400)
enemy_ship = Enemy('Enemy.png',100, 100, 600, 170, 5)

#wall.reset()
#wall2.reset()
#wall3.reset()
#wall4.reset()
#space_ship.reset()
#enemy_ship.reset()
#flag.reset()

GREEN = (99, 246, 68)
BLUE = (58, 52, 230)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

barriers = sprite.Group()
barriers.add(wall)
barriers.add(wall2)
barriers.add(wall3)
barriers.add(wall4)
rockets = sprite.Group()
enemies = sprite.Group()
enemies.add(enemy_ship)

run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False         
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                space_ship.y_speed = -10
            elif e.key == K_DOWN:
                space_ship.y_speed = 10
            elif e.key == K_RIGHT:
                space_ship.x_speed = 10
            elif e.key == K_LEFT:
                space_ship.x_speed = -10
        elif e.type == KEYUP:
            if e.key == K_UP:
                space_ship.y_speed = 0
            elif e.key == K_DOWN:
                space_ship.y_speed = 0
            elif e.key == K_RIGHT:
                space_ship.x_speed = 0
            elif e.key == K_LEFT:
                space_ship.x_speed = 0
            elif e.key == K_SPACE:
                space_ship.fire()
    if not finish:
        window.fill(BLUE)
        barriers.draw(window)
        space_ship.reset()
        flag.reset()
        rockets.draw(window)
        space_ship.update()
        rockets.update()
        if sprite.collide_rect(space_ship, flag):
            window.fill(GREEN)
            text = 'Победа!!!'
            main_font = font.SysFont('verdana', 75)
            caption_1 = main_font.render(
                text, True, WHITE
            )
            window.blit(caption_1, (170, 170))
            finish = True
        if sprite.spritecollide(space_ship, enemies, False):
            window.fill(RED)
            text = 'Поражение!!!'
            main_font = font.SysFont('verdana', 75)
            caption_1 = main_font.render(
                text, True, WHITE
            )
            window.blit(caption_1, (120, 170))
            finish = True  
        sprite.groupcollide(rockets, barriers, True, False)
        sprite.groupcollide(rockets, enemies, True, True)
        enemies.draw(window)
        enemy_ship.update()
    display.update()