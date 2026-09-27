import pygame
import random
import math

pygame.init()

# =========================
# WINDOW
# =========================
WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON DUEL")

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
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 1

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
    global ball_x, ball_y
    global countdown, countdown_timer

    ball.center = (WIDTH // 2, HEIGHT // 2)

    # Ball doesn't move during countdown
    ball_x = 0
    ball_y = 0

    countdown = 3
    countdown_timer = pygame.time.get_ticks()

    # Store the direction for after countdown
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
        pygame.draw.line(
            screen,
            DARK_BLUE,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, 45):
        pygame.draw.line(
            screen,
            DARK_BLUE,
            (0, y),
            (WIDTH, y)
        )

    # Stars
    for star in stars:
        pygame.draw.circle(
            screen,
            GRAY,
            (star[0], star[1]),
            star[2]
        )

    # Arena border
    pygame.draw.rect(
        screen,
        BLUE,
        (10, 10, WIDTH - 20, HEIGHT - 20),
        3,
        border_radius=12
    )

    # Middle line
    for y in range(20, HEIGHT, 35):
        pygame.draw.rect(
            screen,
            GRAY,
            (WIDTH // 2 - 2, y, 4, 18)
        )


# =========================
# PADDLE DRAWING
# =========================
def draw_paddle(paddle, color):

    # Glow
    glow = (
        color[0] // 3,
        color[1] // 3,
        color[2] // 3
    )

    pygame.draw.rect(
        screen,
        glow,
        paddle.inflate(10, 10),
        border_radius=8
    )

    # Paddle
    pygame.draw.rect(
        screen,
        color,
        paddle,
        border_radius=6
    )

    # Highlight
    pygame.draw.rect(
        screen,
        WHITE,
        (
            paddle.x + 4,
            paddle.y + 10,
            3,
            paddle.height - 20
        ),
        border_radius=2
    )


# =========================
# BALL DRAWING
# =========================
def draw_ball():

    # Glow
    pygame.draw.circle(
        screen,
        (100, 80, 30),
        ball.center,
        18
    )

    # Ball
    pygame.draw.circle(
        screen,
        YELLOW,
        ball.center,
        BALL_SIZE // 2
    )

    # Highlight
    pygame.draw.circle(
        screen,
        WHITE,
        (
            ball.centerx - 3,
            ball.centery - 3
        ),
        3
    )


# =========================
# START FIRST ROUND
# =========================
start_countdown(random.choice([-1, 1]))

# =========================
# MAIN LOOP
# =========================
running = True

while running:

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Quit
            if event.key == pygame.K_ESCAPE:
                running = False

            # Restart after winning
            if event.key == pygame.K_SPACE and game_over:

                player1_score = 0
                player2_score = 0

                left.centery = HEIGHT // 2
                right.centery = HEIGHT // 2

                winner = ""
                game_over = False

                start_countdown(random.choice([-1, 1]))

    # =====================
    # COUNTDOWN
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
    # CONTROLS
    # =====================
    keys = pygame.key.get_pressed()

    # Only allow movement when ball is active
    if not game_over and countdown == 0:

        # PLAYER 1
        if keys[pygame.K_w]:
            left.y -= PADDLE_SPEED

        if keys[pygame.K_s]:
            left.y += PADDLE_SPEED

        # PLAYER 2
        if keys[pygame.K_UP]:
            right.y -= PADDLE_SPEED

        if keys[pygame.K_DOWN]:
            right.y += PADDLE_SPEED

        # Keep paddles inside
        left.top = max(15, left.top)
        left.bottom = min(HEIGHT - 15, left.bottom)

        right.top = max(15, right.top)
        right.bottom = min(HEIGHT - 15, right.bottom)

        # =====================
        # BALL MOVEMENT
        # =====================
        ball.x += int(ball_x)
        ball.y += int(ball_y)

        # =====================
        # WALL COLLISION
        # =====================
        if ball.top <= 15:

            ball.top = 15
            ball_y *= -1

            make_particles(
                ball.centerx,
                ball.centery,
                CYAN
            )

        if ball.bottom >= HEIGHT - 15:

            ball.bottom = HEIGHT - 15
            ball_y *= -1

            make_particles(
                ball.centerx,
                ball.centery,
                CYAN
            )

        # =====================
        # LEFT PADDLE
        # =====================
        if ball.colliderect(left) and ball_x < 0:

            ball.left = left.right
            ball_x *= -1

            difference = ball.centery - left.centery
            ball_y = difference / 12

            if abs(ball_x) < 13:
                ball_x *= 1.08

            make_particles(
                ball.centerx,
                ball.centery,
                BLUE,
                20
            )

        # =====================
        # RIGHT PADDLE
        # =====================
        if ball.colliderect(right) and ball_x > 0:

            ball.right = right.left
            ball_x *= -1

            difference = ball.centery - right.centery
            ball_y = difference / 12

            if abs(ball_x) < 13:
                ball_x *= 1.08

            make_particles(
                ball.centerx,
                ball.centery,
                RED,
                20
            )

        # =====================
        # PLAYER 1 SCORES
        # =====================
        if ball.right < 0:

            player2_score += 1

            make_particles(
                0,
                ball.centery,
                RED,
                35
            )

            if player2_score >= WIN_SCORE:

                game_over = True
                winner = "PLAYER 2 WINS!"

            else:

                start_countdown(1)

        # =====================
        # PLAYER 2 SCORES
        # =====================
        if ball.left > WIDTH:

            player1_score += 1

            make_particles(
                WIDTH,
                ball.centery,
                BLUE,
                35
            )

            if player1_score >= WIN_SCORE:

                game_over = True
                winner = "PLAYER 1 WINS!"

            else:

                start_countdown(-1)

    # =====================
    # UPDATE PARTICLES
    # =====================
    update_particles()

    # =====================
    # DRAW
    # =====================
    draw_background()

    draw_particles()

    draw_paddle(left, BLUE)
    draw_paddle(right, RED)

    draw_ball()

    # =====================
    # TITLE
    # =====================
    title = title_font.render(
        "NEON DUEL",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            25
        )
    )

    # =====================
    # PLAYER LABELS
    # =====================
    p1 = small_font.render(
        "PLAYER 1  [ W / S ]",
        True,
        BLUE
    )

    p2 = small_font.render(
        "PLAYER 2  [ UP / DOWN ]",
        True,
        RED
    )

    screen.blit(
        p1,
        (35, HEIGHT - 35)
    )

    screen.blit(
        p2,
        (
            WIDTH - p2.get_width() - 35,
            HEIGHT - 35
        )
    )

    # =====================
    # SCORES
    # =====================
    score1 = score_font.render(
        str(player1_score),
        True,
        BLUE
    )

    score2 = score_font.render(
        str(player2_score),
        True,
        RED
    )

    screen.blit(
        score1,
        (
            WIDTH // 2 - 110,
            75
        )
    )

    screen.blit(
        score2,
        (
            WIDTH // 2 + 70,
            75
        )
    )

    # =====================
    # COUNTDOWN DISPLAY
    # =====================
    if not game_over and countdown > 0:

        countdown_text = big_font.render(
            str(countdown),
            True,
            YELLOW
        )

        screen.blit(
            countdown_text,
            (
                WIDTH // 2 - countdown_text.get_width() // 2,
                HEIGHT // 2 - countdown_text.get_height() // 2
            )
        )

    # =====================
    # GO!
    # =====================
    elif not game_over and countdown == 0 and ball_x != 0:

        # Only show GO briefly
        if pygame.time.get_ticks() - countdown_timer < 500:

            go_text = font.render(
                "GO!",
                True,
                CYAN
            )

            screen.blit(
                go_text,
                (
                    WIDTH // 2 - go_text.get_width() // 2,
                    HEIGHT // 2 - 80
                )
            )

    # =====================
    # GAME OVER
    # =====================
    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 200)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        winner_text = title_font.render(
            winner,
            True,
            YELLOW
        )

        screen.blit(
            winner_text,
            (
                WIDTH // 2 - winner_text.get_width() // 2,
                210
            )
        )

        final_score = font.render(
            f"{player1_score}  -  {player2_score}",
            True,
            WHITE
        )

        screen.blit(
            final_score,
            (
                WIDTH // 2 - final_score.get_width() // 2,
                270
            )
        )

        restart_text = font.render(
            "SPACE = PLAY AGAIN",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                330
            )
        )

        quit_text = small_font.render(
            "ESC = QUIT",
            True,
            GRAY
        )

        screen.blit(
            quit_text,
            (
                WIDTH // 2 - quit_text.get_width() // 2,
                370
            )
        )

    # =====================
    # UPDATE SCREEN
    # =====================
    pygame.display.flip()

    clock.tick(60)

pygame.quit()