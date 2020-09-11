import pygame
import random
from os import path
import time 

img_dir = path.join(path.dirname(__file__),'img')


RED=(255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW= (255,255,0)
WHITE=(255,255,255)

WIDTH = 800
HEIGHT = 800
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game One")
clock = pygame.time.Clock()

def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)
font_name = pygame.font.match_font('arial')
#function to put text on screen
#needs where,what,size,x location,y location  
def draw_text(surf,text,size,x,y):
	font=pygame.font.Font(font_name,size)
	text_surface=font.render(text,True,WHITE)
	text_rect=text_surface.get_rect()
	text_rect.midtop=(x,y)
	surf.blit(text_surface,text_rect)

 
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#size and color
		self.image= pygame.transform.scale(player_img,(100,75))
		self.image.set_colorkey(WHITE)
		#self.image=pygame.Surface((50,40))
		# self.image.fill(WHITE)
		#produce a rectangle
		self.rect = self.image.get_rect()
		self.radius =20
		#pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
		#Location on the screen
		self.rect.centerx=WIDTH/2
		self.rect.bottom = HEIGHT-10
		self.speedx = 0
		self.speedy = 0
	def update(self):
		self.speedx=0
		self.speedy=0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speedx = -8
		if keystate[pygame.K_d]:
			self.speedx = 8
		if keystate[pygame.K_w]:
			self.speedy = -8
		if keystate[pygame.K_s]:
			self.speedy = 8
		if self.rect.right>WIDTH:
			self.rect.right=WIDTH
		if self.rect.left <0:
			self.rect.left = 0
		if self.rect.top > 690:
			self.rect.top = 690
		if self.rect.bottom < -25:
			self.rect.bottom = -25 
		self.rect.x += self.speedx
		self.rect.y += self.speedy
	def shoot(self):
		bullet=Bullet(self.rect.centerx,self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#size and color
		#self.image=pygame.Surface((30,40))
		# self.image.fill(RED)
		self.image= pygame.transform.scale(enemy_img,(200,125))
		self.image.set_colorkey(WHITE)
		#produce a rectangle
		self.rect = self.image.get_rect()
		self.radius = 20
		#pygame.draw.circle(self.image,GREEN,self.rect.center,self.radius)
		
		#Location on the screen
		self.rect.x =random.randrange(WIDTH-self.rect.width)
		self.rect.y =random.randrange(-100,-40) 
		self.speedy = random.randrange(1,8)
		self.speedx = random.randrange(-3,3)
	def update(self):
		self.rect.x +=self.speedx
		self.rect.y += self.speedy
		
		if self.rect.top>HEIGHT+10 or self.rect.left<-25 or self.rect.right>WIDTH+20:
			self.rect.x =random.randrange(WIDTH-self.rect.width)
			self.rect.y =random.randrange(-100,-40)
			self.speedy = random.randrange(1,8)
			
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		#size and color
		#self.image=pygame.Surface((10,20))
		#self.image.fill(YELLOW)
		self.image= pygame.transform.scale(bullet_img,(50,38))
		self.image.set_colorkey(WHITE)
		#produce a rectangle
		self.rect = self.image.get_rect()
		#Location on the screen
		self.rect.bottom=y
		self.rect.centerx =x
		self.speedy = -10
	def update(self):
		
		self.rect.y += self.speedy
		if self.rect.bottom<0:
			self.kill()
			
			
			
def show_go_screen():
	screen.blit(background,background_rect)
	draw_text(screen,"Zombie Game",64,WIDTH/2,HEIGHT/2)
	draw_text(screen,"arrow keys to move. Space to fire",22,WIDTH/2,HEIGHT/4)
	draw_text(screen,"Press a key to begin",18,WIDTH/2,HEIGHT*3/4)
	pygame.display.flip()
	
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False
				
#######################################
#load imgs
background=pygame.image.load(path.join(img_dir,"city.png")).convert()
background_rect=background.get_rect()
player_img=pygame.image.load(path.join(img_dir,"mainguy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"bullet.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir,"enemy.png")).convert()
background = pygame.transform.scale(background, (800,800))
#meteor_images = pygame.image.load(path.join(img_dir,"meteorBrown_big1.png")).convert()
# meteor_images = []
# meteor_list =['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_med1.png',
# 'meteorBrown_med3.png',
# 'meteorBrown_small1.png',
# 'meteorBrown_small2.png',
# 'meteorBrown_tiny1.png']
# explosion_img = pygame.image.load(path.join(img_dir,"Preview_107.png")).convert()
# for img in meteor_list:
	# meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())



#######################################


all_sprites=pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
#player
player=Player()
all_sprites.add(player)
#Mobs
for i in range(8):
	newmob()
game_over = True
running = True
score=0
while running:
	if game_over:
		show_go_screen()
		game_over= False
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			#########
			newmob()
			#########
		score = 0
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type ==pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:	
			if event.key == pygame.K_SPACE:
				player.shoot()
					
	all_sprites.update()
	hits = pygame.sprite.groupcollide(mobs,bullets,True,True)
	for hit in hits:
		score+=50
		# print(score)
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)
	count = 0
	hits=pygame.sprite.spritecollide(player,mobs,False)
	if hits:
		game_over = True
		
	
	screen.fill(BLACK)
	screen.blit(background,background_rect)
	all_sprites.draw(screen)
	draw_text(screen,str(score),25,WIDTH/2,HEIGHT/11)
	#updates the screen
	pygame.display.flip()
pygame.quit()
