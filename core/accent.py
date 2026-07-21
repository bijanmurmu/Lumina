import subprocess
import ctypes

def get_current_wallpaper():
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
        val, _ = winreg.QueryValueEx(key, "WallPaper")
        winreg.CloseKey(key)
        return val
    except:
        return None

def set_accent_color(hex_color: str):
    """
    Sets the Windows accent color via the Registry.
    """
    try:
        if hex_color.lower() == "auto":
            ps_command = f"Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name 'AutoColorization' -Value 1 -Type DWord;"
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
            
            # Force Windows to recalculate the color instantly by refreshing the wallpaper
            current_wallpaper = get_current_wallpaper()
            if current_wallpaper:
                SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, current_wallpaper, 3)
                
        else:
            # Convert standard #RRGGBB to Windows registry BGR format
            clean_hex = hex_color.lstrip('#')
            if len(clean_hex) == 6:
                r, g, b = clean_hex[0:2], clean_hex[2:4], clean_hex[4:6]
                clean_hex = b + g + r
            color_int = int(clean_hex, 16)
            
            ps_command = f"""
            Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop' -Name 'AutoColorization' -Value 0 -Type DWord;
            Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Accent' -Name 'AccentColorMenu' -Value {color_int} -Type DWord;
            Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\DWM' -Name 'AccentColor' -Value {color_int} -Type DWord;
            """
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    except Exception as e:
        print(f"Error setting accent color: {e}")
