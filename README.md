# 🦊 Kitsune Launcher

**Kitsune Launcher** es un launcher no oficial de Minecraft, hecho con ❤️ en Python usando [Flet](https://flet.dev) para la interfaz gráfica y [minecraft_launcher_lib](https://github.com/JakobDev/minecraft-launcher-lib) para gestionar instalaciones y ejecuciones del juego.

> 🚧 Proyecto en desarrollo activo — ¡Buscamos colaboradores!

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

> Imagenes de la version 1.0.1.

| Consola | Configuración | Perfil |
|-------|---------------|---------------------|
| ![console](https://snipboard.io/U69BwR.jpg) | ![config](https://snipboard.io/5871yb.jpg) | ![perfil](https://snipboard.io/McstKu.jpg) |

---

## 💾 Requisitos de instalación

Para ejecutar Kitsune Launcher necesitas:

- ✅ **Java JDK 24 (recomendado)** o al menos **JDK 17** instalado y agregado al PATH
- ✅ **Python 3.10+** instalado (mejora la experiencia en algunos entornos)
- ✅ Archivos clásicos de Minecraft (assets, `.minecraft`, etc.)
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
| 💻 Flet-contrib | [🔗 GitHub - Flet-contrib](https://github.com/flet-dev/flet-contrib) |
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

## ❕ Cambios

# 🦊 Kitsune Launcher - Versión 0.1.3

## 📌 Cambios desde la versión 0.1.2

---

### 🔐 Cambio en el manejo de `USERNAME`

- **Antes:**
  ```python
  page.launcher.config.set("username", nombre)
  ```
- **Ahora:**
  ```python
  page.launcher.set_username(nombre)
  ```

✔️ Se encapsuló el acceso al nombre de usuario para mejorar la organización del código.

---

### ✅ Solución al problema de ventana inmóvil (Windows)

Anteriormente, el launcher no se podía mover al usar interfaz sin bordes. Ahora se soluciona agregando:

```python
page.window.frameless = True
```

✔️ Esto permite que el `WindowDragArea` funcione correctamente.

---

### ⚙️ Cambio en la configuración

- **Formato anterior:** `config.pickle`
- **Formato actual:** `config.json`

- **Ruta anterior:**  
  ```python
  %APPDATA%\config.pickle
  ```

- **Ruta actual:**  
  ```python
  %APPDATA%\KitsuneLauncher\config.json
  ```

✔️ Se migró de `pickle` a `json` para mayor compatibilidad al empaquetar la aplicación.

---

### ✅ Resumen de mejoras

- Código más limpio y mantenible.
- Launcher ahora completamente funcional al ser empaquetado.
- Preparado para futuras expansiones del sistema de configuración.

---

**Versión anterior:** `0.1.2`  
**Versión actual:** `0.1.3`