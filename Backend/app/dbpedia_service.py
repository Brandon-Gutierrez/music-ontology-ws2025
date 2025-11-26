"""
DBpedia Service - Interfaz para consultar DBpedia mediante SPARQL
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict, Any, Optional
import time
from datetime import datetime, timedelta


class DBpediaService:
    """Servicio para consultar DBpedia mediante SPARQL"""
    
    def __init__(self, endpoint: str = "https://dbpedia.org/sparql"):
        """
        Inicializar el servicio DBpedia
        
        Args:
            endpoint: URL del endpoint SPARQL de DBpedia
        """
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)
        self.cache = {}  # Caché simple en memoria
        self.cache_ttl = 3600  # 1 hora
        
    def _execute_sparql(self, query: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Ejecutar consulta SPARQL con manejo de errores y caché
        
        Args:
            query: Consulta SPARQL
            use_cache: Si usar caché para esta consulta
            
        Returns:
            Resultados de la consulta
        """
        # Verificar caché
        cache_key = hash(query)
        if use_cache and cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=self.cache_ttl):
                return cached_data
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            
            # Guardar en caché
            if use_cache:
                self.cache[cache_key] = (results, datetime.now())
            
            return results
        except Exception as e:
            print(f"Error en consulta SPARQL: {str(e)}")
            return {"results": {"bindings": []}}
    
    def query_artists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar artistas en DBpedia
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de artistas encontrados
        """
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?artist ?name ?abstract ?birthPlace ?genre ?birthYear ?activeYears
        WHERE {{
            ?artist a dbo:MusicalArtist .
            ?artist foaf:name ?name .
            FILTER(LANG(?name) = "en" || LANG(?name) = "")
            FILTER(REGEX(?name, "{query}", "i"))
            
            OPTIONAL {{ 
                ?artist dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }}
            OPTIONAL {{ ?artist dbo:birthPlace ?birthPlace }}
            OPTIONAL {{ ?artist dbo:genre ?genre }}
            OPTIONAL {{ ?artist dbo:birthYear ?birthYear }}
            OPTIONAL {{ ?artist dbo:activeYearsStartYear ?activeYears }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "artist")
    
    def query_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar álbumes en DBpedia
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de álbumes encontrados
        """
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?album ?name ?artist ?artistName ?releaseDate ?genre ?abstract
        WHERE {{
            ?album a dbo:Album .
            ?album foaf:name ?name .
            FILTER(LANG(?name) = "en" || LANG(?name) = "")
            FILTER(REGEX(?name, "{query}", "i"))
            
            OPTIONAL {{ 
                ?album dbo:artist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ ?album dbo:releaseDate ?releaseDate }}
            OPTIONAL {{ ?album dbo:genre ?genre }}
            OPTIONAL {{ 
                ?album dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "album")
    
    def query_songs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar canciones en DBpedia
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de canciones encontradas
        """
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?song ?name ?artist ?artistName ?album ?runtime ?abstract
        WHERE {{
            {{ ?song a dbo:Song }} UNION {{ ?song a dbo:Single }}
            ?song foaf:name ?name .
            FILTER(LANG(?name) = "en" || LANG(?name) = "")
            FILTER(REGEX(?name, "{query}", "i"))
            
            OPTIONAL {{ 
                ?song dbo:musicalArtist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ ?song dbo:album ?album }}
            OPTIONAL {{ ?song dbo:runtime ?runtime }}
            OPTIONAL {{ 
                ?song dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "song")
    
    def query_general(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Búsqueda general en DBpedia (artistas, álbumes y canciones)
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados por tipo
            
        Returns:
            Lista combinada de resultados
        """
        results = []
        
        # Buscar artistas
        artists = self.query_artists(query, limit // 3)
        results.extend([{"type": "artist", "data": a, "source": "dbpedia"} for a in artists])
        
        # Buscar álbumes
        albums = self.query_albums(query, limit // 3)
        results.extend([{"type": "album", "data": a, "source": "dbpedia"} for a in albums])
        
        # Buscar canciones
        songs = self.query_songs(query, limit // 3)
        results.extend([{"type": "song", "data": s, "source": "dbpedia"} for s in songs])
        
        return results
    
    def get_artist_details(self, artist_uri: str) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de un artista desde DBpedia
        
        Args:
            artist_uri: URI del artista en DBpedia
            
        Returns:
            Diccionario con información del artista
        """
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?name ?abstract ?birthPlace ?genre ?birthYear ?activeYears ?nationality
        WHERE {{
            <{artist_uri}> foaf:name ?name .
            OPTIONAL {{ 
                <{artist_uri}> dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }}
            OPTIONAL {{ <{artist_uri}> dbo:birthPlace ?birthPlace }}
            OPTIONAL {{ <{artist_uri}> dbo:genre ?genre }}
            OPTIONAL {{ <{artist_uri}> dbo:birthYear ?birthYear }}
            OPTIONAL {{ <{artist_uri}> dbo:activeYearsStartYear ?activeYears }}
            OPTIONAL {{ <{artist_uri}> dbo:nationality ?nationality }}
        }}
        LIMIT 1
        """
        
        results = self._execute_sparql(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        
        if not bindings:
            return None
            
        return self._binding_to_dict(bindings[0], "artist")
    
    def get_album_details(self, album_uri: str) -> Optional[Dict[str, Any]]:
        """
        Obtener detalles completos de un álbum desde DBpedia
        
        Args:
            album_uri: URI del álbum en DBpedia
            
        Returns:
            Diccionario con información del álbum
        """
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?name ?artist ?artistName ?releaseDate ?genre ?abstract ?recordLabel
        WHERE {{
            <{album_uri}> foaf:name ?name .
            OPTIONAL {{ 
                <{album_uri}> dbo:artist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ <{album_uri}> dbo:releaseDate ?releaseDate }}
            OPTIONAL {{ <{album_uri}> dbo:genre ?genre }}
            OPTIONAL {{ <{album_uri}> dbo:recordLabel ?recordLabel }}
            OPTIONAL {{ 
                <{album_uri}> dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }}
        }}
        LIMIT 1
        """
        
        results = self._execute_sparql(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        
        if not bindings:
            return None
            
        return self._binding_to_dict(bindings[0], "album")
    
    def _map_to_local_format(self, results: Dict[str, Any], entity_type: str) -> List[Dict[str, Any]]:
        """
        Transformar resultados SPARQL al formato de la ontología local
        
        Args:
            results: Resultados SPARQL
            entity_type: Tipo de entidad ("artist", "album", "song")
            
        Returns:
            Lista de entidades en formato local
        """
        bindings = results.get("results", {}).get("bindings", [])
        entities = []
        
        for binding in bindings:
            entity = self._binding_to_dict(binding, entity_type)
            if entity:
                entities.append(entity)
        
        return entities
    
    def _binding_to_dict(self, binding: Dict[str, Any], entity_type: str) -> Dict[str, Any]:
        """
        Convertir un binding SPARQL a diccionario local
        
        Args:
            binding: Binding de resultado SPARQL
            entity_type: Tipo de entidad
            
        Returns:
            Diccionario con información de la entidad
        """
        entity = {
            "uri": binding.get(entity_type, {}).get("value", ""),
            "name": binding.get("name", {}).get("value", "Unknown"),
            "type": entity_type
        }
        
        # Descripción/abstract
        if "abstract" in binding:
            abstract = binding["abstract"]["value"]
            # Truncar abstract a primeras 500 caracteres
            entity["description"] = abstract[:500] + "..." if len(abstract) > 500 else abstract
        
        # Propiedades específicas por tipo
        if entity_type == "artist":
            if "birthPlace" in binding:
                place = binding["birthPlace"]["value"]
                # Extraer solo el nombre del lugar, no la URL completa
                entity["birthPlace"] = place.split("/")[-1].replace("_", " ")
            
            if "genre" in binding:
                genre = binding["genre"]["value"]
                entity["genre"] = genre.split("/")[-1].replace("_", " ")
            
            if "birthYear" in binding:
                entity["birthYear"] = int(binding["birthYear"]["value"])
            
            if "activeYears" in binding:
                entity["activeYears"] = str(binding["activeYears"]["value"])
            
            if "nationality" in binding:
                nationality = binding["nationality"]["value"]
                entity["nationality"] = nationality.split("/")[-1].replace("_", " ")
        
        elif entity_type == "album":
            if "artist" in binding:
                entity["artist"] = binding.get("artistName", {}).get("value", "")
                entity["artistUri"] = binding["artist"]["value"]
            
            if "releaseDate" in binding:
                release_date = binding["releaseDate"]["value"]
                # Extraer solo el año
                try:
                    entity["releaseYear"] = int(release_date[:4])
                except:
                    entity["releaseYear"] = release_date
            
            if "genre" in binding:
                genre = binding["genre"]["value"]
                entity["genre"] = genre.split("/")[-1].replace("_", " ")
        
        elif entity_type == "song":
            if "artist" in binding:
                entity["artist"] = binding.get("artistName", {}).get("value", "")
                entity["artistUri"] = binding["artist"]["value"]
            
            if "album" in binding:
                album_uri = binding["album"]["value"]
                entity["album"] = album_uri.split("/")[-1].replace("_", " ")
            
            if "runtime" in binding:
                try:
                    # Runtime en DBpedia está en segundos
                    entity["duration"] = int(float(binding["runtime"]["value"]))
                except:
                    pass
        
        return entity
    
    def clear_cache(self):
        """Limpiar caché de consultas"""
        self.cache.clear()
