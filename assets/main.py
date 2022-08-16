import pygame
from fighter import Fighter
from pygame import mixer

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Morris Eguakun's Ninja Warrior")

clock = pygame.time.Clock()
FPS = 60

# colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# define game varibles
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores [P!, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_OFFSET = [112, 107]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("/Users/morriseguakun/Desktop/streetfighter/assets/audio/Future - PUFFIN ON ZOOTIEZ (Official Audio).mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("/Users/morriseguakun/Desktop/streetfighter/assets/audio/assets_audio_sword.wav")
sword_fx.set_volume(0.35)
magic_fx = pygame.mixer.Sound("/Users/morriseguakun/Desktop/streetfighter/assets/audio/assets_audio_magic.wav")
magic_fx.set_volume(0.35)

# load background image
bg_image = pygame.image.load(
    "/Users/morriseguakun/Desktop/streetfighter/assets/images/background/background_lava.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load(
    "/Users/morriseguakun/Desktop/streetfighter/assets/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("/Users/morriseguakun/Desktop/streetfighter/assets/wizard/wizard.png").convert_alpha()

# load victory image
victory_img = pygame.image.load("/Users/morriseguakun/Desktop/streetfighter/assets/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
count_font = pygame.font.Font("/Users/morriseguakun/Desktop/streetfighter/assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("/Users/morriseguakun/Desktop/streetfighter/assets/fonts/turok.ttf", 30)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# health meters
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)

fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Game loop
run = True

while run:

    clock.tick(FPS)

    # Draw background
    draw_bg()

    # show player health status
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("Player 1 Score: " + str(score[0]), score_font, WHITE, 20, 60)
    draw_text("Player 2 Score: " + str(score[1]), score_font, WHITE, 580, 60)


    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) > 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    # update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:

        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
     # display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


    # event handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
