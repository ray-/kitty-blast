import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
GRID_SIZE = 8  # 8x8 grid
BLOCK_SIZE = 50
SCREEN_WIDTH = GRID_SIZE * BLOCK_SIZE
SCREEN_HEIGHT = GRID_SIZE * BLOCK_SIZE + 100  # Extra space for score
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Kitty’s Sweet Block Party")

# Colors (pastel Sanrio vibes)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)    # Hello Kitty bow
BLUE = (173, 216, 230)    # Cinnamoroll cloud
YELLOW = (255, 255, 224)  # Pompompurin star
BLACK = (0, 0, 0)

# Block types
BLOCK_TYPES = [PINK, BLUE, YELLOW]  # Representing bow, cloud, star

# Initialize grid
grid = [[random.choice(BLOCK_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Game variables
score = 0
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Function to draw the grid
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] is not None:  # Skip None values
                pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

# Function to find matches (3 or more in a row/column)
def find_matches():
    matches = set()
    # Horizontal matches
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2] != None:
                matches.add((y, x))
                matches.add((y, x + 1))
                matches.add((y, x + 2))
    # Vertical matches
    for y in range(GRID_SIZE - 2):
        for x in range(GRID_SIZE):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x] != None:
                matches.add((y, x))
                matches.add((y + 1, x))
                matches.add((y + 2, x))
    return matches

# Function to remove matches and update score
def remove_matches(matches):
    global score
    for (y, x) in matches:
        grid[y][x] = None
        score += 10

# Function to drop blocks down
def drop_blocks():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 1, -1, -1):
            if grid[y][x] is None:
                for above in range(y - 1, -1, -1):
                    if grid[above][x] is not None:
                        grid[y][x] = grid[above][x]
                        grid[above][x] = None
                        break
        # Fill empty spots at the top
        if grid[0][x] is None:
            grid[0][x] = random.choice(BLOCK_TYPES)

# Main game loop
running = True
selected = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get clicked block
            x, y = event.pos
            grid_x, grid_y = x // BLOCK_SIZE, y // BLOCK_SIZE
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                if selected is None:
                    selected = (grid_y, grid_x)
                elif (abs(selected[0] - grid_y) + abs(selected[1] - grid_x)) == 1:  # Adjacent swap
                    # Swap blocks
                    grid[selected[0]][selected[1]], grid[grid_y][grid_x] = grid[grid_y][grid_x], grid[selected[0]][selected[1]]
                    # Check for matches after swap
                    matches = find_matches()
                    if matches:
                        remove_matches(matches)
                        drop_blocks()
                    else:
                        # Swap back if no matches
                        grid[selected[0]][selected[1]], grid[grid_y][grid_x] = grid[grid_y][grid_x], grid[selected[0]][selected[1]]
                    selected = None

    # Draw everything
    screen.fill(WHITE)
    draw_grid()

    # Highlight selected block
    if selected:
        pygame.draw.rect(screen, BLACK, (selected[1] * BLOCK_SIZE, selected[0] * BLOCK_SIZE, BLOCK_SIZE - 2, BLOCK_SIZE - 2), 3)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 80))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()