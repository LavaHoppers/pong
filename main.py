import os
import pygame

screen_dimensions = screen_width, screen_height = 800, 600
game_name = 'Pong'

def clear_screen(screen):
    screen.fill((0,0,0))

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

class GameObject(object):

    def __init__(self, position, size, color = (255, 255, 255)):
        self.color = color
        self.rect = pygame.Rect(position, size)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.rectangle = self.texture.get_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update_position(self):
        self.set_velocity(add(self.velocity, self.acceleration))
        self.set_postion(add(self.position, self.velocity))

    def set_postion(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

def main():

    pygame.init()
    pygame.display.set_caption(game_name)
    screen = pygame.display.set_mode(screen_dimensions)

    game_objects = list()

    # Input variables
    a_pressed = False
    d_pressed = False
    w_pressed = False
    s_pressed = False
    space_pressed = False

    mouse_pos = (0, 0)

    running = True
    while running:

        ### GET INPUT ###
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    a_pressed = True
                if event.key == pygame.K_d:
                    d_pressed = True
                if event.key == pygame.K_w:
                    w_pressed = True
                if event.key == pygame.K_s:
                    s_pressed = True
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    a_pressed = False
                if event.key == pygame.K_d:
                    d_pressed = False
                if event.key == pygame.K_w:
                    w_pressed = False
                if event.key == pygame.K_s:
                    s_pressed = False
                if event.key == pygame.K_SPACE:
                    space_pressed = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
            
            left_clicking = pygame.mouse.get_pressed()[0]
            middle_clicking = pygame.mouse.get_pressed()[1]
            right_clicking = pygame.mouse.get_pressed()[2]
            
        ### GAME LOGIC ###
        if d_pressed and w_pressed:
            pass
        elif a_pressed and w_pressed:
            pass
        elif d_pressed and s_pressed:
            pass
        elif a_pressed and s_pressed:
            pass
        elif a_pressed:
            pass
        elif d_pressed:
            pass
        elif w_pressed:
            pass
        elif s_pressed:
            pass
        else:
            pass

        if d_pressed and a_pressed:
            pass

        if w_pressed and s_pressed:
            pass

        if left_clicking:
            pass


        for game_object in game_objects:
            if isinstance(game_object, GameObject):
                game_object.update_position()

        ### DISPLAY ###
        if int(pygame.time.get_ticks()) % 20 == 0:

            clear_screen(screen)
            for game_object in game_objects:
                if isinstance(game_object, GameObject):
                    game_object.draw(screen)

        pygame.display.update()



    pygame.quit()

main()
