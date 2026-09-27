import streamlit as st
from PIL import Image
import pygame
import random
import math

# =========================
# STREAMLIT UI SETUP
# =========================
st.set_page_config(page_title="NEON DUEL", layout="centered")
st.title("🕹️ NEON DUEL — Web Arcade")
st.write("If you are running this in the cloud, frames will update automatically below.")

# Create an empty placeholder to stream the gameplay frames
frame_placeholder = st.empty()

# Initialize Pygame and its font module explicitly
pygame.init()
pygame.font.init()

# =========================
# WINDOW DIMENSIONS
# =========================
WIDTH = 900
HEIGHT = 600

# Create a hidden memory surface instead of a desktop window pop-up
screen = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# =========================
# COLORS
# =========================
BLACK = (5, 7, 18)
DARK_BLUE = (10, 15, 35)
BLUE = (50, 180, 255)
CYAN = (80, 255, 240)
RED = (255, 70, 100)
WHITE = (240, 245, 255)
YELLOW = (255, 220, 80)
GRAY = (80, 90, 120)

# =========================
# FONTS
# =========================
title_font = pygame.font.SysFont("Arial", 44, bold=True)
score_font = pygame.font.SysFont("Arial", 70, bold=True)
big_font = pygame.font.SysFont("Arial", 80, bold=True)
font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

# =========================
# PADDLES
# =========================
PADDLE_WIDTH = 18
PADDLE_HEIGHT = 110
PADDLE_SPEED = 8

left = pygame.Rect(
    40,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

right = pygame.Rect(
    WIDTH - 58,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)

# =========================
# BALL
# =========================
BALL_SIZE = 18

ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2,
    HEIGHT // 2 - BALL_SIZE // 2,
    BALL_SIZE,
    BALL_SIZE
)

ball_x = 0
ball_y = 0

# =========================
# SCORE
# =========================
player1_score = 0
player2_score = 0

WIN_SCORE = 5

winner = ""
game_over = False

# =========================
# COUNTDOWN
# =========================
countdown = 3
countdown_timer = pygame.time.get_ticks()

# =========================
# STARS
# =========================
stars = []
for i in range(100):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])

# =========================
# PARTICLES
# =========================
particles = []

def make_particles(x, y, color, amount=15):
    for i in range(amount):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 4)
        particles.append([
            x,
            y,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            random.randint(15, 30),
            color
        ])

def update_particles():
    for particle in particles[:]:
        particle[0] += particle[2]  # Update X position
        particle[1] += particle[3]  # Update Y position
        particle[4] -= 1            # Decrease life timer
        if particle[4] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(
            screen,
            particle[5],
            (int(particle[0]), int(particle[1])),
            3
        )

# =========================
# RESET ROUND
# =========================
def start_countdown(direction):
    global ball_x, ball_y, countdown, countdown_timer
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_x = 0
    ball_y = 0
    countdown = 3
    countdown_timer = pygame.time.get_ticks()
    start_countdown.direction = direction

# =========================
# START BALL
# =========================
def launch_ball():
    global ball_x, ball_y
    direction = getattr(start_countdown, "direction", 1)
    ball_x = 6 * direction
    ball_y = random.choice([-4, -3, 3, 4])

# =========================
# BACKGROUND
# =========================
def draw_background():
    screen.fill(BLACK)

    # Grid
    for x in range(0, WIDTH, 45):
        pygame.draw.line(screen, DARK_BLUE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 45):
        pygame.draw.line(screen, DARK_BLUE, (0, y), (WIDTH, y))

    # Stars
    for star in stars:
        pygame.draw.circle(screen, GRAY, (star[0], star[1]), star[2])

    # Arena border
    pygame.draw.rect(screen, BLUE, (10, 10, WIDTH - 20, HEIGHT - 20), 3, border_radius=12)

    # Middle line
    for y in range(20, HEIGHT, 35):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 18))

