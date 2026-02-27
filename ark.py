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
font_grande = pygame.font.SysFont("Courier New", 50)
clock = pygame.time.Clock()

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
fondo_img = pygame.image.load("imagen/drlobo-1986-arkanoid.jpg")
fondo_pixelado = pygame.transform.scale(fondo_img, (150, 100))
fondo_pixelado = pygame.transform.scale(fondo_pixelado, (600, 400))
fondo_pixelado = fondo_pixelado.convert()

fondo_menu_img = pygame.image.load("imagen/c68dc25a5fefae8f70c5a278664e4850.jpg")
fondo_menu = pygame.transform.scale(fondo_menu_img, (150, 100))
fondo_menu = pygame.transform.scale(fondo_menu, (600, 400))
fondo_menu = fondo_menu.convert()

fondo_ganar_img = pygame.image.load("imagen/44df237ddf0fa26582897dabb7ca5335.jpg")
fondo_ganar = pygame.transform.scale(fondo_ganar_img, (150, 100))
fondo_ganar = pygame.transform.scale(fondo_ganar, (600, 400))
fondo_ganar = fondo_ganar.convert()

fondo_perder_img = pygame.image.load("imagen/c68dc25a5fefae8f70c5a278664e4850.jpg")
fondo_perder = pygame.transform.scale(fondo_perder_img, (150, 100))
fondo_perder = pygame.transform.scale(fondo_perder, (600, 400))
fondo_perder = fondo_perder.convert()

# --- Logos opcionales ---
logo_ganar_img = pygame.image.load("imagen/images (1).jpg").convert_alpha()
logo_ganar_img = pygame.transform.scale(logo_ganar_img, (100,100))

logo_perder_img = pygame.image.load("imagen/images (2).jpg").convert_alpha()
logo_perder_img = pygame.transform.scale(logo_perder_img, (100,100))

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
        self.tablero = [
            [4]*10, [3]*10, [2]*10, [1]*10, [2]*10, [3]*10
        ]
    def dibujar(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j]!=0:
                    color = [BLUE, PURPLE, RED, GREEN][self.tablero[i][j]-1]
                    pygame.draw.rect(self.ventana, color, (j*60, i*10+35, 59, 9))

# --- Botón con hover ---
click_ya_detectado = False
def dibujar_boton(texto, x, y, ancho, alto, color_normal, color_hover, accion=None):
    global click_ya_detectado
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = color_normal
    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        color = color_hover
        if click[0] == 1 and not click_ya_detectado and accion is not None:
            click_ya_detectado = True
            accion()
    if click[0] == 0:
        click_ya_detectado = False
    pygame.draw.rect(ventana, color, (x, y, ancho, alto))
    texto_render = font.render(texto, True, WHITE)
    ventana.blit(texto_render, texto_render.get_rect(center=(x + ancho/2, y + alto/2)))

# --- Funciones ---
def reiniciar_juego():
    global bola, r1, tablero, golpes, vidas, estado, estado_actual
    golpes = 0
    vidas = 3
    r1.x = 600/2 - r1.tamano/2
    r1.izq = False
    r1.der = False
    bola.reset()
    tablero = Bloques(ventana)
    estado = "jugando"
    estado_actual = None  # Forzar que música del juego se reinicie

def salir_accion():
    pygame.quit()
    exit()

def colisiones():
    global golpes
    bloques_golpeados = 0
    for i in range(len(tablero.tablero)):
        for j in range(len(tablero.tablero[i])):
            if tablero.tablero[i][j]!=0:
                if ((j*60 < bola.x < j*60+59) or (j*60 < bola.x+10 < j*60+59)) and \
                   ((i*10+35 < bola.y < i*10+44) or (i*10+35 < bola.y+10 < i*10+44)):
                    tablero.tablero[i][j]=0
                    bloques_golpeados+=1
                    golpes+=1
    if bloques_golpeados>0:
        bola.vy*=-1
        canal_bloque.play(sonido_bloque)
        incremento = 0.3*bloques_golpeados
        bola.vx*=(1+incremento/5)
        bola.vy*=(1+incremento/5)
        bola.vx = max(-10, min(10, bola.vx))
        bola.vy = max(-10, min(10, bola.vy))

