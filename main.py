import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# set frame rate
clock = pygame.time.Clock()
FPS = 60  # frames per second
# define player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)


def draw_background():
    screen.fill(BG)


class Solder(pygame.sprite.Sprite):
    def __init__(self, character_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.character_type = character_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f"Images/{self.character_type}/Idle/0 (1).png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
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

        # update rectangle position
        self.rectangle.x += dx
        self.rectangle.y += dy

    def draw(self):
        # flip is to change the direction
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rectangle)


player = Solder('Player', 200, 200, 3, 5)


run = True
while run:
    clock.tick(FPS)
    draw_background()

    player.draw()
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
