import os
import pygame

texture_scale = 2
screen_dimensions = screen_width, screen_height = 800, 600
game_name = 'PIXEL'

player_walking_speed = 1

t_brick = os.path.join('img', 'brick.png')

def clear_screen(screen):
    screen.fill((0,0,0))

def add(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

class GameObject(object):

    def __init__(self, position, texture_path):

        self.position = position
        self.velocity = (0, 0)
        self.acceleration = (0, 0)

        self.texture = self.load_image(texture_path)
        self.texture_flipped = False
        self.rectangle = self.texture.get_rect()
        

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.texture, self.texture_flipped,
        False), self.rectangle)

    def update_position(self):
        self.set_velocity(add(self.velocity, self.acceleration))
        self.set_postion(add(self.position, self.velocity))

    def load_image(self, image_path):
        img = pygame.image.load(image_path)
        return pygame.transform.scale(img, (int(img.get_width() * texture_scale),
        int(img.get_height() * texture_scale)))

    def set_postion(self, position):
        self.position = position
        self.rectangle.x = position[0]
        self.rectangle.y = position[1]
    
    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

def main():

    pygame.init()
    screen = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption(game_name)
    #clock = pygame.time.Clock()

    player = GameObject(0, 0, t_brick)

    game_objects = list()
    game_objects.append(player)

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
            #print(mouse_pos, left_clicking, right_clicking)
            

        ### GAME LOGIC ###
        if d_pressed and w_pressed:
            player.set_velocity((player_walking_speed, -player_walking_speed))
        elif a_pressed and w_pressed:
            player.set_velocity((-player_walking_speed, -player_walking_speed))
        elif d_pressed and s_pressed:
            player.x_vel = player_walking_speed
            player.y_vel = player_walking_speed
        elif a_pressed and s_pressed:
            player.x_vel = -player_walking_speed
            player.y_vel = player_walking_speed
        elif a_pressed:
            player.x_vel = -player_walking_speed
            player.y_vel = 0
        elif d_pressed:
            player.x_vel = player_walking_speed
            player.y_vel = 0
        elif w_pressed:
            player.x_vel = 0
            player.y_vel = -player_walking_speed
        elif s_pressed:
            player.x_vel = 0
            player.y_vel = player_walking_speed
        else:
            player.x_vel = 0
            player.y_vel = 0

        if d_pressed and a_pressed:
            player.x_vel = 0

        if w_pressed and s_pressed:
            player.y_vel = 0

        if left_clicking:
            shot = GameObject(player.rectangle.x, player.rectangle.y, t_brick)
            shot.x_vel = 1
            game_objects.append(shot)


        for game_object in game_objects:
            if isinstance(game_object, GameObject):
                game_object.update_position()

        ### DISPLAY ###
        clear_screen(screen)
        for game_object in game_objects:
            if isinstance(game_object, GameObject):
                game_object.draw(screen)
        pygame.display.update()



    pygame.quit()

main()
