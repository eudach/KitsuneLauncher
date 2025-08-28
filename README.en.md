# 🦊 Kitsune Launcher

[![es](https://img.shields.io/badge/lang-es-gree.svg)](link)

**Kitsune Launcher** is an unofficial Minecraft launcher, made with ❤️ in Python using [Flet](https://flet.dev) for the graphical interface and [minecraft_launcher_lib](https://github.com/JakobDev/minecraft-launcher-lib) to manage installations and game launches.

> 🚧 Project under active development

---

## 🎯 Features

- Modern and customizable interface
- Support for non-premium accounts (premium soon)
- Version selector
- Languages: English and Spanish
- Compatible with alternative servers
- Coming soon: skin support and more

---

## 🖼️ Screenshots

> Images from version 0.1.5

| Modrinth | Settings | Profile |
|-------|---------------|---------------------|
| ![modrinth](https://snipboard.io/l8PeHv.jpg) | ![config](https://snipboard.io/BA6kp8.jpg) | ![profile](https://snipboard.io/RjN8cg.jpg) |

---

## 💾 Installation requirements

To run Kitsune Launcher you need:

- ✅ **Java JDK 24 (recommended) or JDK 17 Adoptium**
- ✅ Internet connection to download versions

---

## ⚙️ Installation instructions

1. Download the file `KitsuneLauncher_Setup.exe` from the releases section.
2. Run the installer and follow the steps.
3. Open Kitsune Launcher from the desktop or start menu.
4. Configure your language, Java path and `.minecraft` folder.
5. Select the Minecraft version you want to play.
6. Ready to play!

> 🛠 If you have problems, make sure Java is properly configured on your system.

---

## 🧠 Technologies used

| Project | Link |
|----------|--------|
| 🎨 Flet | [🔗 GitHub - Flet](https://github.com/flet-dev/flet) |
| 🔀 Flet-route | [🔗 GitHub - Flet-route](https://github.com/saurabhwadekar/flet_route) |
| 🧱 minecraft_launcher_lib | [🔗 GitHub - minecraft_launcher_lib](https://github.com/JakobDev/minecraft-launcher-lib) |

> ⚠️ **These repositories are not my work.** All credits to their respective developers.

---

## 🤝 Want to collaborate?

The project is open to anyone who wants to improve the launcher or learn:

- Report errors or bugs
- Suggest new features
- Create Pull Requests with improvements
- Or simply join the development!

You can open an `issue` or contact me directly.

---

## 🌐 License

This project is for **free non-commercial use and distribution**.  
You can study, modify and share the code for educational or personal purposes.

## 🆕 What's new in version 0.1.5

- 🖥️ **Console removed** from the main selectors, for more convenience and space.  
- 🌐 **New Modrinth section**: for now only mods, but soon it will include textures, maps and more. It's just a preview and will later allow **direct download**.  
- 📜 **Complete rewrite of the code base** for better readability, usability and maintenance.  
- 🎨 **New custom Color Picker**, replacing the old one from *flet_contrib*.  
- 🚫 **Prevention of multiple executions**: now Minecraft cannot be started more than once by mistake.  
- 📦 **Improved installation display of Minecraft versions**: now shown more clearly and organized.  