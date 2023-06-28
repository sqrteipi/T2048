import sys
import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 250, 500
GRID_SIZE = 25

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (107, 0, 7)
COLORS = [RED, BLUE, GREEN]
GRAVITY = 10
DIFFICULTY = "Asia"
WIND = [False, "Left", 0]
WATER = False
TYPHOON = [False, 0]
SNOWING = [False, 0]
EARTHQUAKE = False
VOLCANIC = [False, 0]

# Read new score
with open("new_score.txt") as f:
    highest_score = int(f.readline())
    f.close()

# Tetromino shapes

SHAPES = [
    [
        ['.....',
         '.....',
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         'O....',
         'O....',
         'O....',
         'O....']
    ],
    [
        ['.....',
        '.....',
        'OO...',
        'OO...',
        '.....'],
        ['.....',
        '.....',
        'OO...',
        'OO...',
        '.....']
    ],
    [
        ['.....',
         '.....',
         '.O...',
         'OOO..',
         '.....'],
        ['.....',
         '.O...',
         'OO...',
         '.O...',
         '.....'],
        ['.....',
         '.....',
         'OOO..',
         '.O...',
         '.....'],
        ['.....',
         'O....',
         'OO...',
         'O....',
         '.....']
    ],
    [
        [
         '.....',
         '.....',
         '.OO..',
         'OO...',
         '.....'],
        ['.....',
         'O....',
         'OO...',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '.....',
         'OO...',
         '.OO..',
         '.....'],
        ['.....',
         '.O...',
         'OO...',
         'O....',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         'OOO..',
         '.....',
         '.....'],
        ['.....',
         'OO...',
         '.O...',
         '.O...',
         '.....'],
        ['.....',
         '.....',
         'OOO..',
         'O....',
         '.....'],
        ['.....',
         'O....',
         'O....',
         'OO...',
         '.....'],
    ],
    [
        [
         '.....',
         'O....',
         'OOO..',
         '.....',
         '.....'],
        ['.....',
         'OO...',
         'O....',
         'O....',
         '.....'],
        ['.....',
         '.....',
         'OOO..',
         '..O..',
         '.....'],
        ['.....',
         '.O...',
         '.O...',
         'OO...',
         '.....'],
    ],
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS) # You can choose different colors for each shape
        self.rotation = 0

class colour_tetromino:
    def __init__(self, x, y, shape, colour):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = colour
        self.rotation = 0
