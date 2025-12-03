"""
Enrichment Module - Enriquecer ontología local con datos de DBpedia
"""

import os
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.dbpedia_service import DBpediaService


class OntologyEnrichment:
    """Servicio para enriquecer la ontología local con datos de DBpedia"""
    
    def __init__(self, ontology_path: str):
        """
        Inicializar servicio de enriquecimiento
        
        Args:
            ontology_path: Ruta al archivo OWL de la ontología
        """
        self.ontology_path = ontology_path
        self.graph = Graph()
        self.MUSIC = Namespace("http://example.org/music-ontology#")
        self.dbpedia_service = DBpediaService()
        
        # Cargar ontología existente si existe
        if os.path.exists(ontology_path):
            try:
                self.graph.parse(ontology_path, format='xml')
                print(f"✓ Ontología cargada para enriquecimiento: {len(self.graph)} triplas")
            except Exception as e:
                print(f"⚠ Error al cargar ontología: {e}")
                print("  Creando nueva ontología...")
        
        # Bind namespaces
        self.graph.bind("music", self.MUSIC)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        
        # Estadísticas de enriquecimiento
        self.stats = {
            "artists_added": 0,
            "albums_added": 0,
            "songs_added": 0,
            "total_triples_added": 0,
            "last_enrichment": None
        }
    
    def enrich_artist(self, artist_name: str, fetch_albums: bool = True) -> Dict[str, Any]:
        """
        Enriquecer ontología con datos de un artista desde DBpedia
        
        Args:
            artist_name: Nombre del artista a buscar
            fetch_albums: Si también obtener álbumes del artista
            
        Returns:
            Diccionario con resultado del enriquecimiento
        """
        # Buscar artista en DBpedia
        artists = self.dbpedia_service.query_artists(artist_name, limit=1)
        
        if not artists:
            return {
                "success": False,
                "message": f"No se encontró el artista '{artist_name}' en DBpedia",
                "entities_added": 0
            }
        
        artist_data = artists[0]
        
        # Verificar si ya existe en la ontología local
        artist_uri = self._create_local_uri(artist_data["name"], "Artist")
        
        # Comprobar si ya existe
        if (artist_uri, RDF.type, self.MUSIC.Artist) in self.graph:
            return {
                "success": False,
                "message": f"El artista '{artist_data['name']}' ya existe en la ontología",
                "entities_added": 0
            }
        
        # Agregar artista al grafo
        initial_count = len(self.graph)
        self._add_artist_to_graph(artist_uri, artist_data)
        
        entities_added = 1
        self.stats["artists_added"] += 1
        
        # Opcionalmente buscar y agregar álbumes
        if fetch_albums and "uri" in artist_data:
            # Aquí podríamos hacer una consulta adicional para obtener álbumes
            # Por ahora, buscaremos álbumes por el nombre del artista
            albums = self.dbpedia_service.query_albums(artist_data["name"], limit=5)
            
            for album_data in albums:
                album_uri = self._create_local_uri(album_data["name"], "Album")
                if (album_uri, RDF.type, self.MUSIC.Album) not in self.graph:
                    self._add_album_to_graph(album_uri, album_data, artist_uri)
                    entities_added += 1
                    self.stats["albums_added"] += 1
        
        final_count = len(self.graph)
        triples_added = final_count - initial_count
        self.stats["total_triples_added"] += triples_added
        self.stats["last_enrichment"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "message": f"Artista '{artist_data['name']}' agregado con éxito",
            "entities_added": entities_added,
            "triples_added": triples_added,
            "artist_uri": str(artist_uri)
        }
    
    def enrich_album(self, album_name: str, artist_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Enriquecer ontología con datos de un álbum desde DBpedia
        
        Args:
            album_name: Nombre del álbum
            artist_name: Nombre del artista (opcional, para búsqueda más precisa)
            
        Returns:
            Diccionario con resultado del enriquecimiento
        """
        # Buscar álbum en DBpedia
        search_query = f"{album_name} {artist_name}" if artist_name else album_name
        albums = self.dbpedia_service.query_albums(search_query, limit=1)
        
        if not albums:
            return {
                "success": False,
                "message": f"No se encontró el álbum '{album_name}' en DBpedia",
                "entities_added": 0
            }
        
        album_data = albums[0]
        
        # Crear URI local
        album_uri = self._create_local_uri(album_data["name"], "Album")
        
        # Verificar si ya existe
        if (album_uri, RDF.type, self.MUSIC.Album) in self.graph:
            return {
                "success": False,
                "message": f"El álbum '{album_data['name']}' ya existe en la ontología",
                "entities_added": 0
            }
        
        initial_count = len(self.graph)
        
        # Si el álbum tiene artista, verificar/agregar artista
        artist_uri = None
        if "artist" in album_data:
            artist_uri = self._create_local_uri(album_data["artist"], "Artist")
            
            # Si el artista no existe, agregarlo
            if (artist_uri, RDF.type, self.MUSIC.Artist) not in self.graph:
                self._add_simple_artist(artist_uri, album_data["artist"])
                self.stats["artists_added"] += 1
        
        # Agregar álbum
        self._add_album_to_graph(album_uri, album_data, artist_uri)
        
        final_count = len(self.graph)
        triples_added = final_count - initial_count
        self.stats["albums_added"] += 1
        self.stats["total_triples_added"] += triples_added
        self.stats["last_enrichment"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "message": f"Álbum '{album_data['name']}' agregado con éxito",
            "entities_added": 1,
            "triples_added": triples_added,
            "album_uri": str(album_uri)
        }
    
    def enrich_song(self, song_name: str, artist_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Enriquecer ontología con datos de una canción desde DBpedia
        
        Args:
            song_name: Nombre de la canción
            artist_name: Nombre del artista (opcional)
            
        Returns:
            Diccionario con resultado del enriquecimiento
        """
        # Buscar canción en DBpedia
        search_query = f"{song_name} {artist_name}" if artist_name else song_name
        songs = self.dbpedia_service.query_songs(search_query, limit=1)
        
        if not songs:
            return {
                "success": False,
                "message": f"No se encontró la canción '{song_name}' en DBpedia",
                "entities_added": 0
            }
        
        song_data = songs[0]
        
        # Crear URI local
        song_uri = self._create_local_uri(song_data["name"], "Song")
        
        # Verificar si ya existe
        if (song_uri, RDF.type, self.MUSIC.Song) in self.graph:
            return {
                "success": False,
                "message": f"La canción '{song_data['name']}' ya existe en la ontología",
                "entities_added": 0
            }
        
        initial_count = len(self.graph)
        
        # Agregar canción
        self._add_song_to_graph(song_uri, song_data)
        
        final_count = len(self.graph)
        triples_added = final_count - initial_count
        self.stats["songs_added"] += 1
        self.stats["total_triples_added"] += triples_added
        self.stats["last_enrichment"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "message": f"Canción '{song_data['name']}' agregada con éxito",
            "entities_added": 1,
            "triples_added": triples_added,
            "song_uri": str(song_uri)
        }
    
    def enrich_batch(self, entities: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Enriquecer múltiples entidades en lote
        
        Args:
            entities: Lista de diccionarios con {type, name, artist} (opcional)
            
        Returns:
            Diccionario con resultados del proceso
        """
        results = {
            "success": True,
            "total_entities": len(entities),
            "successful": 0,
            "failed": 0,
            "errors": [],
            "details": []
        }
        
        for entity in entities:
            entity_type = entity.get("type", "").lower()
            name = entity.get("name", "")
            artist = entity.get("artist")
            
            try:
                if entity_type == "artist":
                    result = self.enrich_artist(name)
                elif entity_type == "album":
                    result = self.enrich_album(name, artist)
                elif entity_type == "song":
                    result = self.enrich_song(name, artist)
                else:
                    result = {"success": False, "message": f"Tipo desconocido: {entity_type}"}
                
                if result["success"]:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(result["message"])
                
                results["details"].append(result)
                
            except Exception as e:
                results["failed"] += 1
                error_msg = f"Error en {name}: {str(e)}"
                results["errors"].append(error_msg)
                results["details"].append({"success": False, "message": error_msg})
        
        return results
    
    def save_enriched_ontology(self, output_path: Optional[str] = None) -> bool:
        """
        Guardar ontología enriquecida a disco
        
        Args:
            output_path: Ruta de salida (usa self.ontology_path si no se especifica)
            
        Returns:
            True si se guardó exitosamente
        """
        save_path = output_path or self.ontology_path
        
        try:
            self.graph.serialize(destination=save_path, format='xml')
            print(f"✓ Ontología enriquecida guardada: {save_path} ({len(self.graph)} triplas)")
            return True
        except Exception as e:
            print(f"✗ Error al guardar ontología: {e}")
            return False
    
    def get_enrichment_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de enriquecimiento"""
        return {
            **self.stats,
            "total_triples": len(self.graph),
            "artists_in_ontology": len(list(self.graph.subjects(RDF.type, self.MUSIC.Artist))),
            "albums_in_ontology": len(list(self.graph.subjects(RDF.type, self.MUSIC.Album))),
            "songs_in_ontology": len(list(self.graph.subjects(RDF.type, self.MUSIC.Song)))
        }
    
    def get_entity_count(self) -> int:
        """Obtener cantidad total de entidades en la ontología"""
        artists = len(list(self.graph.subjects(RDF.type, self.MUSIC.Artist)))
        albums = len(list(self.graph.subjects(RDF.type, self.MUSIC.Album)))
        songs = len(list(self.graph.subjects(RDF.type, self.MUSIC.Song)))
        return artists + albums + songs
    
    # Métodos privados para agregar entidades al grafo
    
    def _create_local_uri(self, name: str, entity_type: str) -> URIRef:
        """Crear URI local para una entidad"""
        # Normalizar nombre: quitar espacios, caracteres especiales
        normalized = name.replace(" ", "_").replace("'", "").replace('"', '')
        normalized = "".join(c for c in normalized if c.isalnum() or c == "_")
        return self.MUSIC[f"{entity_type}_{normalized}"]
    
    def _add_artist_to_graph(self, artist_uri: URIRef, artist_data: Dict[str, Any]):
        """Agregar artista al grafo RDF"""
        self.graph.add((artist_uri, RDF.type, self.MUSIC.Artist))
        self.graph.add((artist_uri, self.MUSIC.name, Literal(artist_data["name"])))
        # Marcar como dato descargado de DBpedia
        self.graph.add((artist_uri, self.MUSIC.dataSource, Literal("dbpedia_downloaded")))
        
        if "description" in artist_data:
            self.graph.add((artist_uri, self.MUSIC.description, Literal(artist_data["description"])))
        
        if "birthPlace" in artist_data:
            self.graph.add((artist_uri, self.MUSIC.birthPlace, Literal(artist_data["birthPlace"])))
        
        if "genre" in artist_data:
            # Crear o referenciar género
            genre_uri = self._create_local_uri(artist_data["genre"], "Genre")
            if (genre_uri, RDF.type, self.MUSIC.Genre) not in self.graph:
                self.graph.add((genre_uri, RDF.type, self.MUSIC.Genre))
                self.graph.add((genre_uri, self.MUSIC.name, Literal(artist_data["genre"])))
            self.graph.add((artist_uri, self.MUSIC.performsGenre, genre_uri))
        
        if "birthYear" in artist_data:
            self.graph.add((artist_uri, self.MUSIC.birthYear, Literal(artist_data["birthYear"])))
        
        if "activeYears" in artist_data:
            self.graph.add((artist_uri, self.MUSIC.activeYears, Literal(artist_data["activeYears"])))
        
        if "nationality" in artist_data:
            self.graph.add((artist_uri, self.MUSIC.nationality, Literal(artist_data["nationality"])))
    
    def _add_simple_artist(self, artist_uri: URIRef, artist_name: str):
        """Agregar artista simple (solo nombre) al grafo"""
        self.graph.add((artist_uri, RDF.type, self.MUSIC.Artist))
        self.graph.add((artist_uri, self.MUSIC.name, Literal(artist_name)))
        # Marcar como dato descargado de DBpedia
        self.graph.add((artist_uri, self.MUSIC.dataSource, Literal("dbpedia_downloaded")))
    
    def _add_album_to_graph(self, album_uri: URIRef, album_data: Dict[str, Any], artist_uri: Optional[URIRef] = None):
        """Agregar álbum al grafo RDF"""
        self.graph.add((album_uri, RDF.type, self.MUSIC.Album))
        self.graph.add((album_uri, self.MUSIC.name, Literal(album_data["name"])))
        # Marcar como dato descargado de DBpedia
        self.graph.add((album_uri, self.MUSIC.dataSource, Literal("dbpedia_downloaded")))
        
        if "description" in album_data:
            self.graph.add((album_uri, self.MUSIC.description, Literal(album_data["description"])))
        
        if "releaseYear" in album_data:
            self.graph.add((album_uri, self.MUSIC.releaseYear, Literal(album_data["releaseYear"])))
        
        if "genre" in album_data:
            genre_uri = self._create_local_uri(album_data["genre"], "Genre")
            if (genre_uri, RDF.type, self.MUSIC.Genre) not in self.graph:
                self.graph.add((genre_uri, RDF.type, self.MUSIC.Genre))
                self.graph.add((genre_uri, self.MUSIC.name, Literal(album_data["genre"])))
            self.graph.add((album_uri, self.MUSIC.hasGenre, genre_uri))
        
        # Relacionar con artista
        if artist_uri:
            self.graph.add((artist_uri, self.MUSIC.hasAlbum, album_uri))
    
    def _add_song_to_graph(self, song_uri: URIRef, song_data: Dict[str, Any]):
        """Agregar canción al grafo RDF"""
        self.graph.add((song_uri, RDF.type, self.MUSIC.Song))
        self.graph.add((song_uri, self.MUSIC.name, Literal(song_data["name"])))
        # Marcar como dato descargado de DBpedia
        self.graph.add((song_uri, self.MUSIC.dataSource, Literal("dbpedia_downloaded")))
        
        if "description" in song_data:
            self.graph.add((song_uri, self.MUSIC.description, Literal(song_data["description"])))
        
        if "duration" in song_data:
            self.graph.add((song_uri, self.MUSIC.duration, Literal(song_data["duration"])))
        
        if "artist" in song_data:
            artist_uri = self._create_local_uri(song_data["artist"], "Artist")
            if (artist_uri, RDF.type, self.MUSIC.Artist) not in self.graph:
                self._add_simple_artist(artist_uri, song_data["artist"])
            self.graph.add((song_uri, self.MUSIC.performedBy, artist_uri))
