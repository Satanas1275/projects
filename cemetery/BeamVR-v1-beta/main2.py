import openvr
import glfw
from OpenGL.GL import *
import numpy as np
from mss import mss
import pygetwindow as gw
import time
import ctypes

def init_vr():
    try:
        openvr.init(openvr.VRApplication_Overlay)
        print("OpenVR initialisé avec succès.")
        return openvr.VRSystem(), openvr.VRCompositor()
    except Exception as e:
        print(f"Erreur lors de l'initialisation d'OpenVR : {e}")
        return None, None

def select_window():
    windows = [w for w in gw.getAllWindows() if w.title]
    if not windows:
        print("Aucune fenêtre détectée.")
        return None
    
    print("Fenêtres disponibles :")
    for i, w in enumerate(windows):
        print(f"{i}: {w.title}")
    
    try:
        choice = int(input("Entrez le numéro de la fenêtre à capturer : "))
        if 0 <= choice < len(windows):
            w = windows[choice]
            print(f"Fenêtre sélectionnée : {w.title}")
            return {'left': w.left, 'top': w.top, 'width': w.width, 'height': w.height}
        else:
            print("Numéro invalide.")
            return None
    except ValueError:
        print("Entrée invalide.")
        return None

def capture_window(region):
    try:
        with mss() as sct:
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            img = img[:, :, [2, 1, 0, 3]]  # RGBA -> BGRA
            img = np.flipud(img)  # Corriger le retournement vertical
            print("Capture réussie.")
            return img
    except Exception as e:
        print(f"Erreur lors de la capture : {e}")
        return None

def create_texture(width, height):
    try:
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        print(f"Texture créée : ID {texture_id}")
        return texture_id
    except Exception as e:
        print(f"Erreur lors de la création de la texture : {e}")
        return None

def update_texture(texture_id, image):
    try:
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, image.shape[1], image.shape[0], GL_RGBA, GL_UNSIGNED_BYTE, image)
        print("Texture mise à jour.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la texture : {e}")

def main():
    # Initialisation GLFW
    if not glfw.init():
        print("Échec de l'initialisation de GLFW")
        return

    # Fenêtre invisible pour le contexte OpenGL
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(640, 480, "Hidden OpenGL Context", None, None)
    if not window:
        print("Échec de la création de la fenêtre GLFW")
        glfw.terminate()
        return
    glfw.make_context_current(window)
    print("Contexte GLFW créé.")

    # Initialisation VR
    vr_system, compositor = init_vr()
    if not vr_system or not compositor:
        glfw.terminate()
        return

    # Sélection de la fenêtre
    region = select_window()
    if not region:
        glfw.terminate()
        openvr.shutdown()
        return
    width, height = region['width'], region['height']
    print(f"Région sélectionnée : {region}")

    # Création de la texture
    texture_id = create_texture(width, height)
    if not texture_id:
        glfw.terminate()
        openvr.shutdown()
        return

    # Création de l'overlay
    overlay = openvr.VROverlay()
    overlay_key = "WindowCaptureOverlay"
    overlay_name = "Capture de fenêtre"
    try:
        overlay_handle = overlay.createOverlay(overlay_key, overlay_name)
        print(f"Overlay créé : handle {overlay_handle}")
    except Exception as e:
        print(f"Erreur lors de la création de l'overlay : {e}")
        glfw.terminate()
        openvr.shutdown()
        return

    # Configuration de l'overlay
    try:
        overlay.setOverlayWidthInMeters(overlay_handle, 2.5)  # Largeur augmentée à 2.5m
        print("Largeur de l'overlay définie à 2.5 mètres.")
        
        # Position initiale devant le casque (matrice 4x3 compatible ctypes)
        hmd_pose = openvr.HmdMatrix34_t()
        matrix = [
            [1.0, 0.0, 0.0, 0.2],  # Décalage de 0.2m à droite
            [0.0, 1.0, 0.0, 0.0],  # Pas de décalage vertical
            [0.0, 0.0, 1.0, -0.5],  # 0.5m devant
        ]
        for i in range(3):
            for j in range(4):
                hmd_pose[i][j] = matrix[i][j]
        overlay.setOverlayTransformTrackedDeviceRelative(overlay_handle, openvr.k_unTrackedDeviceIndex_Hmd, hmd_pose)
        print("Position initiale de l'overlay définie (0.5m devant, 0.2m à droite).")
    except Exception as e:
        print(f"Erreur lors de la configuration de l'overlay : {e}")
        return

    try:
        while True:
            image = capture_window(region)
            if image is None:
                print("Échec de la capture, arrêt.")
                break

            update_texture(texture_id, image)
            vr_texture = openvr.Texture_t()
            vr_texture.handle = int(texture_id)
            vr_texture.eType = openvr.TextureType_OpenGL
            vr_texture.eColorSpace = openvr.ColorSpace_Gamma
            print("Texture VR préparée.")

            overlay.setOverlayTexture(overlay_handle, vr_texture)
            print("Texture envoyée à l'overlay.")
            overlay.showOverlay(overlay_handle)
            print("Overlay affiché.")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Arrêt par l'utilisateur.")
    except Exception as e:
        print(f"Erreur dans la boucle principale : {e}")
        import traceback
        traceback.print_exc()
    finally:
        overlay.destroyOverlay(overlay_handle)
        glDeleteTextures(1, [texture_id])
        glfw.destroy_window(window)
        glfw.terminate()
        openvr.shutdown()
        print("Nettoyage terminé.")

if __name__ == "__main__":
    main()