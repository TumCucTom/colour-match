import pygame
import random
import sys

# Config
GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 5
WINDOW_SIZE = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
FPS = 60
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 40))
pygame.display.set_caption("Color Merge Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Board setup
def new_tile():
    return random.choice(COLORS)

def create_board():
    return [[new_tile() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

board = create_board()
score = 0

# Draw function
def draw_board():
    screen.fill((30, 30, 30))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = board[y][x]
            if color:
                rect = pygame.Rect(
                    x * (TILE_SIZE + MARGIN) + MARGIN,
                    y * (TILE_SIZE + MARGIN) + MARGIN,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(screen, color, rect, border_radius=10)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, WINDOW_SIZE + 5))
    pygame.display.flip()

# Move logic
def slide_and_merge(row):
    global score
    new_row = [tile for tile in row if tile is not None]
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] = None
            new_row[i + 1] = None
            score += 1
            i += 2
        else:
            i += 1
    new_row = [tile for tile in new_row if tile is not None]
    while len(new_row) < GRID_SIZE:
        new_row.append(None)
    return new_row

def rotate_board(clockwise=True):
    if clockwise:
        return [list(reversed(col)) for col in zip(*board)]
    else:
        return list(zip(*[reversed(row) for row in board]))

def move(direction):
    global board
    changed = False
    if direction == 'up':
        board[:] = rotate_board(False)
    elif direction == 'down':
        board[:] = rotate_board(True)

    for y in range(GRID_SIZE):
        row = board[y]
        new_row = slide_and_merge(row)
        if new_row != row:
            changed = True
        board[y] = new_row

    if direction == 'up':
        board[:] = rotate_board(True)
    elif direction == 'down':
        board[:] = rotate_board(False)
    elif direction == 'right':
        board = [list(reversed(row)) for row in board]
        for y in range(GRID_SIZE):
            row = board[y]
            new_row = slide_and_merge(row)
            if new_row != row:
                changed = True
            board[y] = new_row
        board = [list(reversed(row)) for row in board]
    elif direction == 'left':
        for y in range(GRID_SIZE):
            row = board[y]
            new_row = slide_and_merge(row)
            if new_row != row:
                changed = True
            board[y] = new_row

    if changed:
        spawn_new_tiles()

def spawn_new_tiles():
    empty = [(y, x) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if board[y][x] is None]
    for _ in range(min(2, len(empty))):
        y, x = random.choice(empty)
        board[y][x] = new_tile()
        empty.remove((y, x))

# Main loop
running = True
draw_board()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move('up')
            elif event.key == pygame.K_DOWN:
                move('down')
            elif event.key == pygame.K_LEFT:
                move('left')
            elif event.key == pygame.K_RIGHT:
                move('right')

    draw_board()
    clock.tick(FPS)

pygame.quit()
sys.exit()
