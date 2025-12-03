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
            ontology_path: Ruta al archivo OWL principal
        """
        # Grafo para la ontología local
        self.local_graph = Graph()
        # Grafo para datos descargados de DBpedia
        self.downloaded_graph = Graph()
        
        self.ontology_path = ontology_path
        self.downloaded_path = os.path.join(
            os.path.dirname(ontology_path),
            "dbpedia-downloaded.owl"
        )
        
        self.MUSIC = Namespace("http://example.org/music-ontology#")
        self.RDF = RDF
        self.RDFS = RDFS
        
        # Inicializar servicio DBpedia (lazy loading para evitar errores si no se usa)
        self._dbpedia_service = None
        
        # Cargar ontologías
        self._load_ontology()
    
    def _load_ontology(self):
        """Cargar las ontologías desde archivos"""
        # Cargar ontología local
        if not os.path.exists(self.ontology_path):
            raise FileNotFoundError(f"Ontología no encontrada: {self.ontology_path}")
        
        try:
            self.local_graph.parse(self.ontology_path, format='xml')
            print(f"✓ Ontología local cargada: {len(self.local_graph)} triplas")
        except Exception as e:
            raise Exception(f"Error al cargar ontología local: {str(e)}")
        
        # Cargar datos descargados de DBpedia si existen
        if os.path.exists(self.downloaded_path):
            try:
                self.downloaded_graph.parse(self.downloaded_path, format='xml')
                print(f"✓ Datos descargados de DBpedia: {len(self.downloaded_graph)} triplas")
            except Exception as e:
                print(f"⚠ No se pudieron cargar datos descargados: {str(e)}")
    
    def _entity_to_dict(self, uri: str, entity_type: str) -> Dict[str, Any]:
        """Convertir entidad RDF a diccionario"""
        name = self.graph.value(uri, self.MUSIC.name)
        description = self.graph.value(uri, self.MUSIC.description)
        
        # Detectar fuente de datos
        data_source = self.graph.value(uri, self.MUSIC.dataSource)
        source = str(data_source) if data_source else "local"
        
        entity = {
            "uri": str(uri),
            "name": str(name) if name else "Sin nombre",
            "type": entity_type,
            "source": source  # local o dbpedia_downloaded
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
        Búsqueda general en ambas ontologías (local y descargada)
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Lista de resultados de ambas fuentes
        """
        query_lower = query.lower()
        results = []
        
        # Buscar en ontología LOCAL
        # Buscar artistas locales
        for artist in self.local_graph.subjects(self.RDF.type, self.MUSIC.Artist):
            name = self.local_graph.value(artist, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(artist, "artist", self.local_graph, "local")
                results.append({
                    "type": "artist",
                    "data": entity_dict
                })
        
        # Buscar álbumes locales
        for album in self.local_graph.subjects(self.RDF.type, self.MUSIC.Album):
            name = self.local_graph.value(album, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(album, "album", self.local_graph, "local")
                results.append({
                    "type": "album",
                    "data": entity_dict
                })
        
        # Buscar canciones locales
        for song in self.local_graph.subjects(self.RDF.type, self.MUSIC.Song):
            name = self.local_graph.value(song, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(song, "song", self.local_graph, "local")
                results.append({
                    "type": "song",
                    "data": entity_dict
                })
        
        # Buscar instrumentos locales
        for instrument in self.local_graph.subjects(self.RDF.type, self.MUSIC.Instrument):
            name = self.local_graph.value(instrument, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(instrument, "instrument", self.local_graph, "local")
                results.append({
                    "type": "instrument",
                    "data": entity_dict
                })
        
        # Buscar géneros locales
        for genre in self.local_graph.subjects(self.RDF.type, self.MUSIC.Genre):
            name = self.local_graph.value(genre, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(genre, "genre", self.local_graph, "local")
                results.append({
                    "type": "genre",
                    "data": entity_dict
                })
        
        # Buscar en datos DESCARGADOS de DBpedia
        # Buscar artistas descargados
        for artist in self.downloaded_graph.subjects(self.RDF.type, self.MUSIC.Artist):
            name = self.downloaded_graph.value(artist, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(artist, "artist", self.downloaded_graph, "dbpedia_downloaded")
                results.append({
                    "type": "artist",
                    "data": entity_dict
                })
        
        # Buscar álbumes descargados
        for album in self.downloaded_graph.subjects(self.RDF.type, self.MUSIC.Album):
            name = self.downloaded_graph.value(album, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(album, "album", self.downloaded_graph, "dbpedia_downloaded")
                results.append({
                    "type": "album",
                    "data": entity_dict
                })
        
        # Buscar canciones descargadas
        for song in self.downloaded_graph.subjects(self.RDF.type, self.MUSIC.Song):
            name = self.downloaded_graph.value(song, self.MUSIC.name)
            if name and query_lower in str(name).lower():
                entity_dict = self._entity_to_dict_from_graph(song, "song", self.downloaded_graph, "dbpedia_downloaded")
                results.append({
                    "type": "song",
                    "data": entity_dict
                })
        
        return results
    
    def _entity_to_dict_from_graph(self, uri: str, entity_type: str, graph: Graph, source: str) -> Dict[str, Any]:
        """Convertir entidad RDF a diccionario desde un grafo específico"""
        name = graph.value(uri, self.MUSIC.name)
        description = graph.value(uri, self.MUSIC.description)
        
        entity = {
            "uri": str(uri),
            "name": str(name) if name else "Sin nombre",
            "type": entity_type,
            "source": source  # "local" o "dbpedia_downloaded"
        }
        
        if description:
            entity["description"] = str(description)
        
        # Propiedades específicas por tipo
        if entity_type == "artist":
            nationality = graph.value(uri, self.MUSIC.nationality)
            if nationality:
                entity["nationality"] = str(nationality)
            
            birthYear = graph.value(uri, self.MUSIC.birthYear)
            if birthYear:
                entity["birthYear"] = int(birthYear)
            
            activeYears = graph.value(uri, self.MUSIC.activeYears)
            if activeYears:
                entity["activeYears"] = str(activeYears)
            
            trajectory = graph.value(uri, self.MUSIC.trajectory)
            if trajectory:
                entity["trajectory"] = str(trajectory)
            
            discography = graph.value(uri, self.MUSIC.discography)
            if discography:
                entity["discography"] = str(discography)
            
            awards = graph.value(uri, self.MUSIC.awards)
            if awards:
                entity["awards"] = str(awards)
            
            genre = graph.value(uri, self.MUSIC.performsGenre)
            if genre:
                genre_name = graph.value(genre, self.MUSIC.name)
                entity["genre"] = str(genre_name) if genre_name else None
        
        elif entity_type == "album":
            year = graph.value(uri, self.MUSIC.releaseYear)
            if year:
                entity["releaseYear"] = int(year)
            genre = graph.value(uri, self.MUSIC.hasGenre)
            if genre:
                genre_name = graph.value(genre, self.MUSIC.name)
                entity["genre"] = str(genre_name) if genre_name else None
        
        elif entity_type == "song":
            duration = graph.value(uri, self.MUSIC.duration)
            if duration:
                entity["duration"] = int(duration)
            year = graph.value(uri, self.MUSIC.releaseYear)
            if year:
                entity["releaseYear"] = int(year)
            artist = graph.value(uri, self.MUSIC.performedBy)
            if artist:
                artist_name = graph.value(artist, self.MUSIC.name)
                entity["artist"] = str(artist_name) if artist_name else None
            
            language = graph.value(uri, self.MUSIC.language)
            if language:
                entity["language"] = str(language)
            
            composers = graph.value(uri, self.MUSIC.composers)
            if composers:
                entity["composers"] = str(composers)
            
            lyrics = graph.value(uri, self.MUSIC.lyrics)
            if lyrics:
                entity["lyrics"] = str(lyrics)
            
            lyricist = graph.value(uri, self.MUSIC.lyricist)
            if lyricist:
                entity["lyricist"] = str(lyricist)
            
            instruments = []
            for instr in graph.objects(uri, self.MUSIC.usesInstrument):
                instr_name = graph.value(instr, self.MUSIC.name)
                instruments.append({
                    "uri": str(instr),
                    "name": str(instr_name) if instr_name else "Sin nombre"
                })
            if instruments:
                entity["instruments"] = instruments
        
        elif entity_type == "instrument":
            instr_type = graph.value(uri, self.MUSIC.type)
            if instr_type:
                entity["type"] = str(instr_type)
        
        return entity
    
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
    
    @property
    def dbpedia_service(self):
        """Lazy loading del servicio DBpedia"""
        if self._dbpedia_service is None:
            try:
                from app.dbpedia_service import DBpediaService
                self._dbpedia_service = DBpediaService()
            except Exception as e:
                print(f"⚠ No se pudo cargar DBpediaService: {e}")
                self._dbpedia_service = None
        return self._dbpedia_service
    
    def search_with_mode(self, query: str, mode: str = "offline", language: str = "en") -> List[Dict[str, Any]]:
        """
        Búsqueda con modo seleccionable (offline/online)
        
        Args:
            query: Término de búsqueda
            mode: Modo de búsqueda ("offline", "online")
            language: Idioma para consultas DBpedia (solo modo online)
            
        Returns:
            Lista de resultados con fuente indicada
        """
        if mode == "offline":
            # Búsqueda local (incluye datos locales y descargados de DBpedia)
            results = self.search(query)
            # Los resultados ya tienen su fuente marcada por _entity_to_dict
            return results
        
        elif mode == "online":
            # Solo búsqueda en DBpedia en vivo
            if self.dbpedia_service is None:
                return []
            
            try:
                # Configurar idioma del servicio DBpedia
                self.dbpedia_service.set_language(language)
                dbpedia_results = self.dbpedia_service.query_general(query, limit=20)
                return dbpedia_results
            except Exception as e:
                print(f"Error en búsqueda DBpedia: {e}")
                return []
        
        else:
            # Modo desconocido, usar offline por defecto
            return self.search_with_mode(query, "offline", language)
    
    def reload_ontology(self):
        """Recargar la ontología desde el archivo (útil después de enriquecer)"""
        self.graph = Graph()
        self.graph.bind("music", self.MUSIC)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self._load_ontology()
    
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
