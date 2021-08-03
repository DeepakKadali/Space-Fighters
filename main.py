import pygame
import os

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)
winner_font=pygame.font.SysFont("comicsans", 100)
window_height, window_width = 500, 1000
vel = 10
bullet_vel = 15
max_number_of_bullets = 15
FPS = 60
black_c = (0, 0, 0)
yellow_c=(255,255,0)
red_c=(255,0,0)
white_c=(255,255,255)
win_c=(255,125,0)
yellow_score = 10
red_score = 10
middle_division = pygame.Rect((window_width // 2) - 10, 0, 10, window_height)
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space FigHEALTH")
spaceship_size_w, spaceship_size_h = 50, 50
# yellow_spaceship=pygame.image.load(os.path.join("Assets/spaceship_yellow.png"))
yellow_spaceship = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/spaceship_yellow.png")),
                           (spaceship_size_w, spaceship_size_h)), 90)
# red_spaceship=pygame.image.load(os.path.join("Assets/spaceship_red.png"))
red_spaceship = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/spaceship_red.png")),
                           (spaceship_size_w, spaceship_size_h)), 270)
space=pygame.transform.scale(pygame.image.load(os.path.join("Assets/—Pngtree—purple flat space planet banner_1101832.jpg")),(window_width,window_height))

def red_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x > middle_division.x + middle_division.width:  # left
        red.x -= vel
    if keys[pygame.K_RIGHT] and red.x < window_width - spaceship_size_w:  # right
        red.x += vel
    if keys[pygame.K_UP] and red.y > 0:  # up
        red.y -= vel
    if keys[pygame.K_DOWN] and red.y + 20 < window_height - spaceship_size_h:  # down
        red.y += vel


def yellow_movement(keys, yellow):
    if keys[pygame.K_a] and yellow.x > 0:  # left
        yellow.x -= vel
    if keys[pygame.K_d] and yellow.x < middle_division.x - spaceship_size_w:  # right
        yellow.x += vel
    if keys[pygame.K_w] and yellow.y > 0:  # up
        yellow.y -= vel
    if keys[pygame.K_s] and yellow.y + 20 < window_height - spaceship_size_h:  # down
        yellow.y += vel


def bullet_movement(yellow_bullets, red_bullets, red, yellow, yellow_score, red_score):
    for bullet in yellow_bullets:
        if bullet.x + bullet_vel > window_width:
            yellow_bullets.remove(bullet)
        elif red.x <= bullet.x < red.x + red.width and red.y <= bullet.y <= red.y + red.height:
            red_score -= 1
            yellow_bullets.remove(bullet)
        else:
            bullet.x += bullet_vel
    for bullet in red_bullets:
        if bullet.x - bullet_vel < 0:
            red_bullets.remove(bullet)
        elif yellow.x <= bullet.x < yellow.x + yellow.width and yellow.y <= bullet.y <= yellow.y + yellow.height:
            yellow_score -= 1
            red_bullets.remove(bullet)
        else:
            bullet.x -= bullet_vel
    #print(yellow_score, red_score)
    return yellow_score, red_score


def draw(yellow, red, yellow_bullets, red_bullets, yellow_score, red_score):
    win.blit(space,(0,0))
    pygame.draw.rect(win, black_c, ((window_width // 2) - 10, 0, 10, window_height))
    win.blit(yellow_spaceship, (yellow.x, yellow.y))
    win.blit(red_spaceship, (red.x, red.y))
    yellow_score_text = font.render("HEALTH :" + str(yellow_score), True,white_c )
    red_score_text = font.render("HEALTH :" + str(red_score), True, white_c)
    win.blit(yellow_score_text,(50,50))
    win.blit(red_score_text, (800, 50))

    for bullet in yellow_bullets:
        # y_bullet=pygame.Rect()
        # win.blit(bullet,(bullet.x,bullet.y))
        pygame.draw.rect(win, yellow_c, (bullet.x, bullet.y, bullet.width, bullet.height))
    for bullet in red_bullets:
        # win.blit(bullet,(bullet.x,bullet.y))
        pygame.draw.rect(win, red_c, (bullet.x, bullet.y, bullet.width, bullet.height))

    pygame.display.update()

def winner(text):
    winner_text=winner_font.render(text,True,win_c)
    win.blit(winner_text,(window_width//2-winner_text.get_width()//2,window_height//2-winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)
def main():
    global yellow_score, red_score
    clock = pygame.time.Clock()
    yellow = pygame.Rect(100, 200, spaceship_size_w, spaceship_size_h)
    red = pygame.Rect(700, 200, spaceship_size_w, spaceship_size_h)
    yellow_bullets = []
    red_bullets = []
    run = True
    while run:
        clock.tick(FPS)
        # pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_number_of_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height / 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_number_of_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height / 2, 10, 5)
                    red_bullets.append(bullet)
        s=''
        # if yellow_score <=0 or yellow_score <=0:
        if yellow_score <=0:
            s='RED WINS!'
        if red_score <= 0:
            s='YELLOW WINS!'
        if len(s)!=0:
            winner(s)
            break
        keys = pygame.key.get_pressed()
        yellow_movement(keys, yellow)
        red_movement(keys, red)
        yellow_score, red_score = bullet_movement(yellow_bullets, red_bullets, red, yellow, yellow_score, red_score)


        draw(yellow, red, yellow_bullets, red_bullets, yellow_score, red_score)
    pygame.quit()


if __name__ == "__main__":
    main()
