import random
import sys
import pygame
import numpy as np 
from agent import Agent1 

#let's fix the action_size and the state_size first
action_size = 4
state_size = (70,70) 
# We're going to start by creating a "Game" class
class Game:
    # Let's start by the constructor
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((700, 700))  # pygame.display.set_mode() creates a new graphical window for our game, if we want it to be full-screen, all we have to do is to add the parameter "pygame.FULLSCREEN"
        pygame.display.set_caption('Snake Game')  # To name the graphical window
        self.game_in_progress = True
        self.snake_position_x = 200 #the game is 2D , that's why we need to initialize the x and y positions of the snake 
        self.snake_position_y = 200
        self.snake_direction_x = 0
        self.snake_direction_y = 0
        self.snake_dimension = 10
        self.clock = pygame.time.Clock()  #we Add clock to control the speed of the game
        self.apple_position_x = random.randrange(20,670,10)#randrange is a function of the random module that generates random numbers between to values respecting a certain step 
        self.apple_position_y = random.randrange(20,670,10)
        self.apple_dimension = 10
        self.snake_length = 1 #the snake is initially made by his head only
        self.start_window = True 
        self. snakeHead = []  #we've just created the list that will contain the positions of our snake's head
        self.font = pygame.font.SysFont('Comic Sans MS', 27) #loads the default font of the system and defines the size of the text 
        #we're going to create a list that will contain all the positions of our snake 
        self.snake_positions = []

        self.agent = Agent1(state_size, action_size , )  # State size: (70, 70), Action size: 4
        self.image = pygame.image.load( r'C:\Users\user\Pictures\HD-wallpaper-classic-snake-adventures-snake-game.jpg') #loads an image from our pc 
    def main_function(self):
        while self.start_window :
             for event in pygame.event.get():  # pygame.event.get() retrieves a list of all the events that have occurred since the last time the function was called
                if event.type == pygame.QUIT:
                    sys.exit() 
                if event.type == pygame.KEYDOWN : 
                    if event.key == pygame.K_RETURN:  #the game will start when we click on the enter key on our keyboard 
                        self.start_window = False 
             self.window.fill((0,0,0))
             message = "welcome to the snake-game , press 'enter' to start "
             text_surface = self.font.render(message , True , (137,207,240)) #creates a text surface to our message , defines its color , and if the bridges are going to be smooth or not  
             text_rect = text_surface.get_rect(topleft=(20,50)) #a rect object that determines the position of the surface
             
             self.window.blit(text_surface , text_rect ) # defines where is our text surface going to be on the screen
             self.window.blit(self.image , (0,200))

             pygame.display.flip()
           

        while self.game_in_progress:
            for event in pygame.event.get():  # pygame.event.get() retrieves a list of all the events that have occurred since the last time the function was called
                if event.type == pygame.QUIT:
                    sys.exit() #to be able to quit the game using the quit icon
            self.update_snake_direction()
            self.move_snake()
            self.check_collisions() 
            self.update_Q_values()

            self.draw() 
            self.create_limits()
            pygame.display.flip() #to update the display
            self.clock.tick(20)  # Control the speed of the game ( 20 pics per sec)
            self.snakeHead.append(self.snake_position_x)
            self.snakeHead.append(self.snake_position_y)
            self.snake_positions.append(self.snakeHead)# we added the positions of the head cuz it is a part of our snake
            if len(self.snake_positions) > self.snake_length : 
                self.snake_positions.pop(0) #to avoid that everytime the snake moves he kepps getting longer 
    def update_snake_direction(self) :
        current_state = (self.snake_position_x // 10 , self.snake_position_y // 10 )  # we turn the window into a grid of cells of size 10*10 pixels
        action = self.agent.get_action(current_state)
 
        if action == 0 and self.snake_direction_x != 10: # action== 0  ( means that the action chosen by the agent is moving to the left)
            self.snake_direction_x = -10
            self.snake_direction_y = 0 
        elif  action == 1 and self.snake_direction_x != -10: #action == 1 ( the action chosen by the agent is moving to the right ) self.snake_direction_x != 0 (to check if the agent is not already moving to the left , cuz if so we don't want to flip it to the right all of a sudden not to bite its own tail) 
            self.snake_direction_x = 10
            self.snake_direction_y = 0 
        elif action == 2 and self.snake_direction_y != 10: #action == 2 (moving downwards)
            self.snake_direction_x = 0
            self.snake_direction_y = -10
        elif action == 3 and self.snake_direction_y != -10: # action == 3 ( moving upwards )
            self.snake_direction_x = 0
            self.snake_direction_y = 10
    def move_snake(self):
        self.snake_position_x += self.snake_direction_x #to actually move the snake horizontally
        self.snake_position_y += self.snake_direction_y
    
    def check_collisions(self) :
        if self.snake_position_x <= 16 or self.snake_position_x >= 680 or self.snake_position_y <= 16 or self.snake_position_y >= 680 : #if the snakes crosses the borders 
            sys.exit()
        if self.snake_position_x == self.apple_position_x and self.snake_position_y == self.apple_position_y : 
                self.apple_position_x = random.randrange ( 20, 670 , 10 ) # generate a new random position to the apple on our grid 
                self.apple_position_y = random.randrange ( 20 , 670 , 10) 
                self.snake_length += 1 
        # now let's create what makes the game stop when the snake's head touches his body
        for snake_part in self.snake_positions[:-1] :
                if self.snakeHead == snake_part : 
                    sys.exit()
    def update_Q_values(self):
        current_state = (self.snake_position_x // 10, self.snake_position_y // 10)
        action = self.agent.get_action(current_state)
        next_state = ((self.snake_position_x + self.snake_direction_x) // 10, (self.snake_position_y + self.snake_direction_y) // 10)
        reward = self.get_reward(current_state, action, next_state)

        self.agent.update_Q_table(current_state, action, reward, next_state)

    def get_reward(self, current_state, action, next_state):
        if next_state[0] < 0 or next_state[0] >= 70 or next_state[1] < 0 or next_state[1] >= 70 :
            return -10
        elif next_state[0] == self.apple_position_x // 10 and next_state[1] == self.apple_position_y // 10 :
            return 10
        else:
            return -1
    def draw (self ):
        self.window.fill((0, 0, 0))  # We paint our window in black
            #let's create our snake
        pygame.draw.rect(self.window,(0,100,0),(self.snake_position_x,self.snake_position_y,self.snake_dimension,self.snake_dimension)) #a pygame's function that draws a rectangle and that takes for parameters the position of the snake , and its dimensions

            #let's create our apple
        pygame.draw.rect(self.window,(255,0,0),(self.apple_position_x,self.apple_position_y,self.apple_dimension,self.apple_dimension))
            #let's add the rest of our snake's body parts 
        for snake_part in self.snake_positions[:-1] : 
            pygame.draw.rect(self.window,(0,100,0),(snake_part[0],snake_part[1],self.snake_dimension,self.snake_dimension))
    def create_limits(self):
        pygame.draw.rect(self.window,(255,34,34), (10,10,680,680),6) #the last parameter is the one that defines the thickness of our rectangle         
if __name__ == '__main__':  # The condition checks if the script is being run in the main program (__name__=='__main__') or if it is imported as a module in another script (__name__=='nameofmodule')
    game_instance = Game()
    game_instance.main_function()
    pygame.quit()  # Quit Pygame when done properly


  




