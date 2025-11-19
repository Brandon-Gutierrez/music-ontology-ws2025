"""
Routers - Endpoints de la API REST
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import ApiResponse, SearchResult, OntologyStats
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
def search(q: str = Query(..., min_length=1)) -> ApiResponse:
    """
    Búsqueda general en toda la ontología
    
    Query Parameters:
        q: Término de búsqueda (requerido)
    """
    try:
        results = ontology_service.search(q)
        return ApiResponse(
            success=True,
            data=results,
            message=f"Se encontraron {len(results)} resultados"
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
