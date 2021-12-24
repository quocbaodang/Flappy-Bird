import pygame
import random

# set cấu hình
WIDTH = 432
HEIGHT = 768
FPS = 120 # khung hình trên giây
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512) # điều chỉnh âm thanh

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

# Các hàm
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 750))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_coll(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_mov*3, 1) # tao hieu ung xoay cho chim
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_suf = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_suf.get_rect(center = (216,100))
        screen.blit(score_suf, score_rect)
    if game_state == 'game over':
        score_suf = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_suf.get_rect(center = (216,100))
        screen.blit(score_suf, score_rect)

        high_score_suf = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_suf.get_rect(center = (216,620))
        screen.blit(high_score_suf, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Các biến
gra = 0.25
bird_mov = 0
game_active = True
score = 0
high_score = 0

# Chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Chèn floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo bird
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))

# Create timer for bird
birdflag = pygame.USEREVENT + 1
pygame.time.set_timer(birdflag, 200)

# Chèn pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Create timer for pipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400]

# Tạo màn hình kết thúc
game_over_suf = pygame.image.load('assets/message.png').convert_alpha()
game_over_suf = pygame.transform.scale2x(game_over_suf)
game_over_rect = game_over_suf.get_rect(center = (216,384))

# chèn âm thanh
flag_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_count = 105

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_mov = 0
                bird_mov -= 9
                flag_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_mov = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflag:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # bachground
    screen.blit(bg, (0,0))

    # Khi game hoat dong
    if game_active:
        # Bird
        bird_mov += gra
        bird_rect.centery += bird_mov
        ro_bird = rotate_bird(bird)
        screen.blit(ro_bird, bird_rect)
        game_active = check_coll(pipe_list)

        # Pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_count -= 1
        if score_sound_count <= 0:
            score_sound.play()
            score_sound_count = 105
    else:
        screen.blit(game_over_suf, game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.flip()
pygame.quit()