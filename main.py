import os
import pygame

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def sub(a, b):
    return tuple(map(lambda x, y: x - y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

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
        pos1 = min(self.pos[0], other.pos[0]), min(self.pos[1], other.pos[1])
        pos2 = max(self.pos[0] + self.dim[0], other.pos[0] + other.dim[0]), max(self.pos[1] + self.dim[1], other.pos[1] + other.dim[1])
        dim = sub(pos2, pos1)
        area_observed = dim[0] * dim[1]
        area_expected = (self.dim[0] + other.dim[0]) * (self.dim[1] + other.dim[1])
        return area_expected >= area_observed
    

def main():

    fps = 240
    screen_dim = 800, 600
    paddle_dim = 20, 100
    ball_dim = 20, 20
    player_init_pos = 0, screen_dim[1] / 2 - paddle_dim[1] / 2
    enemy_init_pos = screen_dim[0] - paddle_dim[0], screen_dim[1] / 2 - paddle_dim[1] / 2

    paddle_speed = 1
    ball_speed = .5

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dim)

    game_objects = list()

    player = Rectangle(player_init_pos, paddle_dim)
    enemy = Rectangle(enemy_init_pos, paddle_dim)
    ball = Rectangle(scale(screen_dim, .5), ball_dim, (0, 122, 255))
    top = Rectangle((0, 0), (screen_dim[0], 1), (255, 0, 0))
    bot = Rectangle((0, screen_dim[1]), (screen_dim[0], 1), (255, 0, 0))

    game_objects.append(ball)
    game_objects.append(player)
    game_objects.append(enemy)



    ball.vel = -ball_speed, ball_speed

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
            player.vel = 0, -paddle_speed 
        elif s_pressed:
            player.vel = 0, paddle_speed
        else:
            player.vel = 0, 0
        if space_pressed:
            pass

        if ball.intersects(player):
            ball.vel = -ball.vel[0], ball.vel[1]
        if ball.intersects(enemy):
            ball.vel = -ball.vel[0], ball.vel[1]
        if ball.intersects(top):
            ball.vel = ball.vel[0], -ball.vel[1]
        if ball.intersects(bot):
            ball.vel = ball.vel[0], -ball.vel[1]

        dif = ball.pos[1] - enemy.pos[1]
        if dif != 0:
            enemy.vel = 0, dif / abs(dif) * paddle_speed

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
