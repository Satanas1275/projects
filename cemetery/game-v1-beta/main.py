import pygame
import os
from PIL import Image

pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mon Jeu")
clock = pygame.time.Clock()

# Joueur
player_pos = pygame.Vector2(screen_width // 2, screen_height - 120)
player_vel = pygame.Vector2(0, 0)
facing_left = False
on_ground = True
gravity = 0.5
jump_force = -12

# Mouvements
moving = False
is_attacking = False

# FPS et animation
frame_index = 0
animation_timer = 0
frame_duration = 100  # ms

# Chargement du fond et redimensionnement
bg = pygame.image.load("assets/bg.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))  # ← IMPORTANT

# Fonction pour charger une anim GIF
def load_gif(path):
    frames = []
    if not os.path.exists(path):
        print(f"[ERREUR] GIF manquant: {path}")
        return frames
    pil_image = Image.open(path)
    try:
        while True:
            frame = pil_image.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            ).convert_alpha()
            frames.append(pygame_image)
            pil_image.seek(pil_image.tell() + 1)
    except EOFError:
        pass
    return frames

# Charger animations
idle_frames = load_gif("assets/idle.gif")
run_frames = load_gif("assets/run.gif")
attack_frames = load_gif("assets/atak.gif")

# Liste par défaut
current_frames = idle_frames

# Boucle principale
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_attacking = True
            frame_index = 0
            animation_timer = 0

    # Clavier
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_q]:
        player_pos.x -= 5
        facing_left = True
        moving = True
    if keys[pygame.K_d]:
        player_pos.x += 5
        facing_left = False
        moving = True
    if keys[pygame.K_SPACE] and on_ground:
        player_vel.y = jump_force
        on_ground = False

    # Gravité
    player_vel.y += gravity
    player_pos.y += player_vel.y

    # Sol
    if player_pos.y >= screen_height - 170:
        player_pos.y = screen_height - 170
        player_vel.y = 0
        on_ground = True

    # Sélection animation
    if is_attacking and len(attack_frames) > 0:
        new_frames = attack_frames
    elif not on_ground:
        new_frames = idle_frames
    elif moving and len(run_frames) > 0:
        new_frames = run_frames
    else:
        new_frames = idle_frames

    if new_frames != current_frames:
        current_frames = new_frames
        frame_index = 0
        animation_timer = 0

    if len(current_frames) == 0:
        continue

    # Animation
    animation_timer += dt
    if animation_timer >= frame_duration:
        animation_timer = 0
        frame_index = (frame_index + 1) % len(current_frames)
        if is_attacking and current_frames == attack_frames and frame_index == 0:
            is_attacking = False

    # Affichage
    screen.blit(bg, (0, 0))  # ← fond adapté à toute la fenêtre
    current_image = current_frames[frame_index]
    if facing_left:
        current_image = pygame.transform.flip(current_image, True, False)
    image_rect = current_image.get_rect(center=player_pos)
    screen.blit(current_image, image_rect)

    pygame.display.flip()

pygame.quit()