# =========================
# PADDLE DRAWING
# =========================
def draw_paddle(paddle, color):
    glow = (color[0] // 3, color[1] // 3, color[2] // 3)
    pygame.draw.rect(screen, glow, paddle.inflate(10, 10), border_radius=8)
    pygame.draw.rect(screen, color, paddle, border_radius=6)
    pygame.draw.rect(screen, WHITE, (paddle.x + 4, paddle.y + 10, 3, paddle.height - 20), border_radius=2)

# =========================
# BALL DRAWING
# =========================
def draw_ball():
    pygame.draw.circle(screen, (100, 80, 30), ball.center, 18)
    pygame.draw.circle(screen, YELLOW, ball.center, BALL_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (ball.centerx - 3, ball.centery - 3), 3)

# =========================
# START FIRST ROUND
# =========================
start_countdown(random.choice([-1, 1]))

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    # Handle Pygame Events internally
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # =====================
    # COUNTDOWN TIMING
    # =====================
    if not game_over:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - countdown_timer

        if elapsed >= 1000 and countdown > 0:
            countdown -= 1
            countdown_timer = current_time
            if countdown == 0:
                launch_ball()

    # =====================
    # GAMEPLAY PHYSICS & LOGIC
    # =====================
    if not game_over and countdown == 0:
        # Simple placeholder autonomous movement so the game plays itself on the web
        # (Since standard desktop key listeners don't cross the cloud fluidly)
        if ball.centery < left.centery and random.random() < 0.70:
            left.y -= PADDLE_SPEED
        elif ball.centery > left.centery and random.random() < 0.70:
            left.y += PADDLE_SPEED

        if ball.centery < right.centery and random.random() < 0.70:
            right.y -= PADDLE_SPEED
        elif ball.centery > right.centery and random.random() < 0.70:
            right.y += PADDLE_SPEED

        # Keep paddles inside boundaries
        left.top = max(15, left.top)
        left.bottom = min(HEIGHT - 15, left.bottom)
        right.top = max(15, right.top)
        right.bottom = min(HEIGHT - 15, right.bottom)

        # Move Ball
        ball.x += int(ball_x)
        ball.y += int(ball_y)

        # Wall Collisions
        if ball.top <= 15:
            ball.top = 15
            ball_y *= -1
            make_particles(ball.centerx, ball.centery, CYAN)

        if ball.bottom >= HEIGHT - 15:
            ball.bottom = HEIGHT - 15
            ball_y *= -1
            make_particles(ball.centerx, ball.centery, CYAN)

        # Left Paddle Collisions
        if ball.colliderect(left) and ball_x < 0:
            ball.left = left.right
            ball_x *= -1
            difference = ball.centery - left.centery
            ball_y = difference / 12
            if abs(ball_x) < 13:
                ball_x *= 1.08
            make_particles(ball.centerx, ball.centery, BLUE, 20)

        # Right Paddle Collisions
        if ball.colliderect(right) and ball_x > 0:
            ball.right = right.left
            ball_x *= -1
            difference = ball.centery - right.centery
            ball_y = difference / 12
            if abs(ball_x) < 13:
                ball_x *= 1.08
            make_particles(ball.centerx, ball.centery, RED, 20)

        # Score Calculations
        if ball.right < 0:
            player2_score += 1
            make_particles(0, ball.centery, RED, 35)
            if player2_score >= WIN_SCORE:
                game_over = True
                winner = "PLAYER 2 WINS!"
            else:
                start_countdown(1)

        if ball.left > WIDTH:
            player1_score += 1
            make_particles(WIDTH, ball.centery, BLUE, 35)
            if player1_score >= WIN_SCORE:
                game_over = True
                winner = "PLAYER 1 WINS!"
            else:
                start_countdown(-1)

    # =====================
    # RENDERING
    # =====================
    update_particles()
    draw_background()
    draw_particles()
    draw_paddle(left, BLUE)
    draw_paddle(right, RED)
    draw_ball()

    # Overlay Title
    title = title_font.render("NEON DUEL", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 25))

    # Player Labels
    p1 = small_font.render("PLAYER 1  (AI)", True, BLUE)
    p2 = small_font.render("PLAYER 2  (AI)", True, RED)
    screen.blit(p1, (35, HEIGHT - 35))
    screen.blit(p2, (WIDTH - p2.get_width() - 35, HEIGHT - 35))

    # Scoreboards
    score1 = score_font.render(str(player1_score), True, BLUE)
    score2 = score_font.render(str(player2_score), True, RED)
    screen.blit(score1, (WIDTH // 2 - 110, 75))
    screen.blit(score2, (WIDTH // 2 + 70, 75))

    # Countdown Numbers
    if not game_over and countdown > 0:
        countdown_text = big_font.render(str(countdown), True, YELLOW)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
    elif not game_over and countdown == 0 and ball_x != 0:
        if pygame.time.get_ticks() - countdown_timer < 500:
            go_text = font.render("GO!", True, CYAN)
