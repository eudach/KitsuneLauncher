from discordrp import Presence

class DiscordReachPresence:
    
    def __init__(self, page, started:bool=True):
        self.page = page
        self.id = "our_own_bot_id"
        self.connected_state = True
        try:
            self.page_presence = Presence(self.id)
        except:
            self.connected_state = False
        if started:
            self.update()
            
    @property
    def connected(self):
        return self.connected_state

    @connected.setter
    def connected_setter(self, valor):
        self.connected_state = valor
    
    def clear(self):
        if not self.connected_state:
            return
        
        self.page_presence.clear()
        
    def update(self):
        if not self.connected_state:
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
                    "timestamps": {"start": int(page.discord_times)},
                    "buttons": [
                        {
                            "label": "Github",
                            "url": "https://github.com/eudach/KitsuneLauncher",
                        }
                    ],
                }
            )
        except:
            self.connected_state = False
    