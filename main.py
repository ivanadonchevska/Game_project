import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# set frame rate
clock = pygame.time.Clock()
FPS = 60  # frames per second

# define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200  # distance that the player can get to the edge of the screen before it starts to scroll
# TILE_SIZE = 40  # pixsel
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3

screen_scroll = 0
background_scroll = 0
level = 1
start_game = False
start_intro = False

restart = False
start = False

# define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# load music and sounds
# pygame.mixer.music.load("Audio/music2.mp3")
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)
jump_sound = pygame.mixer.Sound("Audio/jump.wav")
jump_sound.set_volume(0.5)
shoot_sound = pygame.mixer.Sound("Audio/shot.wav")
shoot_sound.set_volume(0.5)
grenade_sound = pygame.mixer.Sound("Audio/grenade.wav")
grenade_sound.set_volume(0.5)


# button images
# start_image = pygame.image.load("Images/start_btn.png").convert_alpha()
# exit_image = pygame.image.load("Images/exit_btn.png").convert_alpha()
start_image = pygame.image.load("Images/start_menu.jfif").convert_alpha()
restart_image = pygame.image.load("Images/restart.jpg").convert_alpha()

# load images for the background
pine1_image = pygame.image.load("Images/Background/pine1.png").convert_alpha()
pine2_image = pygame.image.load("Images/Background/pine2.png").convert_alpha()
mountain_image = pygame.image.load("Images/Background/mountain.png").convert_alpha()
sky_image = pygame.image.load("Images/Background/sky_cloud.png").convert_alpha()

# store tiles in a list
images_list = []
for x in range(TILE_TYPES):
    image = pygame.image.load(f"Images/Tile/{x}.png")
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    images_list.append(image)
# bullet
bullet_image = pygame.image.load("Images/Icons/bullet.png").convert_alpha()
# grenade
grenade_image = pygame.image.load("Images/Icons/grenade.png").convert_alpha()
# pick up boxes
heal_box_image = pygame.image.load("Images/Icons/health_box.png").convert_alpha()
ammo_box_images = pygame.image.load("Images/Icons/ammo_box.png").convert_alpha()
grenade_box_images = pygame.image.load("Images/Icons/grenade_box.png").convert_alpha()
item_boxes = {
    "Health": heal_box_image,
    "Ammo": ammo_box_images,
    "Grenade": grenade_box_images
}
# define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)


def draw_background():
    screen.fill(BG)
    # pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
    # to draw images for the background on the screen
    width = sky_image.get_width()
    for x in range(5):
        screen.blit(sky_image, ((x * width) - background_scroll * 0.5, 0))
        screen.blit(mountain_image,
                    ((x * width) - background_scroll * 0.6, SCREEN_HEIGHT - mountain_image.get_height() - 300))
        screen.blit(pine1_image,
                    ((x * width) - background_scroll * 0.7, SCREEN_HEIGHT - pine1_image.get_height() - 150))
        screen.blit(pine2_image, ((x * width) - background_scroll * 0.8, SCREEN_HEIGHT - pine2_image.get_height()))


# define font
font = pygame.font.SysFont("Futura", 30)


def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))


