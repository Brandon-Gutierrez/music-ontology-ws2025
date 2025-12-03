"""
Routers - Endpoints de la API REST
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import (
    ApiResponse, SearchResult, OntologyStats, 
    SearchMode, EnrichmentRequest, EnrichmentResponse,
    BatchEnrichmentRequest, EnrichmentStats
)
from app.ontology import OntologyService
import os

# Inicializar router
router = APIRouter(prefix="/api", tags=["Search"])

# Inicializar servicio de ontología
ontology_path = os.path.join(
    os.path.dirname(__file__), 
    "..", 
    "data", 
    "music-ontology.owl"
)
ontology_service = OntologyService(ontology_path)


# ==================== BÚSQUEDA GENERAL ====================

@router.get("/search")
def search(
    q: str = Query(..., min_length=1),
    mode: SearchMode = Query(SearchMode.OFFLINE, description="Modo de búsqueda: offline u online"),
    lang: str = Query("en", description="Idioma para búsquedas DBpedia (en, es, fr, de)")
) -> ApiResponse:
    """
    Búsqueda general en toda la ontología con soporte para múltiples modos y idiomas
    
    Query Parameters:
        q: Término de búsqueda (requerido)
        mode: Modo de búsqueda (offline=local+descargado, online=DBpedia en vivo)
        lang: Idioma para consultas DBpedia (solo modo online)
    """
    try:
        results = ontology_service.search_with_mode(q, mode.value, lang)
        
        # Contar fuentes
        sources = {"local": 0, "dbpedia_downloaded": 0, "dbpedia_live": 0}
        for result in results:
            # El source ahora puede venir en result directamente o en result['source']
            if isinstance(result, dict):
                source = result.get("source", "local")
            else:
                source = getattr(result, "source", "local")
            sources[source] = sources.get(source, 0) + 1
        
        message = f"Se encontraron {len(results)} resultados"
        if mode == SearchMode.OFFLINE:
            message += f" ({sources['local']} locales, {sources['dbpedia_downloaded']} descargados)"
        elif mode == SearchMode.ONLINE:
            message += f" de DBpedia ({lang})"
        
        return ApiResponse(
            success=True,
            data=results,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ARTISTAS ====================

@router.get("/artists")
def get_artists() -> ApiResponse:
    """Obtener todos los artistas"""
    try:
        artists = ontology_service.get_all_artists()
        return ApiResponse(
            success=True,
            data=artists,
            message=f"Se encontraron {len(artists)} artistas"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artists/{artist_id}")
def get_artist(artist_id: str) -> ApiResponse:
    """Obtener un artista específico por ID"""
    try:
        artists = ontology_service.get_all_artists()
        for artist in artists:
            if artist_id in artist["data"]["uri"]:
                return ApiResponse(
                    success=True,
                    data=artist["data"]
                )
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ÁLBUMES ====================

@router.get("/albums")
def get_albums() -> ApiResponse:
    """Obtener todos los álbumes"""
    try:
        albums = ontology_service.get_all_albums()
        return ApiResponse(
            success=True,
            data=albums,
            message=f"Se encontraron {len(albums)} álbumes"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/albums/{album_id}")
def get_album(album_id: str) -> ApiResponse:
    """Obtener un álbum específico"""
    try:
        albums = ontology_service.get_all_albums()
        for album in albums:
            if album_id in album["data"]["uri"]:
                return ApiResponse(
                    success=True,
                    data=album["data"]
                )
        raise HTTPException(status_code=404, detail="Álbum no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/albums/artist/{artist_id}")
def get_albums_by_artist(artist_id: str) -> ApiResponse:
    """Obtener álbumes de un artista específico"""
    try:
        albums = ontology_service.get_albums_by_artist(artist_id)
        return ApiResponse(
            success=True,
            data=albums,
            message=f"Se encontraron {len(albums)} álbumes"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CANCIONES ====================

@router.get("/songs")
def get_songs() -> ApiResponse:
    """Obtener todas las canciones"""
    try:
        songs = ontology_service.get_all_songs()
        return ApiResponse(
            success=True,
            data=songs,
            message=f"Se encontraron {len(songs)} canciones"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/{song_id}")
def get_song(song_id: str) -> ApiResponse:
    """Obtener una canción específica"""
    try:
        songs = ontology_service.get_all_songs()
        for song in songs:
            if song_id in song["data"]["uri"]:
                return ApiResponse(
                    success=True,
                    data=song["data"]
                )
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/album/{album_id}")
def get_songs_by_album(album_id: str) -> ApiResponse:
    """Obtener canciones de un álbum"""
    try:
        songs = ontology_service.get_songs_by_album(album_id)
        return ApiResponse(
            success=True,
            data=songs,
            message=f"Se encontraron {len(songs)} canciones"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/artist/{artist_id}")
def get_songs_by_artist(artist_id: str) -> ApiResponse:
    """Obtener todas las canciones de un artista"""
    try:
        songs = ontology_service.get_songs_by_artist(artist_id)
        return ApiResponse(
            success=True,
            data=songs,
            message=f"Se encontraron {len(songs)} canciones"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/songs/instrument/{instrument_id}")
def get_songs_by_instrument(instrument_id: str) -> ApiResponse:
    """Obtener canciones que utilizan un instrumento"""
    try:
        songs = ontology_service.get_songs_by_instrument(instrument_id)
        return ApiResponse(
            success=True,
            data=songs,
            message=f"Se encontraron {len(songs)} canciones"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== INSTRUMENTOS ====================

@router.get("/instruments")
def get_instruments() -> ApiResponse:
    """Obtener todos los instrumentos"""
    try:
        instruments = ontology_service.get_all_instruments()
        return ApiResponse(
            success=True,
            data=instruments,
            message=f"Se encontraron {len(instruments)} instrumentos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instruments/{instrument_id}")
def get_instrument(instrument_id: str) -> ApiResponse:
    """Obtener un instrumento específico"""
    try:
        instruments = ontology_service.get_all_instruments()
        for instrument in instruments:
            if instrument_id in instrument["data"]["uri"]:
                return ApiResponse(
                    success=True,
                    data=instrument["data"]
                )
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instruments/type/{instrument_type}")
def get_instruments_by_type(instrument_type: str) -> ApiResponse:
    """Obtener instrumentos por tipo"""
    try:
        instruments = ontology_service.get_instruments_by_type(instrument_type)
        return ApiResponse(
            success=True,
            data=instruments,
            message=f"Se encontraron {len(instruments)} instrumentos"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== GÉNEROS ====================

@router.get("/genres")
def get_genres() -> ApiResponse:
    """Obtener todos los géneros"""
    try:
        genres = ontology_service.get_all_genres()
        return ApiResponse(
            success=True,
            data=genres,
            message=f"Se encontraron {len(genres)} géneros"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genres/artist/{artist_id}")
def get_genres_by_artist(artist_id: str) -> ApiResponse:
    """Obtener géneros de un artista"""
    try:
        genres = ontology_service.get_genres_by_artist(artist_id)
        return ApiResponse(
            success=True,
            data=genres,
            message=f"Se encontraron {len(genres)} géneros"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ESTADÍSTICAS ====================

@router.get("/stats")
def get_stats() -> ApiResponse:
    """Obtener estadísticas de la ontología"""
    try:
        stats = ontology_service.get_ontology_stats()
        return ApiResponse(
            success=True,
            data=stats,
            message="Estadísticas de la ontología"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ENRIQUECIMIENTO DESDE DBPEDIA ====================

# Inicializar servicio de enriquecimiento (lazy loading)
enrichment_service = None

def get_enrichment_service():
    """Obtener servicio de enriquecimiento (lazy loading)"""
    global enrichment_service
    if enrichment_service is None:
        from app.enrichment import OntologyEnrichment
        enrichment_service = OntologyEnrichment(ontology_path)
    return enrichment_service


@router.post("/enrich", response_model=EnrichmentResponse)
def enrich_entity(request: EnrichmentRequest) -> EnrichmentResponse:
    """
    Enriquecer la ontología con una entidad desde DBpedia
    
    Body:
        entity_type: Tipo de entidad (artist, album, song)
        name: Nombre de la entidad
        artist: Nombre del artista (opcional, para álbumes y canciones)
        fetch_albums: Si obtener álbumes también (solo para artistas)
    """
    try:
        service = get_enrichment_service()
        
        if request.entity_type == "artist":
            result = service.enrich_artist(request.name, request.fetch_albums)
        elif request.entity_type == "album":
            result = service.enrich_album(request.name, request.artist)
        elif request.entity_type == "song":
            result = service.enrich_song(request.name, request.artist)
        else:
            return EnrichmentResponse(
                success=False,
                message=f"Tipo de entidad desconocido: {request.entity_type}",
                errors=[f"Tipo válidos: artist, album, song"]
            )
        
        # Guardar si fue exitoso
        if result["success"]:
            service.save_enriched_ontology()
            # Recargar ontología en el servicio principal
            ontology_service.reload_ontology()
        
        return EnrichmentResponse(**result)
        
    except Exception as e:
        return EnrichmentResponse(
            success=False,
            message=f"Error al enriquecer: {str(e)}",
            errors=[str(e)]
        )


@router.post("/enrich/batch", response_model=EnrichmentResponse)
def enrich_batch(request: BatchEnrichmentRequest) -> EnrichmentResponse:
    """
    Enriquecer la ontología con múltiples entidades en lote
    
    Body:
        entities: Lista de entidades [{type, name, artist}, ...]
    """
    try:
        service = get_enrichment_service()
        result = service.enrich_batch(request.entities)
        
        # Guardar si hubo al menos una entidad exitosa
        if result["successful"] > 0:
            service.save_enriched_ontology()
            ontology_service.reload_ontology()
        
        return EnrichmentResponse(
            success=result["successful"] > 0,
            message=f"Procesadas {result['total_entities']} entidades: {result['successful']} exitosas, {result['failed']} fallidas",
            entities_added=result["successful"],
            errors=result["errors"]
        )
        
    except Exception as e:
        return EnrichmentResponse(
            success=False,
            message=f"Error en enriquecimiento por lotes: {str(e)}",
            errors=[str(e)]
        )


@router.get("/enrich/stats", response_model=EnrichmentStats)
def get_enrichment_stats() -> EnrichmentStats:
    """Obtener estadísticas de enriquecimiento"""
    try:
        service = get_enrichment_service()
        stats = service.get_enrichment_stats()
        return EnrichmentStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enrich/reload")
def reload_ontology() -> ApiResponse:
    """Recargar la ontología desde el archivo (útil después de enriquecer manualmente)"""
    try:
        ontology_service.reload_ontology()
        stats = ontology_service.get_ontology_stats()
        return ApiResponse(
            success=True,
            data=stats,
            message=f"Ontología recargada: {stats['total_triples']} triplas"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

