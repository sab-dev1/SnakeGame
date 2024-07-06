import random
import sys
import pygame
import numpy as np
from collections import deque #a module that contains is a collection ,from which we can add and remove elements from both sides in a fast and efficient way
from agent import Agent1

# Let's fix the action_size and the state_size
action_size = 4
state_size = (70, 70)

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((700, 700))
        pygame.display.set_caption('Snake Game')
        self.game_in_progress = True
        self.snake_position_x = 200
        self.snake_position_y = 200
        self.snake_direction_x = 0
        self.snake_direction_y = 0
        self.snake_dimension = 10
        self.clock = pygame.time.Clock()
        self.apple_position_x = random.randrange(20, 670, 10)
        self.apple_position_y = random.randrange(20, 670, 10)
        self.apple_dimension = 10
        self.snake_length = 1
        self.start_window = True
        self.snakeHead = []
        self.font = pygame.font.SysFont('Comic Sans MS', 27)
        self.snake_positions = []

        self.agent = Agent1(state_size, action_size)  # Initialize the agent
        self.image = pygame.image.load(r'C:\Users\user\Pictures\HD-wallpaper-classic-snake-adventures-snake-game.jpg')  # Load game image

    def main_function(self):
        while self.start_window:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_window = False

            self.window.fill((0, 0, 0))
            message = "Welcome to the snake game! Press 'Enter' to start."
            text_surface = self.font.render(message, True, (137, 207, 240))
            text_rect = text_surface.get_rect(topleft=(20, 50))
            self.window.blit(text_surface, text_rect)
            self.window.blit(self.image, (0, 200))
            pygame.display.flip()

        while self.game_in_progress:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.update_snake_direction()
            self.move_snake()
            self.check_collisions()

            # Get current state
            current_state = (self.snake_position_x // 10, self.snake_position_y // 10)

            # Get action from agent
            action = self.agent.get_action(current_state)

            # Update Q-values and get reward
            next_state = ((self.snake_position_x + self.snake_direction_x) // 10,
                          (self.snake_position_y + self.snake_direction_y) // 10)
            reward = self.get_reward(current_state, action, next_state)
            self.agent.update_Q_table(current_state, action, reward, next_state)

            self.draw()
            self.create_limits()
            pygame.display.flip()
            self.clock.tick(20)

            # Append snake's head position to positions list
            self.snakeHead.append(self.snake_position_x)
            self.snakeHead.append(self.snake_position_y)
            self.snake_positions.append(self.snakeHead)

            # Remove oldest position if snake has moved
            if len(self.snake_positions) > self.snake_length:
                self.snake_positions.pop(0)

    def update_snake_direction(self):
        current_state = (self.snake_position_x // 10, self.snake_position_y // 10)
        action = self.agent.get_action(current_state)

        if action == 0 and self.snake_direction_x != 10:
            self.snake_direction_x = -10
            self.snake_direction_y = 0
        elif action == 1 and self.snake_direction_x != -10:
            self.snake_direction_x = 10
            self.snake_direction_y = 0
        elif action == 2 and self.snake_direction_y != 10:
            self.snake_direction_x = 0
            self.snake_direction_y = -10
        elif action == 3 and self.snake_direction_y != -10:
            self.snake_direction_x = 0
            self.snake_direction_y = 10

    def move_snake(self):
        self.snake_position_x += self.snake_direction_x
        self.snake_position_y += self.snake_direction_y

    def check_collisions(self):
        if self.snake_position_x <= 16 or self.snake_position_x >= 680 or \
                self.snake_position_y <= 16 or self.snake_position_y >= 680:
            sys.exit()

        if self.snake_position_x == self.apple_position_x and self.snake_position_y == self.apple_position_y:
            self.apple_position_x = random.randrange(20, 670, 10)
            self.apple_position_y = random.randrange(20, 670, 10)
            self.snake_length += 1

        for snake_part in self.snake_positions[:-1]:
            if self.snakeHead == snake_part:
                sys.exit()

    def get_reward(self, current_state, action, next_state):
        if next_state[0] < 0 or next_state[0] >= 70 or next_state[1] < 0 or next_state[1] >= 70:
            return -10
        elif next_state[0] == self.apple_position_x // 10 and next_state[1] == self.apple_position_y // 10:
            return 10
        else:
            return -1

    def draw(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (0, 100, 0),
                         (self.snake_position_x, self.snake_position_y, self.snake_dimension, self.snake_dimension))
        pygame.draw.rect(self.window, (255, 0, 0),
                         (self.apple_position_x, self.apple_position_y, self.apple_dimension, self.apple_dimension))
        for snake_part in self.snake_positions[:-1]:
            pygame.draw.rect(self.window, (0, 100, 0),
                             (snake_part[0], snake_part[1], self.snake_dimension, self.snake_dimension))

    def create_limits(self):
        pygame.draw.rect(self.window, (255, 34, 34), (10, 10, 680, 680), 6)

if __name__ == '__main__':
    game_instance = Game()
    game_instance.main_function()
    pygame.quit()
