from pathlib import Path
import pygame

# --- Rutas de assets (relativas al archivo, portables) ---
# SDK requiere rutas relativas; calculamos desde la ubicacion de este archivo
GAME_DIR  = Path(__file__).resolve().parent.parent.parent  # .../Arkanoid/
SOUND_DIR = GAME_DIR / "sound"
IMAGE_DIR = GAME_DIR / "imagen"


# --- Sonidos ---
def _load_sounds():
    pygame.mixer.set_num_channels(8)

    canales = {
        "bloque":      pygame.mixer.Channel(0),
        "perder_vida": pygame.mixer.Channel(1),
        "game_over":   pygame.mixer.Channel(2),
        "victoria":    pygame.mixer.Channel(3),
    }

    sonidos = {
        "victoria":    pygame.mixer.Sound(str(SOUND_DIR / "sonido-de-victoria.wav")),
        "bloque":      pygame.mixer.Sound(str(SOUND_DIR / "_-Sonido-de-Golpe-_-Efecto-de-Sonido-HD-__MP3_160K_.wav")),
        "perder_vida": pygame.mixer.Sound(str(SOUND_DIR / "Sonido-de-daño-Minecraft_1.wav")),
        "game_over":   pygame.mixer.Sound(str(SOUND_DIR / "Game-Over-sound-effect.wav")),
    }

    sonidos["victoria"].set_volume(0.7)
    sonidos["bloque"].set_volume(0.5)
    sonidos["perder_vida"].set_volume(0.7)
    sonidos["game_over"].set_volume(0.7)

    return canales, sonidos


# --- Fondos ---
def _load_images(w: int, h: int):
    def pixelate(path: Path) -> pygame.Surface:
        img   = pygame.image.load(str(path))
        small = pygame.transform.scale(img, (150, 100))
        return pygame.transform.scale(small, (w, h)).convert()

    return {
        "fondo_juego":  pixelate(IMAGE_DIR / "istockphoto-902929330-612x612.jpg"),
        "fondo_menu":   pixelate(IMAGE_DIR / "c68dc25a5fefae8f70c5a278664e4850.jpg"),
        "fondo_ganar":  pixelate(IMAGE_DIR / "44df237ddf0fa26582897dabb7ca5335.jpg"),
        "fondo_perder": pixelate(IMAGE_DIR / "c68dc25a5fefae8f70c5a278664e4850.jpg"),
        "logo":         pygame.image.load(str(IMAGE_DIR / "images.png")).convert_alpha(),
    }


# --- Musica ---
def musica_menu():
    pygame.mixer.music.load(str(SOUND_DIR / "Arkanoid NES - Title Screen Music.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def musica_juego():
    pygame.mixer.music.load(str(SOUND_DIR / "Sonic The Hedgehog OST - Green Hill Zone(MP3_160K).mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def sonido_ganar(canales, sonidos):
    canales["victoria"].play(sonidos["victoria"])
    pygame.time.delay(int(sonidos["victoria"].get_length() * 1000))


# --- Carga perezosa (llamar despues de pygame.init()) ---
_canales = None
_sonidos = None
_images  = None

def load_all(w: int, h: int):
    global _canales, _sonidos, _images
    _canales, _sonidos = _load_sounds()
    _images = _load_images(w, h)

def get_canales(): return _canales
def get_sonidos(): return _sonidos
def get_images():  return _images