class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0  # Add score attribute
        self.snow_list = []
        self.volcanic_list = []
        self.to_be_color = []
        # self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        # self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        # pygame.mixer.music.load("Sounds/music.ogg")
        # pygame.mixer.music.play(-1)

    def new_piece(self):
        # Choose a random shape
        randnum = random.randint(1, 100)
        if DIFFICULTY == "Noob":
            if randnum <= 50:
                shape = SHAPES[0]
            else:
                shape = SHAPES[1]
        elif DIFFICULTY == "Easy":
            if randnum <= 25:
                shape = SHAPES[0]
            elif randnum <= 50:
                shape = SHAPES[1]
            else:
                shape = shape = random.choice(SHAPES[2:])
        elif DIFFICULTY == "Hard":
            if randnum <= 15:
                shape = SHAPES[0]
            elif randnum <= 30:
                shape = SHAPES[1]
            else:
                shape = random.choice(SHAPES[2:])
        elif DIFFICULTY == "Glitch":
            if randnum <= 5:
                shape = SHAPES[0]
            elif randnum <= 10:
                shape = SHAPES[1]
            elif randnum <= 20:
                shape = SHAPES[2]
            elif randnum <= 50:
                shape = random.choice([SHAPES[4], SHAPES[5]])
            else:
                shape = random.choice([[SHAPES[2], SHAPES[3]]])
        elif DIFFICULTY == "Asian":
            if randnum <= 1:
                shape = SHAPES[0]
            elif randnum <= 6:
                shape = SHAPES[1]
            elif randnum <= 15:
                shape = SHAPES[2]
            elif randnum <= 35:
                shape = random.choice([SHAPES[4], SHAPES[5]])
            else:
                shape = random.choice([SHAPES[2], SHAPES[3]])
        else:
            shape = random.choice(SHAPES)
        # Return a new Tetromino object
        return Tetromino(self.width // 2, 0, shape)

    def snow_block(self):
        shape = [[".....",
                 ".....",
                 "..O..",
                 ".....",
                 "....."]]
        x = random.randint(0, self.width)
        y = 0
        return colour_tetromino(x, y, shape, WHITE)

    def volcanic_block(self):
        shape = [[".....",
                 ".....",
                 "..O..",
                 ".....",
                 "....."]]
        x = random.randint(0, self.width-1)
        y = 0
        return colour_tetromino(x, y, shape, RED)

    def valid_move(self, piece, x, y, rotation):
        """Check if the piece can move to the given position"""
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and ((self.grid[piece.y + i + y][piece.x + j + x] != 0) or piece.y + i + y < 0 or piece.x + j + x < 0):
                        return False
                except IndexError:
                    return False
        return True

    def clear_lines(self):
        """Clear the lines that are full and return the number of cleared lines"""
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        if lines_cleared:
            self.clear_sound.play()
        return lines_cleared

    def random_disappear(self):
        dis = random.randint(0, self.width-1)
        for i in range(self.height):
            self.to_be_color.append(((dis*GRID_SIZE, i*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1), BROWN))
            self.grid[i][dis] =  0

    def lock_piece(self, piece):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O':
                        self.grid[piece.y + i][piece.x + j] = piece.color
                except:
                    pass
        # Clear the lines and update the score
        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100  # Update the score based on the number of cleared lines
        # Create a new piece
        self.current_piece = self.new_piece()
        # Check if the game is over
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def lock_snow_piece(self, piece):
        """Lock the piece in place"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O':
                        self.grid[piece.y + i][piece.x + j] = piece.color
                except:
                    pass

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100  # Update the score based on the number of cleared lines


    def update(self):
        global WIND, SNOWING, TYPHOON, EARTHQUAKE, VOLCANIC
        """Move the tetromino down one cell"""
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

            ''' Wind Function'''
            if WIND[2] >= 10:
                WIND[2] = 0
                WIND[0] = False
            # if WIND[0] and random.randint(0, 1) == 0:
            #     if WIND[1] == "Left":
            #         if self.valid_move(self.current_piece, -1, 0, 0):
            #             self.current_piece.x -= 1
            #     else:
            #         if self.valid_move(self.current_piece, 1, 0, 0):
            #             self.current_piece.x += 1
            #     WIND[2] += 1


            '''Snow Function'''
            if SNOWING[0]:
                if SNOWING[1] >= 5:
                    SNOWING[1] = 0
                    SNOWING[0] = False
                else:
                    self.snow_list.append(self.snow_block())
                    SNOWING[1]+=1

            for snow in self.snow_list:
                if not self.game_over:
                    if self.valid_move(snow, 0, 1, 0):
                        snow.y += 1
                    else:
                        self.lock_snow_piece(snow)
                        self.snow_list.remove(snow)

            '''Typhoon Function'''
            if TYPHOON[1] >= 10:
                TYPHOON[1] = 0
                TYPHOON[0] = False
            # if TYPHOON[0]:
            #     randnum = random.randint(0, 2)
            #     if self.valid_move(self.current_piece, randnum-1, 0, 0):
            #         self.current_piece.x += randnum-1
            #     TYPHOON[1] += 1


            '''Earthquake Function'''
            if EARTHQUAKE:
                self.random_disappear()
                EARTHQUAKE = not EARTHQUAKE


            '''Volcanic Function'''
            if VOLCANIC[0]:
                if VOLCANIC[1] >= 5:
                    VOLCANIC[1] = 0
                    VOLCANIC[0] = False
                else:
                    self.volcanic_list.append(self.volcanic_block())
                    VOLCANIC[1]+=1

            for lava in self.volcanic_list:
                if not self.game_over:
                    if lava.y+1 < self.height:
                        lava.y += 1
                        self.grid[lava.y][lava.x] = 0
                    else:
                        self.volcanic_list.remove(lava)

    def draw(self, screen):
        """Draw the grid and the current piece"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        """Color eqrthquake"""
        for pos, color in self.to_be_color:
            pygame.draw.rect(screen, color, pos)
        self.to_be_color = []

        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        for snow in self.snow_list:
            for i, row in enumerate(snow.shape[snow.rotation % len(snow.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, snow.color, ((snow.x + j) * GRID_SIZE, (snow.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


        for lava in self.volcanic_list:
            for i, row in enumerate(lava.shape[lava.rotation % len(lava.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, lava.color, ((lava.x + j) * GRID_SIZE, (lava.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

def draw_score(screen, score, x, y):
    """Draw the score on the screen"""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (x, y))


def draw_game_over(screen, x, y):
    """Draw the game over text on the screen"""
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (x, y))



def hazards(screen, x, y):
    global WIND, SNOWING, TYPHOON, EARTHQUAKE

    if not (WIND[0] or SNOWING[0] or TYPHOON[0] or EARTHQUAKE):
        randnum = random.randint(1, 100)
        if randnum == 1:
            WIND[0] = True
            WIND[1] = random.choice(["Left", "Right"])
        elif randnum == 2:
            SNOWING[0] = True
        elif randnum == 3:
            TYPHOON[0] = True
        elif randnum == 4:
            EARTHQUAKE = True

    font = pygame.font.Font(None, 36)
    text = font.render("Peaceful", True, WHITE)
    if WIND[0]:
        text = font.render("Windy", True, BLUE)
    elif SNOWING[0]:
        text = font.render("Snowy", True, WHITE)
    elif TYPHOON[0]:
        text = font.render("Typhoon", True, BLUE)
    elif EARTHQUAKE:
        text = font.render("Earthquake", True, BROWN)


    screen.blit(text, (x, y))




def main():
    # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    # Create a clock object
    clock = pygame.time.Clock()
    # Create a Tetris object
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    keys = pygame.key.get_pressed()
    fall_time = 0
    if DIFFICULTY == "Noob":
        fall_speed = 50
    elif DIFFICULTY == "Easy":
        fall_speed = 35
    elif DIFFICULTY == "Normal":
        fall_speed = 20
    elif DIFFICULTY == "Hard":
        fall_speed = 15
    elif DIFFICULTY == "GLITCH":
        fall_speed = 10
    elif DIFFICULTY == "Asian":
        fall_speed = 3
    else:
      fall_speed = 20  # You can adjust this value to change the falling speed, it's in milliseconds

    while True:
        # is_snowing = snowing()
        # if is_snowing:
        #     game.snow_block()

        # Fill the screen with black
        screen.fill(BLACK)
        for event in pygame.event.get():
            # Check for the QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for the KEYDOWN event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1 # Move the piece to the left
                    if WIND[1] or TYPHOON[1]:
                        if game.valid_move(game.current_piece, -1, 0, 0):
                            if random.randint(0, 1) == 0:
                                game.current_piece.x -= 1 # Move the piece to the left
                if event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1 # Move the piece to the right
                    if WIND[2] or TYPHOON[1]:
                        if game.valid_move(game.current_piece, 1, 0, 0):
                            if random.randint(0, 1) == 0:
                                game.current_piece.x += 1 # Move the piece to the left
                if event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1 # Move the piece down
                if event.key == pygame.K_UP:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        # game.rotate_sound.play()
                        game.current_piece.rotation += 1 # Rotate the piece
                if event.key == pygame.K_SPACE:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1 # Move the piece down until it hits the bottom
                    game.lock_piece(game.current_piece) # Lock the piece in place
        # Get the number of milliseconds since the last frame
        delta_time = clock.get_rawtime()
        # Add the delta time to the fall time
        fall_time += delta_time
        if fall_time >= fall_speed:
            # Move the piece down
            game.update()
            # Reset the fall time
            fall_time = 0
        # Draw the score on the screen
        draw_score(screen, game.score, 10, 10)
        hazards(screen, 10, 30)

        # Draw the grid and the current piece
        game.draw(screen)
        if game.game_over:
            # Draw the "Game Over" message
            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)  # Draw the "Game Over" message
            if game.score > highest_score:
                with open("new_score.txt", "w") as f:
                    f.write(str(game.score))
            # You can add a "Press any key to restart" message here
            if event.type == pygame.KEYDOWN:
                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
            # Check for the KEYDOWN event
        # Update the display
        pygame.display.flip()
        # Set the framerate
        clock.tick(60)


if __name__ == "__main__":
    main()
