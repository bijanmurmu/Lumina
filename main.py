import sys
import os
import json

# Append the plugin root and core folder to the path so we can import our modules
plugin_root = os.path.dirname(__file__)
sys.path.append(plugin_root)
sys.path.append(os.path.join(plugin_root, "core"))

from theme import set_theme
from wallpaper import set_wallpaper

class FlowLauncher:
    """
    A lightweight, zero-dependency wrapper for Flow Launcher plugins.
    """
    def __init__(self):
        if len(sys.argv) > 1:
            try:
                request = json.loads(sys.argv[1])
                method = request.get("method")
                parameters = request.get("parameters", [])
                
                if method == "query":
                    results = self.query(*parameters)
                    print(json.dumps({"result": results}))
                else:
                    func = getattr(self, method)
                    func(*parameters)
            except Exception as e:
                print(json.dumps({"result": [{
                    "Title": "Error execution plugin",
                    "SubTitle": str(e),
                    "IcoPath": "Images/app.png"
                }]}))
        else:
            print("This script is meant to be run by Flow Launcher.")

    def query(self, query):
        return []

class Lumina(FlowLauncher):

    def get_settings(self):
        settings_file = os.path.join(plugin_root, "settings.json")
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                return json.load(f)
        return {"wallpaper_dir": os.path.expanduser("~/Pictures")}

    def save_settings(self, settings):
        settings_file = os.path.join(plugin_root, "settings.json")
        with open(settings_file, "w") as f:
            json.dump(settings, f)

    def query(self, raw_query):
        results = []
        query = raw_query.strip().lower()

        if query.startswith("theme"):
            results.append({
                "Title": "Set Theme to Dark",
                "SubTitle": "Switch Windows to Dark Mode",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "change_theme",
                    "parameters": ["dark"],
                    "dontHideAfterAction": False
                }
            })
            results.append({
                "Title": "Set Theme to Light",
                "SubTitle": "Switch Windows to Light Mode",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "change_theme",
                    "parameters": ["light"],
                    "dontHideAfterAction": False
                }
            })
        
        elif query.startswith("accent"):
            color = query.replace("accent", "").strip().upper()
            defaults = {"Auto Match Wallpaper": "auto", "Red": "#FF0000", "Blue": "#0000FF", "Green": "#00FF00", "Purple": "#800080", "Teal": "#008080"}
            
            if not color:
                for name, hex_val in defaults.items():
                    results.append({
                        "Title": f"Set Accent to {name}",
                        "SubTitle": "Automatically pick an accent color from my background" if hex_val == "auto" else f"Change Windows accent color to {hex_val}",
                        "IcoPath": "Images/app.png",
                        "JsonRPCAction": {
                            "method": "change_accent",
                            "parameters": [hex_val],
                            "dontHideAfterAction": False
                        }
                    })

        elif query.startswith("config wall"):
            path = raw_query.strip()[len("config wall"):].strip()
            if path:
                # Provide directory autocomplete suggestions
                search_dir = path
                search_prefix = ""
                
                if not os.path.exists(path) or not os.path.isdir(path):
                    search_dir = os.path.dirname(path)
                    search_prefix = os.path.basename(path).lower()
                    
                if os.path.exists(search_dir) and os.path.isdir(search_dir):
                    try:
                        for item in os.listdir(search_dir):
                            full_item_path = os.path.join(search_dir, item)
                            if os.path.isdir(full_item_path):
                                if not search_prefix or item.lower().startswith(search_prefix):
                                    results.append({
                                        "Title": item,
                                        "SubTitle": full_item_path,
                                        "IcoPath": "Images/app.png",
                                        "AutoCompleteText": f"lumina config wall {full_item_path}\\",
                                    })
                    except PermissionError:
                        pass

                # If the exact path they typed is a valid directory, offer to save it at the very top
                if os.path.exists(path) and os.path.isdir(path):
                    results.insert(0, {
                        "Title": f"Save wallpaper folder: {path}",
                        "SubTitle": "Press Enter to save this configuration",
                        "IcoPath": "Images/app.png",
                        "JsonRPCAction": {
                            "method": "change_wallpaper_dir",
                            "parameters": [path],
                            "dontHideAfterAction": False
                        }
                    })
                elif not results:
                    results.append({
                        "Title": "Folder not found",
                        "SubTitle": "Keep typing to see directory suggestions...",
                        "IcoPath": "Images/app.png"
                    })
            else:
                settings = self.get_settings()
                current_dir = settings.get("wallpaper_dir", os.path.expanduser("~/Pictures"))
                # Suggest common drives
                results.append({
                    "Title": "Configure Wallpaper Folder",
                    "SubTitle": f"Current: {current_dir}. Start typing a path (e.g. C:\\) to browse.",
                    "IcoPath": "Images/app.png",
                    "AutoCompleteText": "lumina config wall C:\\"
                })

        elif query.startswith("wall"):
            search_term = query.replace("wall", "").strip()
            settings = self.get_settings()
            wallpaper_dir = settings.get("wallpaper_dir", os.path.expanduser("~/Pictures"))
            
            if os.path.exists(wallpaper_dir):
                valid_exts = {".jpg", ".jpeg", ".png", ".bmp"}
                found = False
                for file in os.listdir(wallpaper_dir):
                    if any(file.lower().endswith(ext) for ext in valid_exts):
                        if search_term in file.lower():
                            found = True
                            full_path = os.path.join(wallpaper_dir, file)
                            results.append({
                                "Title": file,
                                "SubTitle": "Set this as wallpaper",
                                "IcoPath": full_path, # Show the actual image preview in Flow Launcher!
                                "JsonRPCAction": {
                                    "method": "change_wallpaper",
                                    "parameters": [full_path],
                                    "dontHideAfterAction": False
                                }
                            })
                if not found:
                    results.append({
                        "Title": "No wallpapers found",
                        "SubTitle": f"No images matching '{search_term}' in {wallpaper_dir}",
                        "IcoPath": "Images/app.png"
                    })
            else:
                results.append({
                    "Title": "Wallpaper folder not found",
                    "SubTitle": f"Please set a valid folder using 'lumina config wall <path>'",
                    "IcoPath": "Images/app.png"
                })

        else:
            # Default helper screen
            results.append({
                "Title": "Lumina",
                "SubTitle": "Type 'theme dark/light' or 'wall <image_path>'",
                "IcoPath": "Images/app.png"
            })
            
        return results

    def change_theme(self, mode):
        # mode will be either "dark" or "light"
        set_theme(mode == "light")
        return None  # FlowLauncher expects no return value for actions unless updating UI

    def change_wallpaper(self, path):
        set_wallpaper(path)
        return None

    def change_wallpaper_dir(self, path):
        settings = self.get_settings()
        settings["wallpaper_dir"] = path
        self.save_settings(settings)
        return None

if __name__ == "__main__":
    Lumina()
