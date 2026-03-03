"""
main.py — Punto de entrada del juego Arkanoid integrado con el Arcade Machine SDK.

Ejecutar de forma independiente:
    python main.py

El juego corre en modo standalone usando run_independently() del SDK,
que crea la ventana (1024x768) y el loop principal,
llamando a handle_events, update y render por frame.
"""
import pygame
from arcade_machine_sdk import GameBase, GameMeta
from src.arkanoid.game import ArkanoidGame

if not pygame.get_init():
    pygame.init()

metadata = (
    GameMeta()
    .with_title("Arkanoid")
    .with_description("Juego de romper bloques inspirado en el Arkanoid clásico de NES")
    .with_release_date("2026")
    .with_group_number(5)
    .add_tag("Arcade")
    .add_tag("Bloques")
    .add_author(["César Rodríguez","Rovel Pérez"])
)

game = ArkanoidGame(metadata)

if __name__ == "__main__":
    game.run_independently()
