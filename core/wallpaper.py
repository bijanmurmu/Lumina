import ctypes
import os
import subprocess

def get_current_wallpaper():
    buffer = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(115, 512, buffer, 0) # SPI_GETDESKWALLPAPER = 115
    return buffer.value

def set_wallpaper(image_path: str):
    """
    Sets the Windows desktop wallpaper using the custom LuminaAnimator hardware-accelerated transition engine.
    """
    if not os.path.exists(image_path):
        return False, f"Image not found at path: {image_path}"
        
    try:
        current_wall = get_current_wallpaper()
        animator_path = os.path.join(os.path.dirname(__file__), "LuminaAnimator.exe")
        
        if os.path.exists(animator_path) and os.path.exists(current_wall):
            subprocess.Popen([animator_path, current_wall, image_path, "circle"])
            return True, "Wallpaper transition started."
        else:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            return True, "Wallpaper updated (fallback mode)."
            
    except Exception as e:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        return False, f"Failed to animate, used fallback: {str(e)}"
