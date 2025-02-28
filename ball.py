import pygame
import math
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99
HEX_SIZE = 200
BALL_RADIUS = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Rotating Hexagon @litcezixs")
clock = pygame.time.Clock()

ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [5, 0]
angle = 0
rotation_speed = 1

def draw_hexagon(surface, color, center, size, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + size * math.cos(theta)
        y = center[1] + size * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def check_collision(ball_pos, ball_vel, hex_center, hex_size):
    for i in range(6):
        theta1 = math.radians(i * 60)
        theta2 = math.radians((i + 1) * 60)
        x1 = hex_center[0] + hex_size * math.cos(theta1)
        y1 = hex_center[1] + hex_size * math.sin(theta1)
        x2 = hex_center[0] + hex_size * math.cos(theta2)
        y2 = hex_center[1] + hex_size * math.sin(theta2)

        A = y2 - y1
        B = x1 - x2
        C = x2 * y1 - x1 * y2

        distance = abs(A * ball_pos[0] + B * ball_pos[1] + C) / math.sqrt(A**2 + B**2)

        if distance < BALL_RADIUS:
            normal = pygame.math.Vector2(A, B).normalize()
            ball_vel[0] -= 2 * (ball_vel[0] * normal.x + ball_vel[1] * normal.y) * normal.x
            ball_vel[1] -= 2 * (ball_vel[0] * normal.x + ball_vel[1] * normal.y) * normal.y
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            return True
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_vel[1] += GRAVITY
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    ball_vel[0] *= FRICTION
    ball_vel[1] *= FRICTION

    angle += rotation_speed

    hex_center = (WIDTH // 2, HEIGHT // 2)
    if not check_collision(ball_pos, ball_vel, hex_center, HEX_SIZE):
        if (ball_pos[0] < 0 or ball_pos[0] > WIDTH or
                ball_pos[1] < 0 or ball_pos[1] > HEIGHT):
            ball_pos = [WIDTH // 2, HEIGHT // 2]

    screen.fill((0, 0, 0))
    draw_hexagon(screen, (255, 255, 255), hex_center, HEX_SIZE, angle)
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    pygame.display.flip()
    clock.tick(FPS)
