import os
import pygame
import random

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def sub(a, b):
    return tuple(map(lambda x, y: x - y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

def r_sign():
    return 1 if random.random() < 0.5 else -1

def clear_screen(screen):
    screen.fill((0, 0, 0))

class Rectangle(object):

    def __init__(self, pos, dim, color = (255, 255, 255)):
        self.color = color
        self.pos = pos
        self.dim = dim
        self.vel = (0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos + self.dim)

    def update_pos(self, delta_time):
        self.pos = add(self.pos, scale(self.vel, delta_time))

    def intersects(self, other):
        x_obs = self.dim[0] + other.dim[0]
        y_obs = self.dim[1] + other.dim[1]
        x_max = max(self.pos[0] + self.dim[0], other.pos[0] + other.dim[0]) - min(self.pos[0], other.pos[0])
        y_max = max(self.pos[1] + self.dim[1], other.pos[1] + other.dim[1]) - min(self.pos[1], other.pos[1])
        return (x_max < x_obs) and (y_max < y_obs)
    

def main():

    fps = 240
    screen_dim = 800, 600
    paddle_dim = 20, 100
    ball_dim = 20, 20
    player_init_pos = 0, screen_dim[1] / 2 - paddle_dim[1] / 2
    enemy_init_pos = screen_dim[0] - paddle_dim[0], screen_dim[1] / 2 - paddle_dim[1] / 2

    player_speed = .75
    enemy_speed = .33
    ball_speed = .5

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dim)

    game_objects = list()

    player = Rectangle(player_init_pos, paddle_dim)
    enemy = Rectangle(enemy_init_pos, paddle_dim)
    ball = Rectangle(scale(screen_dim, .5), ball_dim, (0, 122, 255))
    top = Rectangle((0, -50), (screen_dim[0], 50))
    bot = Rectangle((0, screen_dim[1]), (screen_dim[0], 50))
    left = Rectangle((-50, 0), (50, screen_dim[1]))
    right = Rectangle((screen_dim[0], 0), (50, screen_dim[1]))


    game_objects.append(ball)
    game_objects.append(player)
    game_objects.append(enemy)



    ball.vel = r_sign() * ball_speed, r_sign() * ball_speed

    # Input variables
    w_pressed = False
    s_pressed = False
    space_pressed = False

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
            
        ### GAME LOGIC ###
        if w_pressed and s_pressed:
            player.vel = 0, 0
        elif w_pressed:
            player.vel = 0, -player_speed 
        elif s_pressed:
            player.vel = 0, player_speed
        else:
            player.vel = 0, 0
        if space_pressed:
            pass

        if ball.intersects(player) or ball.intersects(enemy):
            ball.vel = -ball.vel[0], ball.vel[1]
        if ball.intersects(top) or ball.intersects(bot):
            ball.vel = ball.vel[0], -ball.vel[1]
        if ball.intersects(left) or ball.intersects(right):
            ball.pos = scale(screen_dim, .5)
            ball.vel = r_sign() * ball.vel[0], r_sign() * ball.vel[1]
        


        dif = (ball.pos[1] + ball.dim[1] / 2) - (enemy.pos[1] + enemy.dim[1] / 2)
        if dif != 0:
            enemy.vel = 0, dif / abs(dif) * enemy_speed

        for game_object in game_objects:
            game_object.update_pos(delta_time)


        ### DISPLAY ###
        if int(pygame.time.get_ticks()) % (1000 // fps) == 0:

            clear_screen(screen)
            for game_object in game_objects:
                game_object.draw(screen)
            pygame.display.update()



    pygame.quit()

main()
