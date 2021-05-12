import os
import pygame

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

def clear_screen(screen):
    screen.fill((0,0,0))

class GameObject(object):

    def __init__(self, position, size, color = (255, 255, 255)):
        self.color = color
        self.rect = pygame.Rect(position, size)
        self.velocity = (0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update_position(self, delta_time):
        self.rect.move_ip(scale(self.velocity, delta_time))
    

def main():

    fps = 60
    screen_dimensions = 800, 600
    paddle_dimensions = 20, 100
    ball_dimensions = 20, 20
    player_paddle_init_pos = 0, screen_dimensions[1] / 2 - paddle_dimensions[1] / 2
    enemy_paddle_init_pos = screen_dimensions[0] - paddle_dimensions[0], screen_dimensions[1] / 2 - paddle_dimensions[1] / 2

    paddle_speed = 1
    ball_speed = 1

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dimensions)

    game_objects = list()

    game_area = pygame.Rect((0, 0), screen_dimensions)

    player_paddle = GameObject(player_paddle_init_pos, paddle_dimensions)
    enemy_paddle = GameObject(enemy_paddle_init_pos, paddle_dimensions)
    ball = GameObject(scale(screen_dimensions, .5), ball_dimensions)
    game_objects.append(ball)
    game_objects.append(player_paddle)
    game_objects.append(enemy_paddle)


    # TODO remove
    ball.velocity = ball_speed, 0

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
            player_paddle.velocity = 0,0
        elif w_pressed:
            player_paddle.velocity = 0, -paddle_speed 
        elif s_pressed:
            player_paddle.velocity = 0, paddle_speed
        else:
            player_paddle.velocity = 0, 0
        if space_pressed:
            pass

        if left_clicking:
            print(mouse_pos)

        for game_object in game_objects:
            game_object.update_position(delta_time)

        player_paddle.rect.clamp_ip(game_area)

        if player_paddle.rect.colliderect(ball):
            ball.velocity = -ball.velocity[0], ball.velocity[1]
        
        if enemy_paddle.rect.colliderect(ball):
            ball.velocity = -ball.velocity[0], ball.velocity[1]


        ### DISPLAY ###
        if int(pygame.time.get_ticks()) % (1000 // fps) == 0:

            clear_screen(screen)
            for game_object in game_objects:
                game_object.draw(screen)
            pygame.display.update()



    pygame.quit()

main()
