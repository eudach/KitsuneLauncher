import json
from pathlib import Path
import aiohttp
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from aiohttp import ClientError
from markdownify import markdownify as md
from core.utils import sha1_of_file_with_progress
import asyncio

class ProjectType(str, Enum):
    """Tipos de proyectos soportados por Modrinth."""
    MOD = "mod"
    MODPACK = "modpack"
    RESOURCEPACK = "resourcepack"
    SHADER = "shader"
    DATAPACK = "datapack"
    PLUGIN = "plugin"

@dataclass
class ModrinthProject:
    """Representación de un proyecto de Modrinth."""
    name: str
    slug: str
    imgs: List[str]
    icon: str
    description: str
    total_versions: int = 0
    client_side: Optional[bool] = None
    server_side: Optional[bool] = None

@dataclass
class ModrinthVersionInfo:
    """Información resumida de versiones disponibles."""
    stable_versions: List[str]
    loaders: List[str]
    icon_url: str
    description: Optional[str]
    title: str
    categories: List[str]
    client_side: Optional[bool]
    server_side: Optional[bool]
    body: List[str]
    gallery: List[Dict[str, Any]]
    slug:str
    
class ModrinthAPI:
    BASE_URL = "https://api.modrinth.com/v2"
    HEADERS = {"User-Agent": "ModrinthAPI-Client/1.0"}

    MIN_LIMIT = 1
    MAX_LIMIT = 100
    DEFAULT_LIMIT = 10
    STABLE_VERSION_PATTERN = re.compile(r"^1\.\d+(\.\d+)?$")

    def __init__(self, page=None, timeout: float = 30.0):
        self.page = page
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> 'ModrinthAPI':
        """Inicializa la sesión para usar la API múltiples veces."""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers=self.HEADERS,
                timeout=self.timeout,
                connector=aiohttp.TCPConnector(limit=10, limit_per_host=5)
            )
        return self

    async def close(self):
        """Cierra la sesión de forma segura."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        if response.status != 200:
            return {}
        try:
            return await response.json()
        except (json.JSONDecodeError, aiohttp.ContentTypeError):
            return {}

    async def _ensure_session(self):
        """Garantiza que exista una sesión activa antes de realizar requests."""
        if not self.session or self.session.closed:
            await self.start()

    async def _make_request(self, url: str, **kwargs) -> Dict[str, Any]:
        try:
            await self._ensure_session()
            async with self.session.get(url, **kwargs) as response:
                return await self._handle_response(response)
        except (ClientError, asyncio.TimeoutError):
            return {}

    def is_stable_version(self, version: str) -> bool:
        return bool(self.STABLE_VERSION_PATTERN.match(version))

    def clean_mod_name(self, file_name: str) -> str:
        # Quitar extensiones
        name = re.sub(r"\.jar$", "", file_name, flags=re.IGNORECASE)
        # Quitar "[Forge]" u otros corchetes al inicio
        name = re.sub(r"^\[.*?\]\s*", "", name)
        # Quitar números al inicio
        name = re.sub(r"^\d+\s*", "", name)
        # Quitar versiones (números y guiones al final)
        name = re.sub(r"(-forge|-Forge)?-[\d.+]+.*$", "", name)
        # Limpiar espacios extra
        name = name.strip()
        
        return name
    async def search_project(
        self, function_on_progress, file_path, algorithm: str = "sha1", project_type:str="mod"
    ) -> Optional[ModrinthVersionInfo]:
        """
        Busca un proyecto en Modrinth a partir del hash de un archivo (.jar).
        Retorna None si no se encuentra.
        """
        if algorithm not in ("sha1", "sha512"):
            raise ValueError("Algoritmo no soportado, usa 'sha1' o 'sha512'")

        # 1. Calcular hash
        hash_val = await sha1_of_file_with_progress(
            path=Path(file_path),
            on_progress=function_on_progress
        )

        # 2. Consultar en Modrinth
        url = f"{self.BASE_URL}/version_file/{hash_val}?algorithm={algorithm}"
        data = await self._make_request(url)

        if not data:
            name = self.clean_mod_name(file_path.name)
            
            
            data = await self.search_projects(query=name, limit=1, project_type=project_type)
            if len(data[0]) == 0:
                return None
            return await self.get_project_details(data[0][0].slug)

        # 3. Obtener project_id y llamar a get_project_details
        project_id = data.get("project_id")

        return await self.get_project_details(project_id)

    
    async def get_project_details(self, slug: str) -> ModrinthVersionInfo:
        """
        Obtiene detalles completos de un proyecto, incluyendo versiones estables.
        
        Args:
            slug: Identificador único del proyecto o project_id
            
        Returns:
            Información del proyecto o objeto vacío si hay error
        """
        url = f"{self.BASE_URL}/project/{slug}"
        data = await self._make_request(url)
        
        if not data:
            return ModrinthVersionInfo(
                stable_versions=[],
                loaders=[],
                icon_url="iconos/no_found_image.png",
                description=None,
                title="",
                categories=[],
                client_side=None,
                server_side=None,
                body=[],
                gallery=[],
                slug=""
            )
        
        # Filtrar versiones estables
        game_versions = data.get('game_versions', [])
        stable_versions = [
            version for version in game_versions 
            if self.is_stable_version(version)
        ]
        stable_versions.sort(reverse=True)  # Más reciente primero
        
        # Extraer imágenes del body
        body = data.get("body", "")
        
        return ModrinthVersionInfo(
            stable_versions=stable_versions,
            loaders=data.get('loaders', []),
            icon_url=data.get('icon_url', None),
            description=data.get('description'),
            title=data.get('title', ''),
            categories=data.get('categories', []),
            client_side=data.get('client_side'),
            server_side=data.get('server_side'),
            body=md(body),
            gallery=data.get('gallery', []),
            slug=data.get('slug', '')
        )
    
    async def get_project_versions(self, slug: str) -> List[Dict[str, Any]]:
        """
        Obtiene las versiones de un proyecto específico.
        
        Args:
            slug: Identificador del proyecto
            
        Returns:
            Lista de versiones o lista vacía si hay error
        """
        url = f"{self.BASE_URL}/project/{slug}/version?version_type=release"
        data = await self._make_request(url)
        
        return data.get('data', []) if data else []
    
    async def search_projects(
        self,
        project_type: Union[str, ProjectType] = ProjectType.MOD,
        query: str = "",
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
        loader: Optional[str] = None
    ) -> tuple[List[ModrinthProject], int]:
        """
        Busca proyectos en Modrinth con filtros avanzados.
        
        Args:
            project_type: Tipo de proyecto (mod, modpack, etc.)
            query: Término de búsqueda
            limit: Número máximo de resultados (1-100)
            offset: Offset para paginación
            loader: Loader específico (solo para mods)
            
        Returns:
            Tuple con (lista de proyectos, total de resultados)
        """
        # Validar parámetros
        if isinstance(project_type, str):
            project_type = ProjectType(project_type)
            
        limit = max(self.MIN_LIMIT, min(limit, self.MAX_LIMIT))
        
        # Preparar facets
        facets = [[f"project_type:{project_type.value}"]]
        if loader and project_type == ProjectType.MOD:
            facets.append([f"categories:{loader.lower()}"])
        
        params = {
            "query": query.strip(),
            "limit": limit,
            "offset": offset,
            "facets": json.dumps(facets),
        }
        
        url = f"{self.BASE_URL}/search"
        data = await self._make_request(url, params=params)
        
        if not data:
            return [], 0
        
        # Procesar resultados
        projects_data = data.get("hits", [])
        total_hits = data.get("total_hits", 0)
        
        projects = [
            ModrinthProject(
                name=proj["title"],
                slug=proj["slug"],
                imgs=proj.get("gallery", []),
                icon=proj.get("icon_url", "iconos/no_found_image.png"),
                description=(proj.get("description", "")[:100] + "...") 
                    if len(proj.get("description", "")) > 100 else proj.get("description", "")
            )
            for proj in projects_data
        ]
        
        # Cachear resultados si se proporcionó page
        if limit > 1:
            try:
                cache = [proj.slug for proj in projects]
                self.page.temp_config_modrinth["list_mods_cache"] = cache
                self.page.temp_config_modrinth["mods_index"] = {p: i for i, p in enumerate(cache)}
                
                self.page.temp_config_modrinth["total_mods_result"] = total_hits
            except AttributeError:
                pass  # Ignorar si no existe el atributo
        
        return projects, total_hits
    
    async def batch_get_details(self, slugs: List[str], max_concurrent: int = 5) -> Dict[str, ModrinthVersionInfo]:
        """
        Obtiene detalles de múltiples proyectos de forma concurrente.
        
        Args:
            slugs: Lista de slugs de proyectos
            max_concurrent: Máximo número de requests concurrentes
            
        Returns:
            Diccionario con slug -> información del proyecto
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_with_semaphore(slug: str) -> tuple[str, ModrinthVersionInfo]:
            async with semaphore:
                return slug, await self.get_project_details(slug)
        
        tasks = [fetch_with_semaphore(slug) for slug in slugs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            slug: info if isinstance(info, ModrinthVersionInfo) else 
            ModrinthVersionInfo(
                stable_versions=[], loaders=[], icon_url="iconos/no_found_image.png",
                description=None, title=slug, categories=[], 
                client_side=None, server_side=None, body=[], gallery=[]
            )
            for slug, info in results
        }