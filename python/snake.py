import pygame
import random
import sys

# postavljanje parametara
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20

# inicijalizacija
pygame.init()
font_file = "MotionControlNeueLite.ttf"

start_font = pygame.font.Font(font_file, 50)
score_font = pygame.font.Font(font_file, 30)
game_over_font = pygame.font.Font(font_file, 50)
score = 0

# definiranje boja
WHITE = (255,255,255)
RED = (255, 0, 0)

# postavljanje zaslona
win = pygame.display.set_mode((WIDTH, HEIGHT))

# postavljanje sata
clock = pygame.time.Clock()

# inicijalizacija zmije i hrane
snake_pos = [[WIDTH//2, HEIGHT//2]]
snake_speed = [0, BLOCK_SIZE]

teleport_walls = False  

def start_screen():
    global score
    score = 0

    win.fill((0,24,0))
    
    # korištenje fonta za početni zaslon
    start_text_line1 = start_font.render("Snake Game", True, WHITE)
    start_text_line2 = score_font.render("Press any key to start", True, WHITE)

    win.blit(start_text_line1, (WIDTH // 2 - start_text_line1.get_width() // 2, 
                                HEIGHT // 2 - start_text_line1.get_height()))
    win.blit(start_text_line2, (WIDTH // 2 - start_text_line2.get_width() // 2,
                                 HEIGHT // 2 + 30))
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_key = False  # početak igre

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos

food_pos = generate_food()
food_color = RED 

def draw_objects():
    win.fill((79, 166, 79))
    for pos in snake_pos:
        pygame.draw.rect(win, WHITE, 
                         pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.circle(win, food_color, 
                       (food_pos[0] + BLOCK_SIZE // 2, food_pos[1] + 
                        BLOCK_SIZE // 2), BLOCK_SIZE // 2)
    # izvod rezultata
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))  # zapis rezultata

def update_snake():
    global food_pos, score, food_color
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]

    if not teleport_walls:
        # provjera je li se sudarila u zid
        if new_head[0] >= WIDTH or new_head[0] < 0 or new_head[1] >= HEIGHT or new_head[1] < 0:
            game_over()
            game_over_screen()
            return

    if new_head == food_pos:
        food_pos = generate_food()  
        food_color = generate_random_color()  # generiranje nove boje hrane
        score += 1  # povećavanje rezultata 
    else:
        snake_pos.pop()  # micanje zadnjeg elementa zmije

    snake_pos.insert(0, new_head)  # nova glava


def game_over():
    # uvijeti kraja igre
    if not teleport_walls:
        return snake_pos[0] in snake_pos[1:] or \
            snake_pos[0][0] > WIDTH - BLOCK_SIZE or \
            snake_pos[0][0] < 0 or \
            snake_pos[0][1] > HEIGHT - BLOCK_SIZE or \
            snake_pos[0][1] < 0

def game_over_screen():
    global score
    win.fill((0,24,0))
    
    game_over_text_line1 = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    
    # korištenje fonta za tekst
    game_over_text_line2 = score_font.render("q - quit, r - restart", True, WHITE)

    win.blit(game_over_text_line1, (WIDTH // 2 - game_over_text_line1.get_width() // 2,
                                     HEIGHT // 2 - game_over_text_line1.get_height()))
    win.blit(game_over_text_line2, (WIDTH // 2 - game_over_text_line2.get_width() // 2,
                                     HEIGHT // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # ponovna igra
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # izlaz iz igre
                    return

def run():
    global snake_speed, snake_pos, food_pos, score
    snake_pos = [[WIDTH // 2, HEIGHT // 2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    start_screen()  # pokazivanje početnog zaslona

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    if snake_speed[1] == BLOCK_SIZE:
                        continue
                    snake_speed = [0, -BLOCK_SIZE]
                if keys[pygame.K_DOWN]:
                    if snake_speed[1] == -BLOCK_SIZE:
                        continue
                    snake_speed = [0, BLOCK_SIZE]
                if keys[pygame.K_LEFT]:
                    if snake_speed[0] == BLOCK_SIZE:
                        continue
                    snake_speed = [-BLOCK_SIZE, 0]
                if keys[pygame.K_RIGHT]:
                    if snake_speed[0] == -BLOCK_SIZE:
                        continue
                    snake_speed = [BLOCK_SIZE, 0]
        if game_over():
            game_over_screen()
            return
        update_snake()
        draw_objects()
        pygame.display.update()
        clock.tick(15)  

if __name__ == '__main__':
    run()
