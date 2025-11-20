import ujson as json
import zipfile
import asyncio
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(slots=True)
class File:
    direct_links: List[str]
    path: str
    required_client: bool
    required_server: bool
    size_bytes: int
    hashes: Dict[str, str]


@dataclass(slots=True)
class MrPackResult:
    name: str
    files: List[File]
    format_version: int
    summary: str
    version_id: str
    dependencies: Dict[str, Any]


class MrPack:
    """Parser asíncrono para archivos .mrpack de Modrinth"""

    @staticmethod
    async def get_information(path: Path) -> MrPackResult:
        """Lee el archivo .mrpack sin bloquear la interfaz (async compatible)"""
        # Mueve la lectura pesada a otro hilo
        index = await asyncio.to_thread(MrPack._read_index, path)
        return MrPack._parse_index(index)

    @staticmethod
    def _read_index(path: Path) -> dict:
        """Función interna: abre el .mrpack y lee el JSON (bloqueante, pero en otro hilo)"""
        with zipfile.ZipFile(path) as zf, zf.open("modrinth.index.json") as f:
            return json.loads(f.read())

    @staticmethod
    def _parse_index(index: dict) -> MrPackResult:
        """Transforma los datos en objetos dataclass"""
        files = [
            File(
                direct_links=file["downloads"],
                path=file["path"],
                size_bytes=file["fileSize"],
                required_client=file["env"]["client"] != "optional",
                required_server=file["env"]["server"] != "optional",
                hashes=file["hashes"],
            )
            for file in index["files"]
        ]

        return MrPackResult(
            name=index["name"],
            summary=index.get("summary", ""),
            format_version=index["formatVersion"],
            version_id=index["versionId"],
            dependencies=index.get("dependencies", {}),
            files=files,
        )


# Ejemplo de uso asíncrono
async def main():
    pck = await MrPack.get_information(
        Path(r"C:\Users\pc\Downloads\Sodium Plus 2.3.3 - alpha.2.mrpack")
    )
    print(pck)


if __name__ == "__main__":
    asyncio.run(main())
