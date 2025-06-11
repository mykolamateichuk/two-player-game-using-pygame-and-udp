from sys import argv
import pygame
import socket

from utils.server import send, receive
from utils.graphics import render_text, draw_player, draw_food
from utils.player import parse_player, parse_coords

if len(argv) >= 2:
    IP = argv[1]
else:
    IP = "127.0.0.1"

# SOCKET DECL
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(300)
sock.connect((IP, 8080))

# PYGAME DECL
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(size=24)

RUNNING = True
DT = 0
FOOD_SIZE = 10

# GAME START
screen.fill("black")

# CONN PROCEDURE
send(sock, "CONN")
PLAYER = parse_player(receive(sock))
PLAYER.size_text = render_text(f"{PLAYER.size}", screen, font)

draw_player(screen, PLAYER)

waiting_text = render_text("Waiting for the other player...", screen, font)
screen.blit(
    waiting_text.text,
    (screen.get_width() / 2 - waiting_text.width / 2,
     screen.get_height() / 2 - 310 - waiting_text.height / 2)
)

pygame.display.flip()

# WAITING FOR THE OPPONENT TO JOIN
OPPONENT = parse_player(receive(sock))
OPPONENT.size_text = render_text(f"{OPPONENT.size}", screen, font)

FOOD = parse_coords(receive(sock))

# GAME TIMER
TIMER = 40
pygame.time.set_timer(pygame.USEREVENT, 1000)

# GAME LOOP
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # SEND EXIT TO CLOSE SERVER
            send(sock, "EXIT")

            # CLOSE SOCKER
            sock.close()

            pygame.quit()
            exit(0)

        if event.type == pygame.USEREVENT:
            TIMER -= 1

    # WIN LOGIC
    if PLAYER.size >= 100 or OPPONENT.size >= 100:
        if PLAYER.size >= 100:
            end_text = render_text("You won!", screen, font)
            screen.fill("green")

        if OPPONENT.size >= 100:
            end_text = render_text("You lost!", screen, font)
            screen.fill("red")

        screen.blit(
            end_text.text,
            (screen.get_width() / 2 - end_text.width / 2,
             screen.get_height() / 2 - end_text.height / 2)
        )

        pygame.display.flip()

        # SEND EXIT TO CLOSE SERVER
        send(sock, "EXIT")

        # CLOSE SOCKER
        sock.close()

        end_game = True
        while end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)


    # TIMEOUT LOGIC
    if TIMER <= 0:
        end_text = render_text("Tie!", screen, font)

        screen.fill("black")
        screen.blit(
            end_text.text,
            (screen.get_width() / 2 - end_text.width / 2,
             screen.get_height() / 2 - end_text.height / 2)
        )

        pygame.display.flip()

        # SEND EXIT TO CLOSE SERVER
        send(sock, "EXIT")

        # CLOSE SOCKER
        sock.close()

        end_game = True
        while end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)


    screen.fill("black")

    # DRAW ENTITIES
    draw_player(screen, OPPONENT)
    draw_food(screen, FOOD, FOOD_SIZE)
    draw_player(screen, PLAYER, main=True) # player on top of everything

    # DRAW TEXT
    timer_text = render_text(f"TIME LEFT: {TIMER}", screen, font)
    screen.blit(
        timer_text.text,
        (screen.get_width() / 2 - timer_text.width / 2,
         screen.get_height() / 2 - 310 - timer_text.height / 2)
    )

    # UPDATES
    pygame.display.flip()
    DT = clock.tick(60) / 1000

    # CONTROLS
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        if PLAYER.coords.y - PLAYER.size <= screen.get_height() / 2 - 360:
            PLAYER.coords.y -= 0 * DT
        else:
            PLAYER.coords.y -= 300 * DT
    if keys[pygame.K_s]:
        if PLAYER.coords.y + PLAYER.size >= screen.get_height() / 2 + 360:
            PLAYER.coords.y += 0 * DT
        else:
            PLAYER.coords.y += 300 * DT
    if keys[pygame.K_a]:
        if PLAYER.coords.x - PLAYER.size <= screen.get_width() / 2 - 640:
            PLAYER.coords.x -= 0 * DT
        else:
            PLAYER.coords.x -= 300 * DT
    if keys[pygame.K_d]:
        if PLAYER.coords.x + PLAYER.size >= screen.get_width() / 2 + 640:
            PLAYER.coords.x += 0 * DT
        else:
            PLAYER.coords.x += 300 * DT
    if keys[pygame.K_ESCAPE]:
        RUNNING = False

    # COMMUNICATE WITH SERVER
    send(sock, f"COORDS {PLAYER.coords.x} {PLAYER.coords.y}")

    FOOD = parse_coords(receive(sock))

    PLAYER = parse_player(receive(sock))
    PLAYER.size_text = render_text(f"{PLAYER.size}", screen, font)

    OPPONENT = parse_player(receive(sock))
    OPPONENT.size_text = render_text(f"{OPPONENT.size}", screen, font)
