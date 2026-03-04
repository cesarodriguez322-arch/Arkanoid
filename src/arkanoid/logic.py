import pygame
from src.arkanoid.constants import WHITE, RED


# --- Colisiones ---
def colisiones(bola, tablero, canales, sonidos):
    bloques_golpeados = 0

    for i in range(len(tablero.tablero)):
        for j in range(len(tablero.tablero[i])):
            if tablero.tablero[i][j] != 0:
                bx0, bx1 = j * 60, j * 60 + 59
                by0, by1 = i * 10 + 35, i * 10 + 44
                if (
                    (bx0 < bola.x < bx1 or bx0 < bola.x + 10 < bx1) and
                    (by0 < bola.y < by1 or by0 < bola.y + 10 < by1)
                ):
                    tablero.tablero[i][j] = 0
                    bloques_golpeados += 1

    if bloques_golpeados > 0:
        bola.vy *= -1
        canales["bloque"].play(sonidos["bloque"])
        incremento = 0.3 * bloques_golpeados
        bola.vx *= (1 + incremento / 5)
        bola.vy *= (1 + incremento / 5)
        bola.vx = max(-10, min(10, bola.vx))
        bola.vy = max(-10, min(10, bola.vy))


# --- Boton con hover seguro ---
# mouse_pos y mouse_pressed se reciben ya ajustados al espacio del canvas interno
click_ya_detectado = False

def dibujar_boton(
    surface, font, texto,
    x, y, ancho, alto,
    color_normal, color_hover,
    accion=None,
    mouse_pos=None,
    mouse_pressed=None,
):
    global click_ya_detectado

    if mouse_pos    is None: mouse_pos    = pygame.mouse.get_pos()
    if mouse_pressed is None: mouse_pressed = pygame.mouse.get_pressed()

    color = color_normal
    if x < mouse_pos[0] < x + ancho and y < mouse_pos[1] < y + alto:
        color = color_hover
        if mouse_pressed[0] == 1 and not click_ya_detectado and accion is not None:
            click_ya_detectado = True
            accion()
    if mouse_pressed[0] == 0:
        click_ya_detectado = False

    pygame.draw.rect(surface, color, (x, y, ancho, alto))
    texto_render = font.render(texto, True, WHITE)
    surface.blit(texto_render, texto_render.get_rect(center=(x + ancho / 2, y + alto / 2)))


# --- HUD vidas ---
def dibujar_vidas(surface, vidas, w):
    ancho_total = vidas * 30
    inicio_x = w / 2 - ancho_total / 2
    for i in range(vidas):
        x = inicio_x + i * 30
        pygame.draw.circle(surface, RED, (int(x),      15), 8)
        pygame.draw.circle(surface, RED, (int(x + 10), 15), 8)
        pygame.draw.polygon(surface, RED, [
            (int(x - 8),  18),
            (int(x + 18), 18),
            (int(x + 5),  32),
        ])
