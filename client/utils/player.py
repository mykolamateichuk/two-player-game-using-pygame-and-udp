import pygame

from utils.types import Player


def parse_coords(coords: str) -> pygame.Vector2:
    return pygame.Vector2(float(coords.split()[0]), float(coords.split()[1]))

def parse_player(player: str) -> Player:
    tokens = player.split()

    return Player(
        coords=pygame.Vector2(float(tokens[0]), float(tokens[1])),
        size=int(tokens[2]),
        color=pygame.Color(int(tokens[3]), int(tokens[4]), int(tokens[5])),
        size_text=None
    )
