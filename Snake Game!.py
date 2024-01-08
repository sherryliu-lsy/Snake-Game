import pygame
from pygame.locals import *
# this will insert some global variables, e.g. KEY-DOWN
import time
import random
import math

size = 40
start_length = 1
w1, w2 = 640, 640
window = (w1, w2)
bg_color = (109, 170, 45)
score_color = (55, 112, 4)
end_color = (216, 245, 193)
font1 = "consolas"


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = size*(random.randint(0, int(w1/size-1)))
        self.y = size*(random.randint(0, int(w2/size-1)))

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, int(w1/size-1))*size
        self.y = random.randint(0, int(w2/size-1))*size


class Snake:

    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert()
        # upload the image "block" in the folder "resources"
        self.x = [size]*length
        self.y = [size]*length
        # x and y coordinates of the block in the window
        # where you want the picture to appear on the window
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        # every time you update the block's position to be displayed
        self.parent_screen.fill(bg_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] -= size
        if self.direction == "down":
            self.y[0] += size
        if self.direction == "left":
            self.x[0] -= size
        if self.direction == "right":
            self.x[0] += size
        self.draw()


class Game:

    def __init__(self):
        pygame.display.set_caption('Sssnake Game :)')
        pygame.init()

        pygame.display.init()
        self.play_bg_music()
        self.surface = pygame.display.set_mode(window)
        # this opens up an empty display window
        self.surface.fill(bg_color)
        # (red, green, blue), can search this color code on google to create any color
        self.snake = Snake(self.surface, start_length)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.highscore = 1

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def is_wall(self, x, y):
        if x[0] < 0 or x[0] >= w1 or y[0] < 0 or y[0] >= w2:
            return True
        return False

    def display_score(self):
        font = pygame.font.SysFont(font1, 30)
        score = font.render(f"Score: {self.snake.length}", True, score_color)
        self.surface.blit(score, (w2-200, 50))
        if self.snake.length >= self.highscore:
            self.highscore = self.snake.length
        highscore = font.render(f"\^o^/: {self.highscore}", True, score_color)
        self.surface.blit(highscore, (w2-200, 10))

    def play_sound(self, sound):
        s = pygame.mixer.Sound("resources/" + sound + ".wav")
        s.play()
        
    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake eats itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over"  # raises an exception

        if self.is_wall(self.snake.x, self.snake.y):
            raise "Game over"

    def show_game_over(self):
        pygame.mixer.music.pause()
        self.play_sound("bounce")
        time.sleep(2)

        if self.snake.length >= self.highscore:
            self.highscore = self.snake.length

        self.surface.fill(bg_color)
        font = pygame.font.SysFont(font1, 50)
        line01 = font.render(f"High score: {self.highscore}", True, end_color)
        self.surface.blit(line01, (w1/2-220, w2/2-200))
        line1 = font.render(f"Score: {self.snake.length}", True, end_color)
        self.surface.blit(line1, (w1/2-220, w2/2-120))

        font = pygame.font.SysFont(font1, 30)
        line3 = font.render("Press Enter to play again!", True, end_color)
        self.surface.blit(line3, (w1/2-220, w2/2))
        line4 = font.render("Press ESC to exit!", True, end_color)
        self.surface.blit(line4, (w1/2-220, w2/2+40))

        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, start_length)
        self.apple = Apple(self.surface)

    def run(self):

        pygame.display.flip()

        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # when clicked "esc" key
                        running = False
                    if event.key == K_RETURN:
                        paused = False
                        pygame.mixer.music.unpause()
                    if event.key == K_SPACE:
                        if paused == True:
                            paused = False
                            pygame.mixer.music.unpause()
                        else:
                            paused = True
                            pygame.mixer.music.pause()
                    if not paused:
                        # moving block up/down and left/right:
                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()

                elif event.type == QUIT:
                    # when you click on the top-right "x" to close the window
                    running = False  # stops the game

            try:
                if not paused:
                    self.play()
            except Exception:
                self.show_game_over()
                paused = True
                self.reset()

            t = -(math.sqrt(0.1 * self.snake.length - 0.1))/10 + 0.3
            if self.snake.length <= 53:
                time.sleep(t)
            else:
                time.sleep(0.07)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