# function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Solder(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.character_type = character_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.velocity_y = 0
        self.in_air = True
        self.jump = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)  # x, y, width, height
        self.idling = False
        self.idling_counter = 0

        # load all images for the players
        animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count number of files in the folder
            number_of_frames = len(os.listdir(f"Images/{self.character_type}/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"Images/{self.character_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0  # delta x -> the change of x
        dy = 0  # delta y -> the change of y

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y

        # check for collision
        for tile in world.obstacle_list:
            # check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall then make it turn around
                if self.character_type == "Enemy":
                    self.direction *= -1
                    self.move_counter = 0
            # check for the collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.velocity_y < 0:  # player is moving up the way
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground i.e. falling
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.character_type == "Player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.character_type == "Player":
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and background_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and background_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx  # scroll in opposite direction from the player

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:  # if i have at least one bullet that i can shoot with
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.75 * self.direction),
                            self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # reduce ammo
            # write on the screen how many bullets are left latter
            self.ammo -= 1
            shoot_sound.play()

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            # check if the ai is near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)
                # shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:  # right side
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1 is for run
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    # pygame.draw.rect(screen, RED, self.vision)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # scroll
        self.rect.x += screen_scroll  # to scroll the enemies

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                # to stop the animation if the enemy is dead
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # 3 is for death animation

    def draw(self):
        # flip is to change the direction
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, RED, self.rect, 1)  # to draw rectangles


class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        #  global player
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    image = images_list[tile]
                    image_rect = image.get_rect()
                    image_rect.x = x * TILE_SIZE
                    image_rect.y = y * TILE_SIZE
                    tile_data = (image, image_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:
                        water = Decoration(image, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(image, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Solder('Player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 5, 5)  # 20 bullets for ammo
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Solder('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = ItemBox("Ammo", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = ItemBox("Grenade", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = ItemBox("Health", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Decoration(image, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(decoration)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            # x coordinate
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll  # to fix decorations where they are


class Water(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = x + TILE_SIZE // 2, y + TILE_SIZE - self.image.get_height()

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == "Health":
                # print(player.health)
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                # print(player.health)
            elif self.item_type == "Ammo":
                player.ammo += 15  # change it
            elif self.item_type == "Grenade":
                player.grenades += 3
            # delete the item box
            self.kill()


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_image
        # check the problem why doesn't work with rectangle instead of rect!!
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.direction = direction

    def update(self):
        # move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if the bullet has gone off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()  # make ammo disappear when collide with tile

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5  # change this numbers later
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    # print(enemy.health)
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -11
        self.speed = 7
        self.image = grenade_image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.velocity_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.velocity_y

        # check for collision with level
        for tile in world.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                # check for the coliision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0  # if not added this grenade keeps sliding
                # check if below the ground i.e. thrown up
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground i.e. falling
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    dy = tile[1].top - self.rect.bottom

        # update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_sound.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50  # figure it out later for different nearby positions
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                    # print(enemy.health)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            image = pygame.image.load(f"Images/Explosion/exp{num}.png").convert_alpha()
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            self.images.append(image)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.counter = 0  # to control the animation

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            # when press start button
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


# create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, BLACK, 4)

# create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 570, SCREEN_HEIGHT // 2 - 320, start_image, 1.15)
# exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_image, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 200, restart_image, 1)

# create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

# print(world_data)
world = World()
player, health_bar = world.process_data(world_data)

run = True
while run:
    clock.tick(FPS)
    # fix start buttons later
    # start_game = True
    if not start_game:
        # draw menu
        screen.fill(BG)
        # add buttons
        # if start_button.draw(screen):
        start_button.draw(screen)
        if start:
            start_game = True
            start_intro = True
        # if exit_button.draw(screen):
        # run = False

    else:
        # update background
        draw_background()
        # draw world
        world.draw()
        # show player health
        health_bar.draw(player.health)

        # show ammo
        draw_text("AMMO:", font, WHITE, 10, 35)
        for _ in range(player.ammo):
            screen.blit(bullet_image, (90 + (_ * 10), 40))
        # show grenades
        draw_text("GRENADES:", font, WHITE, 10, 60)
        for _ in range(player.grenades):
            screen.blit(grenade_image, (135 + (_ * 15), 60))

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        # update and draw groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()

        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        # show intro
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            # shoot bullets
            if shoot:
                player.shoot()
            # throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction),
                                  player.rect.top, player.direction)
                grenade_group.add(grenade)
                # reduce grenades
                player.grenades -= 1
                grenade_thrown = True
                # print(player.grenades)

            if player.in_air:
                player.update_action(2)  # 2 is for jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1 index for run animation
            else:
                player.update_action(0)  # 0 is for idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            # print(level_complete)
            background_scroll -= screen_scroll  # to scroll background too
            # check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                background_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    # load in level data and create world
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

        else:
            screen_scroll = 0
            if death_fade.fade():
                restart_button.draw(screen)
                if restart:
                    death_fade.fade_counter = 0
                    start_intro = True
                    background_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start = True
            if event.key == pygame.K_a:  # A
                moving_left = True
            if event.key == pygame.K_d:  # D
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_sound.play()
            if event.key == pygame.K_r:
                restart = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_r:
                restart = False

    pygame.display.update()
pygame.quit()
