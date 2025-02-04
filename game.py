import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set default parameters
DEFAULT_SIZE = 75  # Increase the grid size
DEFAULT_INTERVAL = 200  # milliseconds
CELL_SIZE = 10  # pixel size of each cell

# Initialize window
width = DEFAULT_SIZE * CELL_SIZE
height = width + 100  # extra space for buttons and information
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Initialize grid
grid = np.zeros((DEFAULT_SIZE, DEFAULT_SIZE), dtype=int)
grid = np.random.choice([0, 1], size=(DEFAULT_SIZE, DEFAULT_SIZE))  # random initialization

# Initialize button area
button_width = 100
button_height = 30
speed_up_button = pygame.Rect(10, height - 90, button_width, button_height)
speed_down_button = pygame.Rect(120, height - 90, button_width, button_height)
restart_button = pygame.Rect(230, height - 90, button_width, button_height)
resize_button = pygame.Rect(340, height - 90, button_width, button_height)

# Initialize interval
interval = DEFAULT_INTERVAL
last_update = 0

# Font
font = pygame.font.SysFont('Arial', 20)

# Main loop
running = True
pause = False

while running:
    current_time = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Click speed up button
            if speed_up_button.collidepoint(mouse_pos):
                interval = max(10, interval - 20)
            # Click speed down button
            elif speed_down_button.collidepoint(mouse_pos):
                interval += 20
            # Click restart button
            elif restart_button.collidepoint(mouse_pos):
                grid = np.random.choice([0, 1], size=(DEFAULT_SIZE, DEFAULT_SIZE))
                interval = DEFAULT_INTERVAL
            # Click resize button
            elif resize_button.collidepoint(mouse_pos):
                new_size = int(input("Enter new grid size: "))
                if new_size > 0:
                    DEFAULT_SIZE = new_size
                    width = new_size * CELL_SIZE
                    height = width + 100
                    screen = pygame.display.set_mode((width, height))
                    grid = np.random.choice([0, 1], size=(new_size, new_size))

    # Update grid
    if not pause and current_time - last_update >= interval:
        new_grid = np.zeros_like(grid)
        rows, cols = grid.shape
        for i in range(rows):
            for j in range(cols):
                # Calculate number of living neighbors
                total = int(
                    (grid[i, (j-1)%cols] + grid[i, (j+1)%cols] +
                     grid[(i-1)%rows, j] + grid[(i+1)%rows, j] +
                     grid[(i-1)%rows, (j-1)%cols] + grid[(i-1)%rows, (j+1)%cols] +
                     grid[(i+1)%rows, (j-1)%cols] + grid[(i+1)%rows, (j+1)%cols])
                )
                # Apply Game of Life rules
                if grid[i, j] == 1 and (total < 2 or total > 3):
                    new_grid[i, j] = 0
                elif grid[i, j] == 0 and total == 3:
                    new_grid[i, j] = 1
                else:
                    new_grid[i, j] = grid[i, j]
        grid = new_grid
        last_update = current_time

    # Render screen
    screen.fill(WHITE)
    
    # Draw grid
    for i in range(rows):
        for j in range(cols):
            color = GREEN if grid[i, j] == 1 else WHITE
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    
    # Draw buttons
    pygame.draw.rect(screen, GRAY, speed_up_button)
    pygame.draw.rect(screen, GRAY, speed_down_button)
    pygame.draw.rect(screen, GRAY, restart_button)
    pygame.draw.rect(screen, GRAY, resize_button)

    # Draw button text
    speed_up_text = font.render("Speed Up", True, BLACK)
    speed_down_text = font.render("Slow Down", True, BLACK)
    restart_text = font.render("Restart", True, BLACK)
    resize_text = font.render("Resize", True, BLACK)
    
    screen.blit(speed_up_text, (speed_up_button.x + 10, speed_up_button.y + 5))
    screen.blit(speed_down_text, (speed_down_button.x + 10, speed_down_button.y + 5))
    screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 5))
    screen.blit(resize_text, (resize_button.x + 10, resize_button.y + 5))

    # Display number of living cells
    alive_count = np.sum(grid)
    alive_text = font.render(f"Living Cells: {alive_count}", True, BLACK)
    screen.blit(alive_text, (10, height - 50))

    pygame.display.flip()

pygame.quit()
