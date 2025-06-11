import pygame
from dataclasses import dataclass

from utils.types import Player, Text


def render_text(text: str, screen: pygame.Surface, font: pygame.font.Font) -> Text:
    rendered_font = font.render(text, True, "white")
    w, h = font.size(text)
    return Text(
        text=rendered_font,
        width=w,
        height=h
    )


def draw_player(
        screen: pygame.Surface,
        player: Player,
        main: bool = False
) -> None:
    pygame.draw.circle(
        screen,
        player.color,
        player.coords,
        player.size
    )

    screen.blit(
        player.size_text.text,
        (player.coords.x - player.size_text.width / 2,
         player.coords.y - player.size_text.height / 2)
    )


def draw_food(screen: pygame.Surface, coords: pygame.Vector2, size: int) -> None:
    pygame.draw.circle(screen, "white", coords, size)


def check_collision(player: Player, food: pygame.Vector2, food_size: int) -> bool:
    if (player.coords.x - player.size - food_size <= food.x <= player.coords.x + player.size + food_size
            and player.coords.y - player.size - food_size <= food.y <= player.coords.y + player.size + food_size):
        return True

    return False
