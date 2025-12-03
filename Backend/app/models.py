"""
Modelos de datos - Validación con Pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class EntityType(str, Enum):
    """Tipos de entidades en la ontología"""
    ARTIST = "artist"
    ALBUM = "album"
    SONG = "song"
    INSTRUMENT = "instrument"
    GENRE = "genre"


class SearchMode(str, Enum):
    """Modos de búsqueda disponibles"""
    OFFLINE = "offline"  # Búsqueda local + datos descargados de DBpedia
    ONLINE = "online"    # Solo consultas en vivo a DBpedia


class DataSource(str, Enum):
    """Fuente de los datos"""
    LOCAL = "local"  # Ontología local
    DBPEDIA_DOWNLOADED = "dbpedia_downloaded"  # Datos descargados de DBpedia a la ontología
    DBPEDIA_LIVE = "dbpedia_live"  # Consulta en vivo a DBpedia


class Artist(BaseModel):
    """Modelo de Artista"""
    uri: str
    name: str
    type: str = "artist"
    description: Optional[str] = None
    genre: Optional[str] = None
    dbpediaUrl: Optional[str] = None  # URL de DBpedia según idioma


class Album(BaseModel):
    """Modelo de Álbum"""
    uri: str
    name: str
    type: str = "album"
    description: Optional[str] = None
    releaseYear: Optional[int] = None
    genre: Optional[str] = None
    dbpediaUrl: Optional[str] = None  # URL de DBpedia según idioma


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
    dbpediaUrl: Optional[str] = None  # URL de DBpedia según idioma


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
    source: DataSource = DataSource.LOCAL  # Nuevo campo para indicar fuente


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


class EnrichmentRequest(BaseModel):
    """Solicitud de enriquecimiento desde DBpedia"""
    entity_type: EntityType
    name: str
    artist: Optional[str] = None  # Para álbumes y canciones
    fetch_albums: bool = True  # Para artistas


class EnrichmentResponse(BaseModel):
    """Respuesta de enriquecimiento"""
    success: bool
    message: str
    entities_added: int = 0
    triples_added: int = 0
    errors: List[str] = []


class BatchEnrichmentRequest(BaseModel):
    """Solicitud de enriquecimiento en lote"""
    entities: List[Dict[str, str]]  # [{type, name, artist}, ...]


class EnrichmentStats(BaseModel):
    """Estadísticas de enriquecimiento"""
    artists_added: int
    albums_added: int
    songs_added: int
    total_triples_added: int
    total_triples: int
    artists_in_ontology: int
    albums_in_ontology: int
    songs_in_ontology: int
    last_enrichment: Optional[str] = None
