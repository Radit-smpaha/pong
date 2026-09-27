
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NEON DUEL",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 1200px;
    }

    header, footer, #MainMenu {
        visibility: hidden;
    }

    h1 {
        text-align: center;
        color: #50b4ff;
        text-shadow: 0 0 18px #167aff;
    }

    .subtitle {
        text-align: center;
        color: #a8b9d9;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🕹️ NEON DUEL")
st.markdown(
    '<p class="subtitle">Two players. One arena. First to 5 wins.</p>',
    unsafe_allow_html=True
)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background: #050712;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game-wrapper {
    width: 100%;
    max-width: 1100px;
    margin: auto;
    position: relative;
}

canvas {
    display: block;
    width: 100%;
    aspect-ratio: 3 / 2;
    background: #050712;
    border: 2px solid #236dff;
    border-radius: 12px;
    box-shadow:
        0 0 12px #167aff,
        0 0 35px rgba(22, 122, 255, 0.25);
    touch-action: none;
    outline: none;
}

#controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 4px;
}

.player-info {
    font-size: 14px;
    line-height: 1.8;
    color: #d0dcf5;
}

.blue {
    color: #50b4ff;
    font-weight: bold;
}

.red {
    color: #ff4664;
    font-weight: bold;
}

button {
    border: 1px solid #50b4ff;
    background: #101a35;
    color: white;
    font-size: 15px;
    font-weight: bold;
    padding: 12px 24px;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.15s;
}

button:hover {
    background: #1c3c70;
    box-shadow: 0 0 15px #167aff;
    transform: translateY(-1px);
}

#message {
    text-align: center;
    color: #8ca6d7;
    font-size: 13px;
    padding-bottom: 10px;
}

.mobile-controls {
    display: none;
    justify-content: space-between;
    gap: 12px;
    margin-top: 8px;
}

.mobile-group {
    display: flex;
    gap: 8px;
}

.mobile-controls button {
    width: 65px;
    height: 55px;
    padding: 0;
    font-size: 22px;
    touch-action: none;
    user-select: none;
}

@media (max-width: 700px) {
    .mobile-controls {
        display: flex;
    }

    .player-info {
        font-size: 12px;
    }

    button {
        padding: 10px 15px;
    }
}
</style>
</head>

<body>
<div id="game-wrapper">

    <canvas id="game" width="900" height="600" tabindex="0"></canvas>

    <div id="controls">
        <div class="player-info">
            <span class="blue">PLAYER 1</span><br>
            W / S to move
        </div>

        <button id="restart">↻ RESTART GAME</button>

        <div class="player-info" style="text-align:right">
            <span class="red">PLAYER 2</span><br>
            ↑ / ↓ to move
        </div>
    </div>

    <div id="message">
        Click the arena to focus the game. First to 5 points wins!
    </div>

    <div class="mobile-controls">
        <div class="mobile-group">
            <button id="p1up">↑</button>
            <button id="p1down">↓</button>
        </div>

        <div class="mobile-group">
            <button id="p2up">↑</button>
            <button id="p2down">↓</button>
        </div>
    </div>

</div>

