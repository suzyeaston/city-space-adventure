import pygame
import os
import random
from moviepy.editor import ImageSequenceClip

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vancouver Space Adventure")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAR_COLOR = (255, 255, 200)
GIRL_HEAD_COLOR = (255, 223, 186)
GIRL_BODY_COLOR = (135, 206, 250)
BASS_COLOR = (255, 0, 0)
BUILDING_COLORS = [(70, 130, 180), (60, 120, 200), (50, 110, 190)]
WINDOW_COLOR = (255, 255, 0)
CLOUD_COLOR = (192, 192, 192)

# Fonts
font = pygame.font.Font(None, 40)

# Game elements
clock = pygame.time.Clock()
frames = []
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)
frame_count = 0

# Starfield
stars = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT), "size": random.randint(1, 3)} for _ in range(100)]

# Clouds
clouds = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(-200, 0), "speed": random.randint(1, 3)} for _ in range(5)]

# Skyline
buildings = [{"x": i, "width": 80, "height": random.randint(150, 300), "color": random.choice(BUILDING_COLORS)} for i in range(0, SCREEN_WIDTH, 100)]

# Girl's attributes
girl_x, girl_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200
girl_dx = 5

# Function to draw stars
def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (star["x"], star["y"]), star["size"])
        star["y"] += 1
        if star["y"] > SCREEN_HEIGHT:
            star["x"] = random.randint(0, SCREEN_WIDTH)
            star["y"] = 0

# Function to draw clouds
def draw_clouds():
    for cloud in clouds:
        pygame.draw.ellipse(screen, CLOUD_COLOR, (cloud["x"], cloud["y"], 150, 60))
        cloud["y"] += cloud["speed"]
        if cloud["y"] > SCREEN_HEIGHT:
            cloud["x"] = random.randint(0, SCREEN_WIDTH)
            cloud["y"] = random.randint(-200, 0)

# Function to draw skyline with windows
def draw_skyline():
    for building in buildings:
        pygame.draw.rect(screen, building["color"], (building["x"], SCREEN_HEIGHT - building["height"], building["width"], building["height"]))
        # Add windows
        for i in range(building["x"] + 10, building["x"] + building["width"] - 10, 20):
            for j in range(SCREEN_HEIGHT - building["height"] + 10, SCREEN_HEIGHT - 10, 20):
                pygame.draw.rect(screen, WINDOW_COLOR, (i, j, 10, 10))
        # Scroll buildings
        building["x"] -= 2
        if building["x"] < -building["width"]:
            building["x"] = SCREEN_WIDTH
            building["height"] = random.randint(150, 300)
            building["color"] = random.choice(BUILDING_COLORS)

# Function to draw the girl with ponytail and bass guitar
def draw_girl(x, y):
    # Head
    pygame.draw.circle(screen, GIRL_HEAD_COLOR, (x + 25, y), 20)
    # Ponytail
    pygame.draw.ellipse(screen, GIRL_HEAD_COLOR, (x + 40, y - 10, 15, 30))
    # Body
    pygame.draw.rect(screen, GIRL_BODY_COLOR, (x + 15, y + 20, 20, 50))
    # Arms
    pygame.draw.line(screen, GIRL_BODY_COLOR, (x + 15, y + 40), (x - 10, y + 60), 5)
    pygame.draw.line(screen, GIRL_BODY_COLOR, (x + 35, y + 40), (x + 60, y + 60), 5)
    # Bass Guitar
    pygame.draw.rect(screen, BASS_COLOR, (x - 10, y + 60, 10, 80))
    pygame.draw.line(screen, WHITE, (x - 5, y + 60), (x - 5, y + 140), 2)
    # Legs
    pygame.draw.line(screen, GIRL_BODY_COLOR, (x + 20, y + 70), (x + 10, y + 110), 5)
    pygame.draw.line(screen, GIRL_BODY_COLOR, (x + 30, y + 70), (x + 40, y + 110), 5)

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Draw animated elements
    draw_stars()
    draw_clouds()
    draw_skyline()
    draw_girl(girl_x, girl_y)

    # Girl movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and girl_x > 0:
        girl_x -= girl_dx
    if keys[pygame.K_RIGHT] and girl_x < SCREEN_WIDTH - 50:
        girl_x += girl_dx

    # Save the frame
    frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
    pygame.image.save(screen, frame_path)
    frames.append(frame_path)
    frame_count += 1

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Stop Pygame
pygame.quit()

# Compile frames into a video
clip = ImageSequenceClip(frames, fps=30)
clip.write_videofile("city_space_adventure.mp4", codec="libx264")

# Clean up frames
for frame in frames:
    os.remove(frame)

print("Animation complete. Video saved as city_space_adventure.mp4")
