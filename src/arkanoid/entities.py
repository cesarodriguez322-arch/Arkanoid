import pygame
import random
from .constants import WHITE, BLUE, PURPLE, RED, GREEN


# --- Pelota ---
class Pelota:
    def __init__(self, surface: pygame.Surface, raqueta):
        self.surface = surface
        self.raqueta = raqueta
        self.moviendo = False
        self.reset()

    def reset(self):
        self.x = self.raqueta.x + self.raqueta.tamano / 2 - 5
        self.y = self.raqueta.y - 10
        self.vx = random.choice([-5, -4, 4, 5])
        self.vy = -5
        self.moviendo = False

    def dibujar(self):
        pygame.draw.circle(
            self.surface, WHITE,
            (int(self.x + 5), int(self.y + 5)), 5
        )

    def mover(self):
        if self.moviendo:
            self.x += self.vx
            self.y += self.vy


# --- Raqueta ---
class Raqueta:
    def __init__(self, surface: pygame.Surface, w: int, h: int):
        self.surface = surface
        self.w = w
        self.h = h
        self.tamano = 80
        self.x = w / 2 - self.tamano / 2
        self.y = h - 20
        self.centro = self.x + self.tamano / 2
        self.izq = False
        self.der = False

    def dibujar(self):
        pygame.draw.rect(
            self.surface, WHITE,
            (self.x, self.y, self.tamano, 10)
        )

    def mover(self):
        if self.izq: self.x -= 10
        if self.der: self.x += 10
        if self.x < 0: self.x = 0
        if self.x + self.tamano > self.w: self.x = self.w - self.tamano
        self.centro = self.x + self.tamano / 2


# --- Bloques ---
class Bloques:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.tablero = [
            [4] * 10,
            [3] * 10,
            [2] * 10,
            [1] * 10,
            [2] * 10,
            [3] * 10,
        ]

    def dibujar(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] != 0:
                    color = [BLUE, PURPLE, RED, GREEN][self.tablero[i][j] - 1]
                    pygame.draw.rect(
                        self.surface, color,
                        (j * 60, i * 10 + 35, 59, 9)
                    )

    def todos_destruidos(self) -> bool:
        return not any(
            self.tablero[i][j] != 0
            for i in range(len(self.tablero))
            for j in range(len(self.tablero[i]))
        )