<script>
(() => {
    "use strict";

    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    const W = canvas.width;
    const H = canvas.height;

    const WIN_SCORE = 5;

    const COLORS = {
        black: "#050712",
        darkBlue: "#0a0f23",
        blue: "#32b4ff",
        cyan: "#50fff0",
        red: "#ff4664",
        white: "#f0f5ff",
        yellow: "#ffdc50",
        gray: "#506080"
    };

    const keys = {};

    let lastTime = 0;
    let animationId = null;
    let gameOver = false;
    let countdown = 3;
    let countdownTime = 0;
    let winner = "";
    let particles = [];
    let stars = [];

    let score1 = 0;
    let score2 = 0;

    const paddle = {
        width: 18,
        height: 110,
        speed: 460
    };

    const left = {
        x: 40,
        y: H / 2 - paddle.height / 2,
        w: paddle.width,
        h: paddle.height,
        color: COLORS.blue
    };

    const right = {
        x: W - 58,
        y: H / 2 - paddle.height / 2,
        w: paddle.width,
        h: paddle.height,
        color: COLORS.red
    };

    const ball = {
        x: W / 2,
        y: H / 2,
        r: 10,
        vx: 0,
        vy: 0,
        speed: 390
    };

    function random(min, max) {
        return Math.random() * (max - min) + min;
    }

    function makeStars() {
        stars = [];

        for (let i = 0; i < 120; i++) {
            stars.push({
                x: random(0, W),
                y: random(0, H),
                r: random(1, 2.5),
                alpha: random(0.15, 0.7)
            });
        }
    }

    function createParticles(x, y, color, amount = 18) {
        for (let i = 0; i < amount; i++) {
            const angle = random(0, Math.PI * 2);
            const speed = random(80, 350);

            particles.push({
                x,
                y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: random(0.3, 0.8),
                maxLife: 0.8,
                size: random(2, 5),
                color
            });
        }

        if (particles.length > 700) {
            particles.splice(0, particles.length - 700);
        }
    }

    function resetBall(direction) {
        ball.x = W / 2;
        ball.y = H / 2;
        ball.vx = 0;
        ball.vy = 0;

        countdown = 3;
        countdownTime = 0;
        ball.direction = direction;
    }

    function launchBall() {
        const direction = ball.direction || 1;
        const angle = random(-0.55, 0.55);

        ball.vx = Math.cos(angle) * ball.speed * direction;
        ball.vy = Math.sin(angle) * ball.speed;
    }

    function resetGame() {
        score1 = 0;
        score2 = 0;
        gameOver = false;
        winner = "";

        left.y = H / 2 - left.h / 2;
        right.y = H / 2 - right.h / 2;

        particles = [];

        resetBall(Math.random() < 0.5 ? -1 : 1);
    }

    function clampPaddles() {
        left.y = Math.max(
            15,
            Math.min(H - 15 - left.h, left.y)
        );

        right.y = Math.max(
            15,
            Math.min(H - 15 - right.h, right.y)
        );
    }

    function updatePaddleMovement(dt) {
        if (keys["w"] || keys["W"] || keys["ArrowUp1"]) {
            left.y -= paddle.speed * dt;
        }

        if (keys["s"] || keys["S"] || keys["ArrowDown1"]) {
            left.y += paddle.speed * dt;
        }

        if (keys["ArrowUp"]) {
            right.y -= paddle.speed * dt;
        }

        if (keys["ArrowDown"]) {
            right.y += paddle.speed * dt;
        }

        clampPaddles();
    }

    function circleRectCollision(p, r) {
        const closestX = Math.max(r.x, Math.min(p.x, r.x + r.w));
        const closestY = Math.max(r.y, Math.min(p.y, r.y + r.h));

        const dx = p.x - closestX;
        const dy = p.y - closestY;

        return dx * dx + dy * dy < p.r * p.r;
    }

    function hitPaddle(p, direction) {
        const relativeHit =
            (ball.y - (p.y + p.h / 2)) / (p.h / 2);

        const angle = relativeHit * 0.9;

        ball.speed = Math.min(ball.speed * 1.055, 850);

        ball.vx = Math.cos(angle) * ball.speed * direction;
        ball.vy = Math.sin(angle) * ball.speed;

        if (direction === 1) {
            ball.x = p.x + p.w + ball.r + 1;
        } else {
            ball.x = p.x - ball.r - 1;
        }

        createParticles(
            ball.x,
            ball.y,
            p.color,
            22
        );
    }

    function scorePoint(player) {
        if (player === 1) {
            score1++;
            createParticles(W - 10, ball.y, COLORS.blue, 45);
        } else {
            score2++;
            createParticles(10, ball.y, COLORS.red, 45);
        }

        if (score1 >= WIN_SCORE || score2 >= WIN_SCORE) {
            gameOver = true;
            winner = score1 >= WIN_SCORE
                ? "PLAYER 1 WINS!"
                : "PLAYER 2 WINS!";

            createParticles(W / 2, H / 2, COLORS.yellow, 100);
        } else {
            resetBall(player === 1 ? -1 : 1);
        }
    }

    function updatePhysics(dt) {
        if (gameOver) return;

        if (countdown > 0) {
            countdownTime += dt;

            if (countdownTime >= 1) {
                countdown--;
                countdownTime = 0;

                if (countdown === 0) {
                    launchBall();
                }
            }

            return;
        }

        ball.x += ball.vx * dt;
        ball.y += ball.vy * dt;

        // Top and bottom walls
        if (ball.y - ball.r <= 15) {
            ball.y = 15 + ball.r;
            ball.vy = Math.abs(ball.vy);

            createParticles(ball.x, ball.y, COLORS.cyan, 12);
        }

        if (ball.y + ball.r >= H - 15) {
            ball.y = H - 15 - ball.r;
            ball.vy = -Math.abs(ball.vy);

            createParticles(ball.x, ball.y, COLORS.cyan, 12);
        }

        // Paddle collisions
        if (ball.vx < 0 && circleRectCollision(ball, left)) {
            hitPaddle(left, 1);
        }

        if (ball.vx > 0 && circleRectCollision(ball, right)) {
            hitPaddle(right, -1);
        }

        // Scoring
        if (ball.x + ball.r < 0) {
            scorePoint(2);
        }

        if (ball.x - ball.r > W) {
            scorePoint(1);
        }
    }

    function updateParticles(dt) {
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];

            p.x += p.vx * dt;
            p.y += p.vy * dt;

            p.vx *= Math.pow(0.15, dt);
            p.vy *= Math.pow(0.15, dt);

            p.life -= dt;

            if (p.life <= 0) {
                particles.splice(i, 1);
            }
        }
    }

    function drawBackground() {
        ctx.fillStyle = COLORS.black;
        ctx.fillRect(0, 0, W, H);

        // Background glow
        const gradient = ctx.createRadialGradient(
            W / 2, H / 2, 10,
            W / 2, H / 2, W * 0.65
        );

        gradient.addColorStop(0, "#101b3a");
        gradient.addColorStop(1, "#050712");

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, W, H);

        // Grid
        ctx.strokeStyle = "rgba(50, 100, 200, 0.12)";
        ctx.lineWidth = 1;

        for (let x = 0; x <= W; x += 45) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, H);
            ctx.stroke();
        }

        for (let y = 0; y <= H; y += 45) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(W, y);
            ctx.stroke();
        }

        // Stars
        for (const star of stars) {
            ctx.globalAlpha = star.alpha;
            ctx.fillStyle = "#9cbfff";

            ctx.beginPath();
            ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.globalAlpha = 1;

        // Arena border
        ctx.shadowBlur = 15;
        ctx.shadowColor = COLORS.blue;
        ctx.strokeStyle = COLORS.blue;
        ctx.lineWidth = 3;

        roundRect(ctx, 10, 10, W - 20, H - 20, 12);
        ctx.stroke();

        ctx.shadowBlur = 0;

        // Middle line
        ctx.fillStyle = "rgba(120, 150, 200, 0.5)";

        for (let y = 20; y < H; y += 35) {
            ctx.fillRect(W / 2 - 2, y, 4, 18);
        }
    }

    function roundRect(ctx, x, y, w, h, r) {
        ctx.beginPath();
        ctx.roundRect(x, y, w, h, r);
    }

    function drawPaddle(p) {
        ctx.save();

        ctx.shadowBlur = 25;
        ctx.shadowColor = p.color;

        ctx.fillStyle = p.color;
        roundRect(
            ctx,
            p.x - 3,
            p.y - 3,
            p.w + 6,
            p.h + 6,
            8
        );
        ctx.fill();

        ctx.shadowBlur = 0;

        ctx.fillStyle = "rgba(255,255,255,0.8)";
        roundRect(
            ctx,
            p.x + 4,
            p.y + 10,
            3,
            p.h - 20,
            2
        );
        ctx.fill();

        ctx.restore();
    }

    function drawBall() {
        ctx.save();

        ctx.shadowBlur = 25;
        ctx.shadowColor = COLORS.yellow;

        ctx.fillStyle = COLORS.yellow;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
        ctx.fill();

        ctx.shadowBlur = 0;

        ctx.fillStyle = COLORS.white;
        ctx.beginPath();
        ctx.arc(
            ball.x - 3,
            ball.y - 3,
            3,
            0,
            Math.PI * 2
        );
        ctx.fill();

        ctx.restore();
    }

    function drawParticles() {
        for (const p of particles) {
            ctx.globalAlpha = Math.max(
                0,
                p.life / p.maxLife
            );

            ctx.fillStyle = p.color;

            ctx.shadowBlur = 8;
            ctx.shadowColor = p.color;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;
    }

    function drawText(text, x, y, size, color, align = "center") {
        ctx.save();

        ctx.font = `bold ${size}px Arial, sans-serif`;
        ctx.textAlign = align;
        ctx.textBaseline = "middle";

        ctx.shadowBlur = 15;
        ctx.shadowColor = color;

        ctx.fillStyle = color;
        ctx.fillText(text, x, y);

        ctx.restore();
    }

    function render() {
        drawBackground();
        drawParticles();

        drawPaddle(left);
        drawPaddle(right);
        drawBall();

        // Title
        drawText(
            "NEON DUEL",
            W / 2,
            48,
            30,
            COLORS.white
        );

        // Scores
        drawText(
            String(score1),
            W / 2 - 100,
            120,
            78,
            COLORS.blue
        );

        drawText(
            String(score2),
            W / 2 + 100,
            120,
            78,
            COLORS.red
        );

        // Labels
        drawText(
            "PLAYER 1",
            100,
            H - 35,
            17,
            COLORS.blue
        );

        drawText(
            "PLAYER 2",
            W - 100,
            H - 35,
            17,
            COLORS.red
        );

        if (!gameOver && countdown > 0) {
            drawText(
                String(countdown),
                W / 2,
                H / 2,
                100,
                COLORS.yellow
            );
        }

        if (!gameOver && countdown === 0 && Math.abs(ball.vx) > 0) {
            // Small GO text at the start of the rally
            if (Math.abs(ball.x - W / 2) < 25) {
                drawText(
                    "GO!",
                    W / 2,
                    H / 2 - 80,
                    35,
                    COLORS.cyan
                );
            }
        }

        if (gameOver) {
            ctx.fillStyle = "rgba(5, 7, 18, 0.75)";
            ctx.fillRect(0, 0, W, H);

            drawText(
                winner,
                W / 2,
                H / 2 - 30,
                45,
                COLORS.yellow
            );

            drawText(
                "Press RESTART GAME to play again",
                W / 2,
                H / 2 + 35,
                22,
                COLORS.white
            );
        }
    }

    function frame(timestamp) {
        if (!lastTime) {
            lastTime = timestamp;
        }

        // Cap delta time to avoid large jumps after a tab switch
        const dt = Math.min((timestamp - lastTime) / 1000, 0.033);
        lastTime = timestamp;

        updatePaddleMovement(dt);
        updatePhysics(dt);
        updateParticles(dt);
        render();

        animationId = requestAnimationFrame(frame);
    }

    // Keyboard controls
    window.addEventListener("keydown", (event) => {
        if (
            ["ArrowUp", "ArrowDown", " "].includes(event.key)
        ) {
            event.preventDefault();
        }

        keys[event.key] = true;
    });

    window.addEventListener("keyup", (event) => {
        keys[event.key] = false;
    });

    window.addEventListener("blur", () => {
        for (const key in keys) {
            keys[key] = false;
        }
    });

    // Restart
    document.getElementById("restart").addEventListener(
        "click",
        () => {
            resetGame();
            canvas.focus();
        }
    );

    // Mobile / touch controls
    function bindButton(id, key) {
        const button = document.getElementById(id);

        button.addEventListener("pointerdown", (event) => {
            event.preventDefault();
            keys[key] = true;
            button.setPointerCapture(event.pointerId);
        });

        function release(event) {
            event.preventDefault();
            keys[key] = false;
        }

        button.addEventListener("pointerup", release);
        button.addEventListener("pointercancel", release);
        button.addEventListener("lostpointercapture", () => {
            keys[key] = false;
        });
    }

    bindButton("p1up", "ArrowUp1");
    bindButton("p1down", "ArrowDown1");
    bindButton("p2up", "ArrowUp");
    bindButton("p2down", "ArrowDown");

    makeStars();
    resetGame();

    if (animationId !== null) {
        cancelAnimationFrame(animationId);
    }

    animationId = requestAnimationFrame(frame);

})();
</script>
</body>
</html>
"""

components.html(
    game_html,
    height=760,
    scrolling=False
)

st.markdown("""
<div style="text-align:center; color:#7185a8; font-size:12px;">
NEON DUEL • Browser Edition • Built with HTML5 Canvas
</div>
""", unsafe_allow_html=True)
