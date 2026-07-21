import winreg

def set_theme(is_light_mode: bool):
    """
    Sets the Windows theme to Light (True) or Dark (False).
    """
    value = 1 if is_light_mode else 0
    try:
        # Change Apps Theme & System Theme
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 
            0, 
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(registry_key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
        winreg.SetValueEx(registry_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        winreg.CloseKey(registry_key)
        
        mode = "Light" if is_light_mode else "Dark"
        return True, f"Theme set to {mode} Mode."
    except Exception as e:
        return False, f"Failed to set theme: {str(e)}"
