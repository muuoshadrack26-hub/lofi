import os
import pygame

pygame.init()

screen_width = 800
screen_height = int(screen_width * 0.8)
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("lofi")

GRAVITY = 0.75
clock = pygame.time.Clock()
fps = 60

# Define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False  # Keep global flag tracking
grenade_thrown=False

# Load images
bullet_img = pygame.image.load('shooter_assets/img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('shooter_assets/img/icons/grenade.png').convert_alpha()

BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    SCREEN.fill(BG)
    pygame.draw.line(SCREEN, RED, (0, 300), (screen_width, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.speed = speed
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.grenades=5
        self.start_ammo = ammo
        self.char_type = char_type
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Load all images for the player animation_types
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            # Count number of frames in the folder
            number_of_frames = len(os.listdir(f"shooter_assets/img/{self.char_type}/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"shooter_assets/img/{self.char_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(scale * img.get_width()), int(scale * img.get_height())))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.flip = False
        self.direction = 1
        self.jump = False
        self.vel_y = 0

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump:
            self.vel_y = -11
            self.jump = False

        # Applying gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10  # FIXED: Added assignment operator
        dy += self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom

        # Update rectangle coordinates
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_grp.add(bullet)
            # Reduce ammo
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since last animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Resetting the animation
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = (len(self.animation_list[self.action])) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def update_action(self, new_action):
        # Check if the new action is diff to previous
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Delete bullet when it crosses screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        # Checking collisions with characters
        if pygame.sprite.spritecollide(player, bullet_grp, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_grp, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -10
        self.speed = 7
        self.image = grenade_img  # FIXED: Set image to grenade_img instead of bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y+=GRAVITY
        dx=self.direction*self.speed
        dy=self.vel_y
        #check collision with floor
        if self.rect.bottom + dy>300:
            dy=300-self.rect.bottom
            self.speed=0
        if self.rect.left + dx <0 or self.rect.right + dx > screen_width:
            self.direction*= -1
            dx = self.direction * self.speed
        #update grenade pos
        self.rect.x+=dx
        self.rect.y+=dy

    # Note: You will need to add an update method here later to make grenades move/explode


bullet_grp = pygame.sprite.Group()
grenade_grp = pygame.sprite.Group()

player = Soldier('player', 300, 200, 3, 5, 10)
enemy = Soldier('enemy', 200, 250, 3, 5, 10)

run = True
while run:
    clock.tick(fps)
    draw_bg()

    player.update()
    player.draw()

    # Update player action
    if player.alive:
        if shoot:
            player.shoot()
        elif grenade and grenade_thrown==False and player.grenades>0:  # FIXED: Replaced dangling 'else' with explicit check
            new_grenade = Grenade(player.rect.centerx + (player.rect.size[0]*player.direction),\
                                  player.rect.centery - player.rect.top, player.direction)
            grenade_grp.add(new_grenade)

            player.grenades-=1
            grenade_thrown=True
            grenade = False  # Reset flag so it only throws one per key press
            print(player.grenades)

        if moving_left or moving_right:
            player.update_action(1)  # Running
        else:
            player.update_action(0)  # Idle

        player.move(moving_left, moving_right)

    enemy.update()
    enemy.draw()

    # Update and draw groups
    bullet_grp.update()
    grenade_grp.update()
    bullet_grp.draw(SCREEN)
    grenade_grp.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_m:
                shoot = True
            if event.key == pygame.K_g:
                grenade = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_m:
                shoot = False
            if event.key==pygame.K_g:
                grenade=True
                grenade_thrown=False

    pygame.display.update()

pygame.quit()
