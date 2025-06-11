import pygame

from dataclasses import dataclass


@dataclass
class Text:
    text: pygame.Surface
    width: int
    height: int


@dataclass
class Player:
    coords: pygame.Vector2
    size: int
    color: pygame.Color
    size_text: Text | None
