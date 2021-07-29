import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
bulletsound=pygame.mixer.Sound('bullet.mp3')
hitsound=pygame.mixer.Sound('hit.mp3')
music=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score=0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standleft=False
        self.standright=False
        self.hitbox=(self.x+17, self.y+2,31,57)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            self.standleft=True
            self.standright=False
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
            self.standleft=False
            self.standright=True
        else:
            if self.standleft:
                win.blit(walkLeft[0], (self.x,self.y))
            elif self.standright:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(char, (self.x,self.y))
        self.hitbox=(self.x+17, self.y+2,31,57)
        pygame.draw.rect(win, (0,0,0), self.hitbox, 2)
    
    def hit(self):
        self.x=60
        self.y=410
        self.walkcount=0
        self.isJump=False
        self.jumpCount=10
        font1=pygame.font.SysFont('comicsans', 100, bold=True, italic=False)
        text1=font1.render('-5', 1, (255,0,0))
        win.blit(text1, (250-(text1.get_width()/2),200))
        pygame.display.update()
        for i in range(150):
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit() 

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=15*facing
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.walkcount=0
        self.vel=5
        self.hitbox=(self.x+17, self.y+2,31,57)
        self.health=10
        self.healthbox=(self.x+30, self.y-5, 3*self.health,5)
        self.visibility=True
    def draw(self,win):
        if self.visibility:
            self.move()
            if self.walkcount+1>=33:
                self.walkcount=0
            
            if self.vel>0:
                win.blit(self.walkRight[self.walkcount//3], (self.x,self.y))
                self.walkcount+=1
            else:
                win.blit(self.walkLeft[self.walkcount//3], (self.x,self.y))
                self.walkcount+=1
            self.hitbox=(self.x+17, self.y+2,31,57)

    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*(-1)
        else:
            if self.x+self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*(-1)
        self.healthbox=(self.x+30, self.y-5, 3*self.health,5)
    def hit(self):
        print("hit")
        self.health-=1
        if self.health==0:
            self.visibility=False
            


def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: '+str(score), 1, (0,0,0))
    win.blit(text,(390,10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if goblin.visibility:
        pygame.draw.rect(win, (255,0,0), (goblin.x+30, goblin.y-5, 30,5))
        pygame.draw.rect(win, (0,128,0), goblin.healthbox)
    pygame.display.update()



#mainloop
font=pygame.font.SysFont('comicsans', 30, bold=False, italic=False)
man = player(250, 410, 64,64)
bullets=[]
goblin = enemy(100,410,64,64,450)
bulletloop=0
run = True
while run:
    clock.tick(27)
    if bulletloop<3:
        bulletloop+=1
    else:
        bulletloop=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3]> goblin.hitbox[1]:
            if man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0]:
                if goblin.visibility:
                    man.hit()   
                    score-=5
    for bullet in bullets:
        if bullet.y-bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x-bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                if goblin.visibility:
                    hitsound.play()
                    goblin.hit()
                    score+=1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 500 and bullet.x>0:
            bullet.x += bullet.vel 
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    if keys[pygame.K_SPACE]:
        if len(bullets)<10 and bulletloop==0:
            bulletsound.play()
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(255,0,0), 1 if man.standright else -1))        
    redrawGameWindow()

pygame.quit()