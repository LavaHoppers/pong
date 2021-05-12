import pygame
import random

from pygame.constants import GL_MULTISAMPLEBUFFERS

def add(a: tuple, b: tuple) -> tuple:
    return tuple(map(lambda x, y: x + y, a, b))

def sub(a, b):
    return tuple(map(lambda x, y: x - y, a, b))

def scale(a, c):
    return tuple(map(lambda x: x * c, a))

def r_sign():
    return 1 if random.random() < 0.5 else -1

def clear_screen(screen):
    screen.fill((38, 70, 83))

class Rectangle(object):

    def __init__(self, pos, dim, color = (255, 255, 255)):
        self.color = color
        self.pos = pos
        self.dim = dim
        self.vel = (0, 0)
        self.displaying = True

    def draw(self, screen):
        if self.displaying:
            pygame.draw.rect(screen, self.color, self.pos + self.dim)

    def update_pos(self, delta_time):
        self.pos = add(self.pos, scale(self.vel, delta_time))

    def intersects(self, other):
        x_obs = self.dim[0] + other.dim[0]
        y_obs = self.dim[1] + other.dim[1]
        x_max = max(self.pos[0] + self.dim[0], other.pos[0] + other.dim[0]) - min(self.pos[0], other.pos[0])
        y_max = max(self.pos[1] + self.dim[1], other.pos[1] + other.dim[1]) - min(self.pos[1], other.pos[1])
        return (x_max < x_obs) and (y_max < y_obs)
    
class Text(object):

    def __init__(self, font, size, text, color):
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.img = self.font.render(text, True, self.color)
        self.pos = 0, 0
        self.rect = self.img.get_rect()
        self.displaying = True

    def set_pos(self, pos: tuple) -> None:
        self.pos = pos
    
    def draw(self, screen):
        if self.displaying:
           # pygame.draw.rect(self.img, (38, 70, 83), self.rect, 1)
            screen.blit(self.img, self.pos)

    def set_text(self, text: str) -> None:
        self.img = self.font.render(text, True, self.color)

    def update_pos(self, delta_time):
        pass

