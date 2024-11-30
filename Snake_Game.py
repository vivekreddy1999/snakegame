import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20 #Increase or decrease this number to adjust game size.
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)          #Background Color
WHITE = (255, 255, 255)    #Score card color
RED = (255, 0, 0)          #Food Color
GREEN = (0, 255, 0)        #Snake Color
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)

    def spawn_food(self):
        while True:
            food_pos = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
            if food_pos not in self.snake:
                return food_pos

    def move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            # Remove tail if not eating
            self.snake.pop()

    def draw(self):
        screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, 
                (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                 GRID_SIZE-1, GRID_SIZE-1))

        # Draw food
        pygame.draw.rect(screen, RED, 
            (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE, 
             GRID_SIZE-1, GRID_SIZE-1))

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Handle key presses for direction
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)

            self.move_snake()
            self.draw()

            # Game speed (frames per second) Change to adjust speed
            clock.tick(10)

            if self.game_over:
                # Game over screen
                screen.fill(BLACK)
                game_over_text = self.font.render('Game Over!', True, WHITE)
                score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
                
                screen.blit(game_over_text, 
                    (WIDTH//2 - game_over_text.get_width()//2, 
                     HEIGHT//2 - 50))
                screen.blit(score_text, 
                    (WIDTH//2 - score_text.get_width()//2, 
                     HEIGHT//2 + 50))
                
                pygame.display.flip()
                pygame.time.wait(2000)
                break

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