def refrescar():
    ventana.blit(fondo_pixelado, (0,0))
    bola.dibujar()
    r1.dibujar()
    tablero.dibujar()
    ancho_total = vidas*30
    inicio_x = 300 - ancho_total/2
    for i in range(vidas):
        x = inicio_x + i*30
        pygame.draw.circle(ventana, RED, (int(x), 15), 8)
        pygame.draw.circle(ventana, RED, (int(x+10), 15), 8)
        pygame.draw.polygon(ventana, RED, [(int(x-8),18),(int(x+18),18),(int(x+5),32)])

# --- Variables ---
vidas = 3
golpes = 0
estado = "menu"
r1 = Raqueta(ventana)
bola = Pelota(ventana,r1)
tablero = Bloques(ventana)
estado_actual = None
jugar = True

# --- Bucle principal ---
while jugar:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            jugar=False
        if estado=="jugando":
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT: r1.izq=True
                if event.key==pygame.K_RIGHT: r1.der=True
                if not bola.moviendo and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    bola.moviendo=True
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT: r1.izq=False
                if event.key==pygame.K_RIGHT: r1.der=False

    # --- Música ---
    if estado=="menu" and estado_actual!="menu":
        musica_menu()
        estado_actual="menu"
    elif estado=="jugando" and estado_actual!="jugando":
        musica_juego()
        estado_actual="jugando"

    # --- Lógica juego ---
    if estado=="jugando":
        r1.mover()
        if not bola.moviendo:
            bola.x = r1.x + r1.tamano/2 - 5
            bola.y = r1.y - 10
        else:
            bola.mover()

        colisiones()

        if bola.x>=590 or bola.x<=0:
            bola.vx*=-1
            bola.x=min(max(bola.x,0),590)
        if bola.y<=0:
            bola.vy*=-1
            bola.y=0
        if bola.y+10>r1.y:
            if r1.x<bola.x<r1.x+r1.tamano:
                porcentaje = (bola.x - r1.centro)/(r1.tamano/2)
                bola.vx+=porcentaje*3
                bola.vx=max(-7,min(7,bola.vx))
                bola.vy*=-1
                bola.y=r1.y-10
            else:
                if bola.y>400:
                    vidas-=1
                    canal_perder_vida.play(sonido_perder_vida)
                    bola.reset()
                    pygame.time.delay(500)
                    bola.moviendo=True if vidas>0 else False
                    if vidas==0:
                        pygame.mixer.music.stop()
                        canal_game_over.play(sonido_game_over)
                        pygame.time.delay(int(sonido_game_over.get_length()*1000))
                        estado="final_perder"

        # Victoria
        if not any(tablero.tablero[i][j]!=0 for i in range(len(tablero.tablero)) for j in range(len(tablero.tablero[i]))):
            pygame.mixer.music.stop()
            sonido_ganar()
            estado="final_ganar"

        refrescar()

    # --- Menú principal ---
    elif estado=="menu":
        ventana.blit(fondo_menu, (0,0))
        ventana.blit(logo_img, logo_img.get_rect(center=(300,100)))
        dibujar_boton("JUGAR", 225, 180, 150, 50, (50,50,50), (100,100,100), reiniciar_juego)
        dibujar_boton("SALIR", 225, 260, 150, 50, (50,50,50), (100,100,100), salir_accion)

    # --- Pantalla GANASTE ---
    elif estado=="final_ganar":
        ventana.blit(fondo_ganar, (0,0))
        ventana.blit(logo_ganar_img, logo_ganar_img.get_rect(center=(300,100)))
        mensaje = font_grande.render("GANASTE", True, RED)
        ventana.blit(mensaje, mensaje.get_rect(center=(300,150)))
        dibujar_boton("REINICIAR", 200, 250, 200, 50, (50,50,50), (100,100,100), reiniciar_juego)
        dibujar_boton("SALIR", 225, 320, 150, 40, (50,50,50), (100,100,100), salir_accion)

    # --- Pantalla PERDISTE ---
    elif estado=="final_perder":
        ventana.blit(fondo_perder, (0,0))
        ventana.blit(logo_perder_img, logo_perder_img.get_rect(center=(300,100)))
        mensaje = font_grande.render("PERDISTE", True, RED)
        ventana.blit(mensaje, mensaje.get_rect(center=(300,150)))
        dibujar_boton("REINICIAR", 200, 250, 200, 50, (50,50,50), (100,100,100), reiniciar_juego)
        dibujar_boton("SALIR", 225, 320, 150, 40, (50,50,50), (100,100,100), salir_accion)

    pygame.display.update()
    clock.tick(60)

pygame.quit()