def main():

    fps = 240
    screen_dim = 800, 600
    paddle_dim = 20, 100
    ball_dim = 15, 15
    player_init_pos = 15, screen_dim[1] / 2 - paddle_dim[1] / 2
    enemy_init_pos = screen_dim[0] - paddle_dim[0] - 15, screen_dim[1] / 2 - paddle_dim[1] / 2
    ball_init_pos = sub(scale(screen_dim, .5), scale(ball_dim, .5))

    player_speed = .75
    enemy_speed = .33
    ball_speed = .45

    pygame.init()
    pygame.display.set_caption('Pong')
    screen = pygame.display.set_mode(screen_dim)

    game_objects = list()

    player_score = 0
    enemy_score = 0

    player_score_text = Text('roboto.ttf', 122, str(player_score), (244, 162, 97))
    player_score_text.set_pos((180, 50))
    game_objects.append(player_score_text)

    enemy_score_text = Text('roboto.ttf', 122, str(enemy_score), (244, 162, 97))
    enemy_score_text.set_pos((580, 50))
    game_objects.append(enemy_score_text)

    start_text1 = Text('roboto.ttf', 32, "Use W and S to move", (233, 196, 106))
    start_text1.set_pos((290, 400))
    start_text2 = Text('roboto.ttf', 72, 'Press space to begin', (233, 196, 106))
    start_text2.set_pos((160, 420))
    game_objects.append(start_text1)
    game_objects.append(start_text2)

    game_over = False
    winning_text = Text('roboto.ttf', 122, "You Won!", (42, 157, 143))
    winning_text.set_pos((210, 260))
    winning_text.displaying = False
    losing_text = Text('roboto.ttf', 122, 'You Lost!', (231, 111, 81))
    losing_text.set_pos((210, 260))
    losing_text.displaying = False
    game_objects.append(winning_text)
    game_objects.append(losing_text)

    player = Rectangle(player_init_pos, paddle_dim, (42, 157, 143))
    enemy = Rectangle(enemy_init_pos, paddle_dim, (231, 111, 81))
    ball = Rectangle(ball_init_pos, ball_dim, (233, 196, 106))
    ball.displaying = False
    top = Rectangle((0, -50), (screen_dim[0], 50))
    bot = Rectangle((0, screen_dim[1]), (screen_dim[0], 50))
    left = Rectangle((-50, -50), (50, screen_dim[1] + 100))
    right = Rectangle((screen_dim[0], -50), (50, screen_dim[1] + 100))

    game_objects.append(ball)
    game_objects.append(player)
    game_objects.append(enemy)

    ball.vel = 0, 0

    # Input variables
    w_pressed = False
    s_pressed = False
    space_pressed = False

    new_round = True
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
        if space_pressed and new_round:
            if game_over:
                player_score = 0
                player_score_text.set_text(str(player_score))
                enemy_score = 0
                enemy_score_text.set_text(str(enemy_score))
                game_over = False
            start_text1.displaying = False
            start_text2.displaying = False
            ball.displaying = True
            ball.vel = r_sign() * ball_speed, r_sign() * ball_speed
            new_round = False
            losing_text.displaying = False
            winning_text.displaying = False

        ball_after = Rectangle(add(ball.pos, ball.vel), ball.dim)

        if ball_after.intersects(player):
            ball.vel = ball_speed * random.uniform(.75, 1.25), ball_speed * r_sign() * random.uniform(.75, 1.25)
        if ball_after.intersects(enemy):
            ball.vel = ball_speed * -random.uniform(.75, 1.25), ball_speed * r_sign() * random.uniform(.75, 1.25)
        if ball_after.intersects(top) or ball_after.intersects(bot):
            ball.vel = ball.vel[0], -ball.vel[1]
        if ball_after.intersects(left):
            ball.pos = ball_init_pos
            ball.displaying = False
            ball.vel = 0, 0
            new_round = True
            enemy_score += 1
            enemy_score_text.set_text(str(enemy_score))
        if ball_after.intersects(right):
            ball.pos = ball_init_pos
            ball.displaying = False
            ball.vel = 0, 0
            new_round = True
            player_score += 1
            player_score_text.set_text(str(player_score))

        if new_round:
            enemy.vel = 0, 0
        else:
            dif = (ball.pos[1] + ball.dim[1] / 2) - (enemy.pos[1] + enemy.dim[1] / 2)
            if dif == 0:
                enemy.vel = 0, 0
            else:
                enemy.vel = 0, dif / abs(dif) * enemy_speed
        
        enemy_after = Rectangle(add(enemy.pos, enemy.vel), paddle_dim)
        if enemy_after.intersects(top) or enemy_after.intersects(bot):
            enemy.vel = 0, 0

        player_after = Rectangle(add(player.pos, player.vel), paddle_dim)
        if player_after.intersects(top) or player_after.intersects(bot):
            player.vel = 0, 0
            
        for game_object in game_objects:
            game_object.update_pos(delta_time)

        if player_score >= 5:
            game_over = True
            winning_text.displaying = True
            ball.vel = 0, 0
            ball.pos = ball_init_pos
            ball.displaying = False
            start_text2.set_text("Press space to play again")
            start_text2.set_pos((90,420))
            start_text2.displaying = True
        elif enemy_score >= 5:
            game_over = True
            losing_text.displaying = True
            ball.vel = 0, 0
            ball.pos = ball_init_pos
            ball.displaying = False
            new_round = True
            start_text2.set_text("Press space to play again")
            start_text2.set_pos((90,420))
            start_text2.displaying = True
        else:
            pass
        ### DISPLAY ###
        if int(pygame.time.get_ticks()) % (1000 // fps) == 0:

            clear_screen(screen)
            for game_object in game_objects:
                game_object.draw(screen)
            
            pygame.display.update()


    pygame.quit()

main()
