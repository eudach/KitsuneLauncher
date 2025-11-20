from discordrp import Presence
import socket
import requests

class DiscordReachPresence:
    
    def __init__(self, page, started:bool=True):
        self.page = page
        self.id = "1394361962212626543"
        self.connected_state = True
        self.page_presence = None
        
        # Verificar conectividad a internet antes de intentar conectar Discord
        if self._check_internet_connection() == False:
            self.connected_state = False
            self.page.logger.error(f"🌐 Discord: offline ❌")
            return
            
        try:
            self.page_presence = Presence(self.id)
        except Exception as e:
            page.logger.error(f"Error conectando con Discord: {e}")
            self.connected_state = False
            
        if started and self.connected_state:
            self.update()
    
    def close(self):
        if not self.connected_state or self.page_presence is None:
            return
        
        if not self._check_internet_connection():
            self.connected_state = False
            return
        try:
            self.page_presence.close()
        except Exception as e:
            self.page.logger.error(f"Error cerrando conexión con Discord: {e}")
            self.connected_state = False
    
    def _check_internet_connection(self, timeout=3):
        """Verifica si hay conexión a internet"""
        try:
            # Intentar conectar a un servidor DNS público
            socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            
            return True
        except OSError:
            try:
                # Fallback: intentar hacer una petición HTTP simple
                response = requests.get("https://www.google.com", timeout=timeout)
                return response.status_code == 200
            except:
                return False
            
    @property
    def connected(self):
        return self.connected_state

    @connected.setter
    def connected_setter(self, valor):
        self.connected_state = valor
    
    def clear(self):
        if not self.connected_state or self.page_presence is None:
            return
        
        self.page_presence.clear()
    
    def reconnect(self):
        """Intenta reconectar Discord cuando se recupere la conexión"""
        if self.connected_state:
            return True
            
        if not self._check_internet_connection():
            return False
            
        try:
            self.page_presence = Presence(self.id)
            self.connected_state = True
            return True
        except Exception as e:
            self.page.logger.error(f"Error reconectando con Discord: {e}")
            return False
        
    def update(self):
        if not self.connected_state or self.page_presence is None:
            return
        
        # Verificar conectividad antes de actualizar
        if not self._check_internet_connection():
            self.connected_state = False
            return
        
        page = self.page
        name = page.launcher.username
        minecraft_opened = page.temp_config_modrinth["minecraft_started"]
        state_ = None
        details_ = None
        if minecraft_opened:
            version = page.launcher.last_played_version[0]
            version_name = version
            version_details = ""
            if len(version.split("-"))>1:
                version_name = version.split("-")[0]
                version_details = version.split("-")[1]
            details_ = f"{name} {page.t("user_state_discord_conect")}"
            state_ = f"{page.t("user_state_discord_playing")} {version_name} {version_details}"
        else:
            
            details_ = f"{name} {page.t("user_state_discord_conect")}" if name is not None else f"{page.t("user_state_discord_disconect")}"
            state_ = page.t("user_state_discord_mainpage")
        try:
            self.page_presence.set(
                {
                    "state": state_,
                    "details": details_,
                    "timestamps": {"start": int(page.global_vars["discord_time_instance"])},
                    "buttons": [
                        {
                            "label": "Github",
                            "url": "https://github.com/eudach/KitsuneLauncher",
                        }
                    ],
                }
            )
            page.logger.debug(f"Presencia de Discord actualizada")
        except Exception as e:
            page.logger.error(f"Error actualizando presencia de Discord: {e}")
            self.connected_state = False
    