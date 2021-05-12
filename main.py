import os
import pygame

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

def clear_screen(screen):
    screen.fill((0, 0, 0))

class GameObject(object):

    def __init__(self, pos, dim, color = (255, 255, 255)):
        self.color = color
        self.pos = pos
        self.dim = dim
        self.vel = (0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos + self.dim)

    def update_position(self, delta_time):
        self.pos = add(self.pos, scale(self.vel, delta_time))
    

def main():

    fps = 240
    screen_dim = 800, 600
    paddle_dim = 20, 100
    ball_dim = 20, 20
    player_init_pos = 0, screen_dim[1] / 2 - paddle_dim[1] / 2
    enemy_init_pos = screen_dim[0] - paddle_dim[0], screen_dim[1] / 2 - paddle_dim[1] / 2

    paddle_speed = 1
    ball_speed = 1

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dim)

    game_objects = list()

    player = GameObject(player_init_pos, paddle_dim)
    enemy = GameObject(enemy_init_pos, paddle_dim)
    ball = GameObject(scale(screen_dim, .5), ball_dim, (0, 122, 255))

    game_objects.append(ball)
    game_objects.append(player)
    game_objects.append(enemy)

    ball.vel = -ball_speed, 0

    # Input variables
    w_pressed = False
    s_pressed = False
    space_pressed = False
    mouse_pos = (0, 0)

    previous_time = pygame.time.get_ticks()
    running = True
    while running:

        delta_time = pygame.time.get_ticks() - previous_time 
        previous_time = pygame.time.get_ticks()

        ### GET INPUT ###
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    w_pressed = True
                if event.key == pygame.K_s:
                    s_pressed = True
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
                if event.key == pygame.K_SPACE:
                    space_pressed = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
            
            left_clicking = pygame.mouse.get_pressed()[0]
            
        ### GAME LOGIC ###
        if w_pressed and s_pressed:
            player.vel = 0,0
        elif w_pressed:
            player.vel = 0, -paddle_speed 
        elif s_pressed:
            player.vel = 0, paddle_speed
        else:
            player.vel = 0, 0
        if space_pressed:
            pass

        if left_clicking:
            print(mouse_pos)

        for game_object in game_objects:
            game_object.update_position(delta_time)


        ### DISPLAY ###
        if int(pygame.time.get_ticks()) % (1000 // fps) == 0:

            clear_screen(screen)
            for game_object in game_objects:
                game_object.draw(screen)
            pygame.display.update()



    pygame.quit()

main()
