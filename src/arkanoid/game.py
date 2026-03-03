import pygame
from arcade_machine_sdk import GameBase, GameMeta

from .constants import GAME_WIDTH, GAME_HEIGHT, WHITE, GREEN, RED
from .entities import Pelota, Raqueta, Bloques
from .logic import colisiones, dibujar_boton, dibujar_vidas
from . import assets


class ArkanoidGame(GameBase):

    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)
        self._estado = "menu"
        self._estado_actual = None

        # Canvas interno 600x400 — toda la logica corre en esta resolucion
        self._canvas = None

        # Geometria del canvas escalado en la ventana del SDK (1024x768)
        self._scaled_w = GAME_WIDTH
        self._scaled_h = GAME_HEIGHT
        self._scaled_rect = None

        self._r1      = None
        self._bola    = None
        self._tablero = None

        self._vidas  = 3
        self._golpes = 0

        self._font       = None
        self._font_grande = None

    # --- Ciclo de vida ---
    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)

        assets.load_all(GAME_WIDTH, GAME_HEIGHT)

        self._font       = pygame.font.SysFont("Courier New", 30)
        self._font_grande = pygame.font.SysFont("Courier New", 50)

        # Calcular el mayor tamaño 3:2 que cabe en la ventana del SDK
        sw, sh = surface.get_size()
        ratio = GAME_WIDTH / GAME_HEIGHT  # 1.5
        if sw / sh >= ratio:
            self._scaled_h = sh
            self._scaled_w = int(sh * ratio)
        else:
            self._scaled_w = sw
            self._scaled_h = int(sw / ratio)

        offset_x = (sw - self._scaled_w) // 2
        offset_y = (sh - self._scaled_h) // 2
        self._scaled_rect = pygame.Rect(offset_x, offset_y, self._scaled_w, self._scaled_h)

        self._canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

        self._inicializar_entidades()
        self._estado = "menu"
        self._estado_actual = None

    def stop(self) -> None:
        pygame.mixer.music.stop()
        super().stop()

    # --- Eventos (SDK: no usar pygame.event.get()) ---
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if self._estado == "jugando":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  self._r1.izq = True
                    if event.key == pygame.K_RIGHT: self._r1.der = True
                    if not self._bola.moviendo and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self._bola.moviendo = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:  self._r1.izq = False
                    if event.key == pygame.K_RIGHT: self._r1.der = False

    # --- Logica por frame ---
    def update(self, dt: float) -> None:
        canales = assets.get_canales()
        sonidos = assets.get_sonidos()

        # --- Musica ---
        if self._estado == "menu" and self._estado_actual != "menu":
            assets.musica_menu()
            self._estado_actual = "menu"
        elif self._estado == "jugando" and self._estado_actual != "jugando":
            assets.musica_juego()
            self._estado_actual = "jugando"

        if self._estado != "jugando":
            return

        # --- Logica juego ---
        self._r1.mover()
        if not self._bola.moviendo:
            self._bola.x = self._r1.x + self._r1.tamano / 2 - 5
            self._bola.y = self._r1.y - 10
        else:
            self._bola.mover()

        colisiones(self._bola, self._tablero, canales, sonidos)

        if self._bola.x >= GAME_WIDTH - 10 or self._bola.x <= 0:
            self._bola.vx *= -1
            self._bola.x = min(max(self._bola.x, 0), GAME_WIDTH - 10)
        if self._bola.y <= 0:
            self._bola.vy *= -1
            self._bola.y = 0

        if self._bola.y + 10 > self._r1.y:
            if self._r1.x < self._bola.x < self._r1.x + self._r1.tamano:
                porcentaje = (self._bola.x - self._r1.centro) / (self._r1.tamano / 2)
                self._bola.vx += porcentaje * 3
                self._bola.vx = max(-7, min(7, self._bola.vx))
                self._bola.vy *= -1
                self._bola.y = self._r1.y - 10
            else:
                if self._bola.y > GAME_HEIGHT:
                    self._vidas -= 1
                    canales["perder_vida"].play(sonidos["perder_vida"])
                    self._bola.reset()
                    pygame.time.delay(500)
                    self._bola.moviendo = self._vidas > 0
                    if self._vidas == 0:
                        pygame.mixer.music.stop()
                        canales["game_over"].play(sonidos["game_over"])
                        pygame.time.delay(int(sonidos["game_over"].get_length() * 1000))
                        self._estado = "final_perder"

        # Victoria
        if self._tablero.todos_destruidos():
            pygame.mixer.music.stop()
            assets.sonido_ganar(canales, sonidos)
            self._estado = "final_ganar"

    # --- Renderizado (SDK: no usar pygame.display.flip()) ---
    def render(self) -> None:
        images  = assets.get_images()
        canvas  = self._canvas
        screen  = self.surface

        # Convertir mouse a espacio logico 600x400
        raw_mouse     = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ox, oy = self._scaled_rect.topleft
        sx = GAME_WIDTH  / self._scaled_w
        sy = GAME_HEIGHT / self._scaled_h
        mouse_rel = ((raw_mouse[0] - ox) * sx, (raw_mouse[1] - oy) * sy)

        if self._estado == "jugando":
            canvas.blit(images["fondo_juego"], (0, 0))
            self._bola.dibujar()
            self._r1.dibujar()
            self._tablero.dibujar()
            dibujar_vidas(canvas, self._vidas, GAME_WIDTH)

        elif self._estado == "menu":
            canvas.blit(images["fondo_menu"], (0, 0))
            logo = images["logo"]
            canvas.blit(logo, logo.get_rect(center=(GAME_WIDTH // 2, 100)))
            dibujar_boton(canvas, self._font, "JUGAR",
                          225, 180, 150, 50, (50,50,50), (100,100,100),
                          self._reiniciar_juego, mouse_rel, mouse_pressed)
            dibujar_boton(canvas, self._font, "SALIR",
                          225, 260, 150, 50, (50,50,50), (100,100,100),
                          self.stop, mouse_rel, mouse_pressed)

        elif self._estado == "final_ganar":
            canvas.blit(images["fondo_ganar"], (0, 0))
            msg = self._font_grande.render("GANASTE", True, GREEN)
            canvas.blit(msg, msg.get_rect(center=(GAME_WIDTH // 2, 150)))
            dibujar_boton(canvas, self._font, "REINICIAR",
                          200, 250, 200, 50, (50,50,50), (100,100,100),
                          self._reiniciar_juego, mouse_rel, mouse_pressed)
            dibujar_boton(canvas, self._font, "SALIR",
                          225, 320, 150, 40, (50,50,50), (100,100,100),
                          self.stop, mouse_rel, mouse_pressed)

        elif self._estado == "final_perder":
            canvas.blit(images["fondo_perder"], (0, 0))
            msg = self._font_grande.render("PERDISTE", True, RED)
            canvas.blit(msg, msg.get_rect(center=(GAME_WIDTH // 2, 150)))
            dibujar_boton(canvas, self._font, "REINICIAR",
                          200, 250, 200, 50, (50,50,50), (100,100,100),
                          self._reiniciar_juego, mouse_rel, mouse_pressed)
            dibujar_boton(canvas, self._font, "SALIR",
                          225, 320, 150, 40, (50,50,50), (100,100,100),
                          self.stop, mouse_rel, mouse_pressed)

        # Escalar canvas 600x400 al tamaño calculado y centrar en pantalla
        screen.fill((0, 0, 0))
        scaled = pygame.transform.scale(canvas, (self._scaled_w, self._scaled_h))
        screen.blit(scaled, self._scaled_rect.topleft)

    # --- Helpers ---
    def _inicializar_entidades(self):
        self._r1      = Raqueta(self._canvas, GAME_WIDTH, GAME_HEIGHT)
        self._bola    = Pelota(self._canvas, self._r1)
        self._tablero = Bloques(self._canvas)
        self._vidas   = 3
        self._golpes  = 0

    def _reiniciar_juego(self):
        self._inicializar_entidades()
        self._estado        = "jugando"
        self._estado_actual = None  # Forzar que musica del juego se reinicie
