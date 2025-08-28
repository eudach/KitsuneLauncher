
import json
import aiohttp
import re

class ModrinthAPI:
    BASE_URL = "https://api.modrinth.com/v2"

    def __init__(self, page=None):
        self.session = None
        self.page = page  # Para guardar page.temp_config_modrinth['total_mods_result']  y page.temp_config_modrinth['list_mods_cache'] si se desea

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()
    
    async def get_more(self, slug):
        url = f"{self.BASE_URL}/project/{slug}/version?version_type=release"

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return {}
                mods_data = await response.json()
                
        except aiohttp.ClientError:
            return {}
        
    def es_version_estable(self, v: str) -> bool:
        """
        Retorna True si la versión es estable (ej: 1.20.4), False si es snapshot (ej: 23w45a).
        """
        return re.match(r"^1\.\d+(\.\d+)?$", v) is not None

    async def get_mod_description(self, slug: str) -> dict:
        url = f"{self.BASE_URL}/project/{slug}"

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return {}
                mods_data = await response.json()
        except aiohttp.ClientError:
            return {}

        versions = []
        for e in mods_data.get('game_versions', []):
            if self.es_version_estable(e):
                versions.append(e)
        versions.reverse()
        
        body = mods_data.get("body", "")
        body_images = re.findall(r'!\[.*?\]\((.*?)\)', body)
        
        return {
            "versions": versions,
            "icon_url": mods_data.get('icon_url'),
            "loaders": mods_data.get('loaders', []),
            "description": mods_data.get('description'),
            "body_images": body_images,
            "title": mods_data.get('title'),
            "categories": mods_data.get('categories', []),
            "client_side": mods_data.get('client_side'),
            "server_side": mods_data.get('server_side'),
            "gallery": mods_data.get('gallery', [])
        }
        
    async def search_mod_modrinth(
        self, query: str = "", limit: int = 10, offset: int = 0, loader: str | None = None
    ) -> list[dict]:
        self.page.temp_config_modrinth['list_mods_cache'] = []
        
        url = f"{self.BASE_URL}/search"
        facets = [["project_type:mod"]]
        if loader:
            facets.append([f"categories:{loader.lower()}"])

        params = {
            "query": query,
            "limit": limit,
            "offset": offset,
            "facets": json.dumps(facets)  # JSON válido, no str() de Python
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return []
                data = await response.json()
        except aiohttp.ClientError:
            return []

        mods_data = data.get("hits", [])
        self.page.temp_config_modrinth['total_mods_result'] = data.get("total_hits", 0)
        mods = []
        for mod in mods_data:
            self.page.temp_config_modrinth['list_mods_cache'].append(mod["slug"])
            mods.append({
                "name": mod["title"],
                "slug": mod["slug"],
                "imgs": mod.get("gallery", []),
                "icon": mod.get("icon_url") or "icon.png",
                "description": mod.get("description", "")[:100],
            })
        return mods


