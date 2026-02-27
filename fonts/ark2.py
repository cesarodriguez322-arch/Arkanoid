import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

# --- Canales de sonido ---
canal_bloque = pygame.mixer.Channel(0)
canal_perder_vida = pygame.mixer.Channel(1)
canal_game_over = pygame.mixer.Channel(2)
canal_victoria = pygame.mixer.Channel(3)

# --- Sonidos ---
sonido_victoria = pygame.mixer.Sound("sound/sonido-de-victoria.wav")
sonido_victoria.set_volume(0.7)
sonido_bloque = pygame.mixer.Sound("sound/_-Sonido-de-Golpe-_-Efecto-de-Sonido-HD-__MP3_160K_.wav")
sonido_bloque.set_volume(0.5)
sonido_perder_vida = pygame.mixer.Sound("sound/Sonido-de-daño-Minecraft_1.wav")
sonido_perder_vida.set_volume(0.7)
sonido_game_over = pygame.mixer.Sound("sound/Game-Over-sound-effect.wav")
sonido_game_over.set_volume(0.7)

# --- Colores ---
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- Pantalla ---
ventana = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Arkanoid Pixel")
font = pygame.font.SysFont("Courier New", 30)
font_grande = pygame.font.SysFont("Courier New", 60)
clock = pygame.time.Clock()

def texto_arcade(texto, fuente, color_texto, color_borde, centro):
    render_texto = fuente.render(texto, True, color_texto)
    render_borde = fuente.render(texto, True, color_borde)

    rect = render_texto.get_rect(center=centro)

    # Dibujar borde
    for dx in [-3, -2, -1, 1, 2, 3]:
        for dy in [-3, -2, -1, 1, 2, 3]:
            ventana.blit(render_borde, rect.move(dx, dy))

    # Dibujar texto principal
    ventana.blit(render_texto, rect)

# --- Música ---
def musica_menu():
    pygame.mixer.music.load("sound/Arkanoid NES - Title Screen Music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def musica_juego():
    pygame.mixer.music.load("sound/Sonic The Hedgehog OST - Green Hill Zone(MP3_160K).mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def sonido_ganar():
    canal_victoria.play(sonido_victoria)
    pygame.time.delay(int(sonido_victoria.get_length() * 1000))

# --- Fondos ---
fondo_img = pygame.image.load("imagen/istockphoto-902929330-612x612.jpg")
fondo_pixelado = pygame.transform.scale(fondo_img, (150, 100))
fondo_pixelado = pygame.transform.scale(fondo_pixelado, (600, 400)).convert()

fondo_menu_img = pygame.image.load("imagen/c68dc25a5fefae8f70c5a278664e4850.jpg")
fondo_menu = pygame.transform.scale(fondo_menu_img, (150, 100))
fondo_menu = pygame.transform.scale(fondo_menu, (600, 400)).convert()

fondo_ganar_img = pygame.image.load("imagen/44df237ddf0fa26582897dabb7ca5335.jpg")
fondo_ganar = pygame.transform.scale(fondo_ganar_img, (150, 100))
fondo_ganar = pygame.transform.scale(fondo_ganar, (600, 400)).convert()

fondo_perder_img = pygame.image.load("imagen/c68dc25a5fefae8f70c5a278664e4850.jpg")
fondo_perder = pygame.transform.scale(fondo_perder_img, (150, 100))
fondo_perder = pygame.transform.scale(fondo_perder, (600, 400)).convert()

logo_img = pygame.image.load("imagen/images.png").convert_alpha()

# --- Clases ---
class Pelota:
    def __init__(self, ventana, raqueta):
        self.ventana = ventana
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
        pygame.draw.circle(self.ventana, WHITE, (int(self.x + 5), int(self.y + 5)), 5)

    def mover(self):
        if self.moviendo:
            self.x += self.vx
            self.y += self.vy

class Raqueta:
    def __init__(self, ventana):
        self.tamano = 80
        self.x = 600 / 2 - self.tamano / 2
        self.y = 380
        self.centro = self.x + self.tamano / 2
        self.ventana = ventana
        self.izq = False
        self.der = False

    def dibujar(self):
        pygame.draw.rect(self.ventana, WHITE, (self.x, self.y, self.tamano, 10))

    def mover(self):
        if self.izq: self.x -= 10
        if self.der: self.x += 10
        if self.x < 0: self.x = 0
        if self.x + self.tamano > 600: self.x = 600 - self.tamano
        self.centro = self.x + self.tamano / 2

class Bloques:
    def __init__(self, ventana):
        self.ventana = ventana
        self.tablero = [[4]*10, [3]*10, [2]*10, [1]*10, [2]*10, [3]*10]

    def dibujar(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] != 0:
                    color = [BLUE, PURPLE, RED, GREEN][self.tablero[i][j]-1]
                    pygame.draw.rect(self.ventana, color, (j*60, i*10+35, 59, 9))

# --- Variables ---
vidas = 3
estado = "menu"
r1 = Raqueta(ventana)
bola = Pelota(ventana, r1)
tablero = Bloques(ventana)
estado_actual = None
jugar = True

# --- Bucle principal ---
while jugar:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugar = False

    if estado == "final_ganar":
       texto_arcade("GANASTE", font_grande, GREEN, BLACK, (300,150))

    elif estado == "final_perder":
       texto_arcade("PERDISTE", font_grande, RED, BLACK, (300,150))

    pygame.display.update()
    clock.tick(60)

pygame.quit()