"""
Modelos de datos - Validación con Pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class EntityType(str, Enum):
    """Tipos de entidades en la ontología"""
    ARTIST = "artist"
    ALBUM = "album"
    SONG = "song"
    INSTRUMENT = "instrument"
    GENRE = "genre"


class Artist(BaseModel):
    """Modelo de Artista"""
    uri: str
    name: str
    type: str = "artist"
    description: Optional[str] = None
    genre: Optional[str] = None


class Album(BaseModel):
    """Modelo de Álbum"""
    uri: str
    name: str
    type: str = "album"
    description: Optional[str] = None
    releaseYear: Optional[int] = None
    genre: Optional[str] = None


class Instrument(BaseModel):
    """Modelo de Instrumento"""
    uri: str
    name: str
    type: Optional[str] = None
    description: Optional[str] = None


class Song(BaseModel):
    """Modelo de Canción"""
    uri: str
    name: str
    type: str = "song"
    description: Optional[str] = None
    duration: Optional[int] = None
    releaseYear: Optional[int] = None
    artist: Optional[str] = None
    instruments: Optional[List[Instrument]] = None


class Genre(BaseModel):
    """Modelo de Género"""
    uri: str
    name: str
    type: str = "genre"
    description: Optional[str] = None


class SearchResult(BaseModel):
    """Resultado de búsqueda"""
    type: EntityType
    data: dict = Field(..., description="Datos de la entidad")


class ApiResponse(BaseModel):
    """Respuesta genérica de API"""
    success: bool
    data: dict | list
    error: Optional[str] = None
    message: Optional[str] = None


class SearchQuery(BaseModel):
    """Consulta de búsqueda"""
    query: str = Field(..., min_length=1)
    filter_type: Optional[EntityType] = None


class OntologyStats(BaseModel):
    """Estadísticas de la ontología"""
    total_triples: int
    artists: int
    albums: int
    songs: int
    instruments: int
    genres: int
