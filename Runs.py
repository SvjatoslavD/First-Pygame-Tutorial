import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_2,player_walk_1]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state( )

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = ((random.randint(900,1100)),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy
    
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(midtop = (400,25))

    if current_time <= 34:
        bar_width = 20 * current_time
        progress_bar_back = pygame.draw.rect(screen, (64,64,64), pygame.Rect(60,355,680,20))
        progress_bar_loading = pygame.draw.rect(screen, (255,215,0), pygame.Rect(60,355,(bar_width),20))



    screen.blit(score_surface,score_rect)
    return current_time

def game_start_stop(score):
    text_1 = test_font.render(f'Runs', False, '#c0e8ec')
    text_1_rect = text_1.get_rect(midtop = (400,30))

    text_2 = test_font.render(f'Press Space to Start', False,'#c0e8ec')
    text_2_rect = text_2.get_rect(midtop = (400,340))

    text_3 = test_font.render(f'Your Score is {score}', False,'#c0e8ec')
    text_3_rect = text_3.get_rect(midtop = (400,340))

    player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,3)
    player_stand_rect = player_stand.get_rect(center = (400,200))

    screen.fill((94,129,162))
    screen.blit(player_stand,player_stand_rect)
    screen.blit(text_1,text_1_rect)
    if score == 0: screen.blit(text_2,text_2_rect)
    else: screen.blit(text_3,text_3_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            elif obstacle_rect.bottom == 210:screen.blit(fly_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):return False
    return True

def collision_sprite():
    if pygame.sprite.pygame.sprite.spritecollide(player.sprite, obstacle_group, False): 
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf,player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

def level():
    score = int(pygame.time.get_ticks()/1000) - start_time
    if score <= 34:
        sky_surface = pygame.image.load('graphics/Sky.png').convert()
        ground_surface = pygame.image.load('graphics/Ground.png').convert()

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
    else:
        sky_surface = pygame.image.load('graphics/lvl2Sky.png').convert()
        ground_surface = pygame.image.load('graphics/lvl2Ground.png').convert()

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runs')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 60)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())
 
obstacle_group = pygame.sprite.Group()

# obstacle_rect_list = []

# snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_frame_1,snail_frame_2]
# snail_frame_index = 0
# snail_surf = snail_frames[snail_frame_index]

# fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
# fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
# fly_frames = [fly_frame_1,fly_frame_2]
# fly_frame_index = 0
# fly_surf = fly_frames[fly_frame_index]

# player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_2,player_walk_1]
# player_index = 0
# player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(bottomleft = (100,300))
# player_gravity = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    #check that window closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly','snail','snail'])))

            # if event.type == snail_animation_timer:
            #     if snail_frame_index == 0: snail_frame_index = 1
            #     else: snail_frame_index = 0
            #     snail_surf = snail_frames[snail_frame_index]

            # if event.type == fly_animation_timer:
            #     if fly_frame_index == 0: fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surf = fly_frames[fly_frame_index]
        
    if game_active == True:
        level()
        score = display_score()

        player.draw(screen)
        player.update()
            
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        game_start_stop(score)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_active = True 
            start_time = int(pygame.time.get_ticks()/1000)

    #draw all elements
    pygame.display.update()
    clock.tick(60)