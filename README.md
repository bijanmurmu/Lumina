# Lumina for Flow Launcher

Lumina is a fast, zero-dependency plugin for [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher) that lets you customize your Windows desktop environment instantly from your keyboard.

## Features

* **Theme Switcher:** Instantly toggle your Windows system and apps between Light and Dark mode. Features dynamic sun/moon icons in the results!
  * *Usage:* `lumina theme dark` or `lumina theme light`
* **Wallpaper Gallery:** Browse, search, and apply wallpapers directly from a local folder. Flow Launcher will display actual image previews next to the search results.
  * *Setup:* First, set your wallpaper folder by typing: `lumina config wall C:\Path\To\Your\Wallpapers`
  * *Usage:* `lumina wall` (lists all) or `lumina wall space` (searches for "space")
* **Accent Color Switcher:** Quickly change your Windows UI highlight and accent colors.
  * *Usage:* `lumina accent` (shows a list of defaults including "Auto Match Wallpaper") or `lumina accent #FFA500` (for a custom hex code). 
  * *Note:* The "Auto Match" option forces an instant UI refresh to ensure your title bars and borders immediately match your background!

## Installation

1. Download or clone this repository.
2. Move the `Lumina` folder into your Flow Launcher plugins directory:
   `%appdata%\FlowLauncher\Plugins`
3. Type `restart flow` in Flow Launcher.

## Configuration

You can configure the plugin directly from within Flow Launcher—no code editing required!

* **Set Wallpaper Directory:** 
  To change where Lumina looks for your wallpapers, simply type:
  `lumina config wall C:\Path\To\Your\Wallpapers`
  
*(Note: If you don't configure a folder, Lumina will automatically default to your Windows `Pictures` directory).*
