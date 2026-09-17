from idlelib.colorizer import prog_group_name_to_tag

import pygame

pygame.init()

screen_width=800
screen_height=int(screen_width*0.8)

SCREEN=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("lofi")

clock=pygame.time.Clock()
fps=60

moving_left=False
moving_right=False

BG=(144,201,120)

def draw_bg():
    SCREEN.fill(BG)

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        self.speed=speed
        self.char_type=char_type
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.update_time=pygame.time.get_ticks()
        for i in range(5):
         img = pygame.image.load(f'shooter_assets/img/{self.char_type}/Idle/{i}.png')
         #image scaling
         img= pygame.transform.scale(img, (int(scale * img.get_width()), int(scale * img.get_height())))
         self.animation_list.append(img)
        self.image=self.animation_list[self.frame_index]
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)
        self.flip=False
        self.direction=1


    def move(self,moving_left,moving_right):
        #reset movement variables
        dx=0
        dy=0

        #assign movement variables if moving left or right
        if moving_left:
            dx= -self.speed
            self.flip=True
            self.direction=-1
        if moving_right:
            dx=self.speed
            self.flip=False
            self.direction=1

        #update rectangle coordinates
        self.rect.x+=dx
        self.rect.y+=dy
    def update_animation(self):
        ANIMATION_COOLDOWN=100
        #update image depending on current frame
        self.image=self.animation_list[self.frame_index]
        #check if enough time has passed since last animation
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        #reseting the animation
        if self.frame_index>=len(self.animation_list):
            self.frame_index=0
    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)



player=Soldier('player',200,200,3,5)
enemy=Soldier('enemy',400,200,3,5)

run=True
while run:
    clock.tick(fps)
    draw_bg()
    player.update_animation()
    player.draw()
    player.move(moving_left,moving_right)
    enemy.draw()


    for event in pygame.event.get():
        #quit game
        if event.type==pygame.QUIT:
            run=False

        #keyboard presses
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                moving_right=True
            if event.key==pygame.K_LEFT:
                moving_left=True
            if event.key==pygame.K_ESCAPE:
                run=False

        #keyboard release
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                moving_left=False
            if event.key==pygame.K_RIGHT:
                moving_right=False








    pygame.display.update()