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

    def update_position(self):
        self.set_postion(add(self.rect.topleft, self.velocity))

    def set_postion(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    def set_velocity(self, velocity):
        self.velocity = velocity

def main():

    screen_dimensions = (800, 600)
    fps = 60
    paddle_dimensions = (20, 100)
    player_paddle_init_pos = (0, screen_dimensions[1] / 2 - paddle_dimensions[1] / 2)

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dimensions)

    game_objects = list()

    player_paddle = GameObject(player_paddle_init_pos, paddle_dimensions)
    game_objects.append(player_paddle)

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
            player_paddle.set_velocity((0,0))
        elif w_pressed:
            player_paddle.set_velocity((0,-1 * delta_time))
        elif s_pressed:
            player_paddle.set_velocity((0,1 * delta_time))
        else:
            player_paddle.set_velocity((0,0))
        if space_pressed:
            player_paddle.set_postion(player_paddle_init_pos)

        if left_clicking:
            player_paddle.set_postion(mouse_pos)

        for game_object in game_objects:
            game_object.update_position()

        if player_paddle.rect.x < 0:
            game_object.set_postion(0, player_paddle.rect.y)

        ### DISPLAY ###
        if int(pygame.time.get_ticks()) %  (1000 // 60) == 0:

            clear_screen(screen)
            for game_object in game_objects:
                game_object.draw(screen)
            pygame.display.update()



    pygame.quit()

main()
