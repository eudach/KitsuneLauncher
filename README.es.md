# 🦊 Kitsune Launcher

[![en](https://img.shields.io/badge/lang-en-gree.svg)](link)

**Kitsune Launcher** es un launcher no oficial de Minecraft, hecho con ❤️ en Python usando [Flet](https://flet.dev) para la interfaz gráfica y [minecraft_launcher_lib](https://github.com/JakobDev/minecraft-launcher-lib) para gestionar instalaciones y ejecuciones del juego.

> 🚧 Proyecto en desarrollo activo

---

## 🎯 Características

- Interfaz moderna y personalizable
- Soporte para cuentas no premium (próximamente premium)
- Selector de versión
- idiomas: english y español
- Compatible con servidores alternativos
- En camino: soporte de skins y más

---

## 🖼️ Capturas de pantalla

> Imagenes de la version 0.1.5

| Modrinth | Configuración | Perfil |
|-------|---------------|---------------------|
| ![modrinth](https://snipboard.io/l8PeHv.jpg) | ![config](https://snipboard.io/BA6kp8.jpg) | ![perfil](https://snipboard.io/RjN8cg.jpg) |

---

## 💾 Requisitos de instalación

Para ejecutar Kitsune Launcher necesitas:

- ✅ **Java JDK 24 (recomendado) o JDK 17 Adoptium**
- ✅ Conexión a internet para descargar versiones

---

## ⚙️ Instrucciones de instalación

1. Descarga el archivo `KitsuneLauncher_Setup.exe` desde la sección de releases.
2. Ejecuta el instalador y sigue los pasos.
3. Abre Kitsune Launcher desde el escritorio o el menú de inicio.
4. Configura tu idioma, ruta de Java y carpeta `.minecraft`.
5. Selecciona la versión de Minecraft que deseas jugar.
6. ¡Listo para jugar!

> 🛠 Si tienes problemas, asegúrate de tener Java correctamente configurado en el sistema.

---

## 🧠 Tecnologías utilizadas

| Proyecto | Enlace |
|----------|--------|
| 🎨 Flet | [🔗 GitHub - Flet](https://github.com/flet-dev/flet) |
| 🔀 Flet-route | [🔗 GitHub - Flet-route](https://github.com/saurabhwadekar/flet_route) |
| 🧱 minecraft_launcher_lib | [🔗 GitHub - minecraft_launcher_lib](https://github.com/JakobDev/minecraft-launcher-lib) |

> ⚠️ **Estos repositorios no son de mi autoría.** Todos los créditos a sus respectivos desarrolladores.

---

## 🤝 ¿Quieres colaborar?

El proyecto está abierto a quienes deseen mejorar el launcher o aprender:

- Reporta errores o bugs
- Sugiere nuevas funcionalidades
- Crea Pull Requests con mejoras
- ¡O simplemente únete al desarrollo!

Puedes abrir un `issue` o contactar directamente.

---

## 🌐 Licencia

Este proyecto es de **libre uso y distribución no comercial**.  
Puedes estudiar, modificar y compartir el código con fines educativos o personales.

## 🆕 Novedades en la versión 0.1.5

- 🖥️ **Se quitó la consola** de los selectores principales, para dar más comodidad y espacio.  
- 🌐 **Nuevo apartado de Modrinth**: por ahora solo mods, pero pronto incluirá texturas, mapas y más. Es solo una vista previa y más adelante permitirá **descargar directamente**.  
- 📜 **Reescritura completa del código base** para mayor legibilidad, comodidad y mantenimiento.  
- 🎨 **Nuevo Color Picker propio**, reemplazando al antiguo de *flet_contrib*.  
- 🚫 **Prevención de múltiples ejecuciones**: ahora no se puede iniciar Minecraft más de una vez por error.  
- 📦 **Instalación mejorada de versiones** de Minecraft: ahora se muestra de forma más clara y organizada.  