import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

x = 200
y = 200
scale = 3
image = pygame.image.load("Images/Enemy/Idle/0 (1).png")
image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
rectangle = image.get_rect()
rectangle.center = x, y


run = True
while run:
    screen.blit(image, rectangle)
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
