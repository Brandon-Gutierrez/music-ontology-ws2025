"""
Módulo de ontología - Carga y consulta de la ontología RDF/OWL
"""

import os
from rdflib import Graph, Namespace, RDF, RDFS, Literal
from typing import List, Dict, Any, Optional, Tuple

class OntologyService:
    """Servicio para consultar la ontología de música"""
    
    def __init__(self, ontology_path: str):
        """
        Inicializar el servicio de ontología
        
        Args:
            ontology_path: Ruta al archivo OWL
        """
        self.graph = Graph()
        self.ontology_path = ontology_path
        self.MUSIC = Namespace("http://example.org/music-ontology#")
        self.RDF = RDF
        self.RDFS = RDFS
        
        # Cargar ontología
        self._load_ontology()
    
    def _load_ontology(self):
        """Cargar la ontología desde archivo"""
        if not os.path.exists(self.ontology_path):
            raise FileNotFoundError(f"Ontología no encontrada: {self.ontology_path}")
        
        try:
            self.graph.parse(self.ontology_path, format='xml')
            print(f"✓ Ontología cargada: {len(self.graph)} triplas")
        except Exception as e:
            raise Exception(f"Error al cargar ontología: {str(e)}")
    
    def _entity_to_dict(self, uri: str, entity_type: str) -> Dict[str, Any]:
        """Convertir entidad RDF a diccionario"""
        name = self.graph.value(uri, self.MUSIC.name)
        description = self.graph.value(uri, self.MUSIC.description)
        
        entity = {
            "uri": str(uri),
            "name": str(name) if name else "Sin nombre",
            "type": entity_type
        }
        
        if description:
            entity["description"] = str(description)
        
        # Propiedades específicas por tipo
        if entity_type == "artist":
            # Propiedades nuevas
            nationality = self.graph.value(uri, self.MUSIC.nationality)
            if nationality:
                entity["nationality"] = str(nationality)
            
            birthYear = self.graph.value(uri, self.MUSIC.birthYear)
            if birthYear:
                entity["birthYear"] = int(birthYear)
            
            activeYears = self.graph.value(uri, self.MUSIC.activeYears)
            if activeYears:
                entity["activeYears"] = str(activeYears)
            
            trajectory = self.graph.value(uri, self.MUSIC.trajectory)
            if trajectory:
                entity["trajectory"] = str(trajectory)
            
            discography = self.graph.value(uri, self.MUSIC.discography)
            if discography:
                entity["discography"] = str(discography)
            
            awards = self.graph.value(uri, self.MUSIC.awards)
            if awards:
                entity["awards"] = str(awards)
            
            # Género
            genre = self.graph.value(uri, self.MUSIC.performsGenre)
            if genre:
                genre_name = self.graph.value(genre, self.MUSIC.name)
                entity["genre"] = str(genre_name) if genre_name else None
        
        elif entity_type == "album":
            year = self.graph.value(uri, self.MUSIC.releaseYear)
            if year:
                entity["releaseYear"] = int(year)
            genre = self.graph.value(uri, self.MUSIC.hasGenre)
            if genre:
                genre_name = self.graph.value(genre, self.MUSIC.name)
                entity["genre"] = str(genre_name) if genre_name else None
        
        elif entity_type == "song":
            duration = self.graph.value(uri, self.MUSIC.duration)
            if duration:
                entity["duration"] = int(duration)
            year = self.graph.value(uri, self.MUSIC.releaseYear)
            if year:
                entity["releaseYear"] = int(year)
            artist = self.graph.value(uri, self.MUSIC.performedBy)
            if artist:
                artist_name = self.graph.value(artist, self.MUSIC.name)
                entity["artist"] = str(artist_name) if artist_name else None
            
            # Propiedades nuevas de canción
            language = self.graph.value(uri, self.MUSIC.language)
            if language:
                entity["language"] = str(language)
            
            composers = self.graph.value(uri, self.MUSIC.composers)
            if composers:
                entity["composers"] = str(composers)
            
            lyrics = self.graph.value(uri, self.MUSIC.lyrics)
            if lyrics:
                entity["lyrics"] = str(lyrics)
            
            lyricist = self.graph.value(uri, self.MUSIC.lyricist)
            if lyricist:
                entity["lyricist"] = str(lyricist)
            
            # Instrumentos
            instruments = []
            for instr in self.graph.objects(uri, self.MUSIC.usesInstrument):
                instr_name = self.graph.value(instr, self.MUSIC.name)
                instruments.append({
                    "uri": str(instr),
                    "name": str(instr_name) if instr_name else "Sin nombre"
                })
            if instruments:
                entity["instruments"] = instruments
        
        elif entity_type == "instrument":
            instr_type = self.graph.value(uri, self.MUSIC.type)
            if instr_type:
                entity["type"] = str(instr_type)
        
        return entity
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Búsqueda general en la ontología
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Lista de resultados
        """
        query_lower = query.lower()
        results = []
        
        # Buscar artistas
        for artist in self.graph.subjects(self.RDF.type, self.MUSIC.Artist):
            name = self.graph.value(artist, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                results.append({
                    "type": "artist",
                    "data": self._entity_to_dict(artist, "artist")
                })
        
        # Buscar álbumes
        for album in self.graph.subjects(self.RDF.type, self.MUSIC.Album):
            name = self.graph.value(album, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                results.append({
                    "type": "album",
                    "data": self._entity_to_dict(album, "album")
                })
        
        # Buscar canciones
        for song in self.graph.subjects(self.RDF.type, self.MUSIC.Song):
            name = self.graph.value(song, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                results.append({
                    "type": "song",
                    "data": self._entity_to_dict(song, "song")
                })
        
        # Buscar instrumentos
        for instrument in self.graph.subjects(self.RDF.type, self.MUSIC.Instrument):
            name = self.graph.value(instrument, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                results.append({
                    "type": "instrument",
                    "data": self._entity_to_dict(instrument, "instrument")
                })
        
        # Buscar géneros
        for genre in self.graph.subjects(self.RDF.type, self.MUSIC.Genre):
            name = self.graph.value(genre, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                results.append({
                    "type": "genre",
                    "data": self._entity_to_dict(genre, "genre")
                })
        
        return results
    
    def get_all_artists(self) -> List[Dict[str, Any]]:
        """Obtener todos los artistas"""
        artists = []
        for artist in self.graph.subjects(self.RDF.type, self.MUSIC.Artist):
            artists.append({
                "type": "artist",
                "data": self._entity_to_dict(artist, "artist")
            })
        return artists
    
    def get_all_albums(self) -> List[Dict[str, Any]]:
        """Obtener todos los álbumes"""
        albums = []
        for album in self.graph.subjects(self.RDF.type, self.MUSIC.Album):
            albums.append({
                "type": "album",
                "data": self._entity_to_dict(album, "album")
            })
        return albums
    
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """Obtener todas las canciones"""
        songs = []
        for song in self.graph.subjects(self.RDF.type, self.MUSIC.Song):
            songs.append({
                "type": "song",
                "data": self._entity_to_dict(song, "song")
            })
        return songs
    
    def get_all_instruments(self) -> List[Dict[str, Any]]:
        """Obtener todos los instrumentos"""
        instruments = []
        for instrument in self.graph.subjects(self.RDF.type, self.MUSIC.Instrument):
            instruments.append({
                "type": "instrument",
                "data": self._entity_to_dict(instrument, "instrument")
            })
        return instruments
    
    def get_all_genres(self) -> List[Dict[str, Any]]:
        """Obtener todos los géneros"""
        genres = []
        for genre in self.graph.subjects(self.RDF.type, self.MUSIC.Genre):
            genres.append({
                "type": "genre",
                "data": self._entity_to_dict(genre, "genre")
            })
        return genres
    
    def get_albums_by_artist(self, artist_uri: str) -> List[Dict[str, Any]]:
        """Obtener álbumes de un artista"""
        artist_iri = self.MUSIC[artist_uri.split('#')[-1]] if '#' not in artist_uri else artist_uri
        albums = []
        
        for album in self.graph.objects(artist_iri, self.MUSIC.hasAlbum):
            albums.append({
                "type": "album",
                "data": self._entity_to_dict(album, "album")
            })
        return albums
    
    def get_songs_by_album(self, album_uri: str) -> List[Dict[str, Any]]:
        """Obtener canciones de un álbum"""
        album_iri = self.MUSIC[album_uri.split('#')[-1]] if '#' not in album_uri else album_uri
        songs = []
        
        for song in self.graph.objects(album_iri, self.MUSIC.containsSong):
            songs.append({
                "type": "song",
                "data": self._entity_to_dict(song, "song")
            })
        return songs
    
    def get_songs_by_artist(self, artist_uri: str) -> List[Dict[str, Any]]:
        """Obtener todas las canciones de un artista"""
        artist_iri = self.MUSIC[artist_uri.split('#')[-1]] if '#' not in artist_uri else artist_uri
        songs = []
        
        # Obtener albums del artista
        for album in self.graph.objects(artist_iri, self.MUSIC.hasAlbum):
            # Obtener canciones del album
            for song in self.graph.objects(album, self.MUSIC.containsSong):
                songs.append({
                    "type": "song",
                    "data": self._entity_to_dict(song, "song")
                })
        return songs
    
    def get_songs_by_instrument(self, instrument_uri: str) -> List[Dict[str, Any]]:
        """Obtener canciones que usan un instrumento"""
        instrument_iri = self.MUSIC[instrument_uri.split('#')[-1]] if '#' not in instrument_uri else instrument_uri
        songs = []
        
        for song in self.graph.subjects(self.MUSIC.usesInstrument, instrument_iri):
            songs.append({
                "type": "song",
                "data": self._entity_to_dict(song, "song")
            })
        return songs
    
    def get_instruments_by_type(self, instr_type: str) -> List[Dict[str, Any]]:
        """Obtener instrumentos por tipo"""
        instruments = []
        type_lower = instr_type.lower()
        
        for instrument in self.graph.subjects(self.RDF.type, self.MUSIC.Instrument):
            instr_type_node = self.graph.value(instrument, self.MUSIC.type)
            if instr_type_node and type_lower in str(instr_type_node).lower():
                instruments.append({
                    "type": "instrument",
                    "data": self._entity_to_dict(instrument, "instrument")
                })
        return instruments
    
    def get_genres_by_artist(self, artist_uri: str) -> List[Dict[str, Any]]:
        """Obtener géneros de un artista"""
        artist_iri = self.MUSIC[artist_uri.split('#')[-1]] if '#' not in artist_uri else artist_uri
        genres = []
        
        for genre in self.graph.objects(artist_iri, self.MUSIC.performsGenre):
            genres.append({
                "type": "genre",
                "data": self._entity_to_dict(genre, "genre")
            })
        return genres
    
    def get_ontology_stats(self) -> Dict[str, int]:
        """Obtener estadísticas de la ontología"""
        return {
            "total_triples": len(self.graph),
            "artists": len(list(self.graph.subjects(self.RDF.type, self.MUSIC.Artist))),
            "albums": len(list(self.graph.subjects(self.RDF.type, self.MUSIC.Album))),
            "songs": len(list(self.graph.subjects(self.RDF.type, self.MUSIC.Song))),
            "instruments": len(list(self.graph.subjects(self.RDF.type, self.MUSIC.Instrument))),
            "genres": len(list(self.graph.subjects(self.RDF.type, self.MUSIC.Genre)))
        }
