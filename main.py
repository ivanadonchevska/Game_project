import pygame
import os

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

# define player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_background():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Solder(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.character_type = character_type
        self.speed = speed
        self.direction = 1
        self.velocity_y = 0
        self.in_air = True
        self.jump = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ["Idle", "Run", "Jump"]
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count number of files in the folder
            number_of_frames = len(os.listdir(f"Images/{self.character_type}/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"Images/{self.character_type}/{animation}/{i}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rectangle = self.image.get_rect()
        self.rectangle.center = x, y

    def move(self, moving_left, moving_right):
        # reset movement variables
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

        # check collision with floor
        if self.rectangle.bottom + dy > 300:  # 300 number from line in background
            dy = 300 - self.rectangle.bottom
            self.in_air = False
        # update rectangle position
        self.rectangle.x += dx
        self.rectangle.y += dy


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
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        # flip is to change the direction
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rectangle)


player = Solder('Player', 200, 200, 3, 5)

run = True
while run:
    clock.tick(FPS)
    draw_background()

    player.update_animation()
    player.draw()

    # update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)  # 2 is for jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1 index for run animation
        else:
            player.update_action(0)  # 0 is for idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # A
                moving_left = True
            if event.key == pygame.K_d:  # D
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
pygame.quit()
