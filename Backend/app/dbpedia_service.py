"""
DBpedia Service - Interfaz para consultar DBpedia mediante SPARQL
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict, Any, Optional
import time
from datetime import datetime, timedelta
import re


class DBpediaService:
    """Servicio para consultar DBpedia mediante SPARQL"""
    
    # Mapeo de idiomas a subdominios de DBpedia
    LANGUAGE_DOMAINS = {
        "en": "dbpedia.org",
        "es": "es.dbpedia.org",
        "fr": "fr.dbpedia.org",
    }
    
    def __init__(self, endpoint: str = None, language: str = "en"):
        """
        Inicializar el servicio DBpedia
        
        Args:
            endpoint: URL del endpoint SPARQL de DBpedia (si es None, se genera según el idioma)
            language: Idioma para consultas (en, es, fr)
        """
        self.language = language
        
        # Si no se proporciona endpoint, generar según el idioma
        if endpoint is None:
            domain = self.LANGUAGE_DOMAINS.get(language, "dbpedia.org")
            self.endpoint = f"https://{domain}/sparql"
        else:
            self.endpoint = endpoint
        
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)
        self.cache = {}  # Caché simple en memoria
        self.cache_ttl = 3600  # 1 hora
    
    def set_language(self, language: str):
        """
        Cambiar el idioma de las consultas y actualizar el endpoint SPARQL
        """
        self.language = language
        # Actualizar el endpoint SPARQL según el idioma
        domain = self.LANGUAGE_DOMAINS.get(language, "dbpedia.org")
        self.endpoint = f"https://{domain}/sparql"
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)
    
    def get_dbpedia_url(self, entity_name: str) -> str:
        """
        Generar URL de DBpedia según el idioma configurado
        
        Args:
            entity_name: Nombre de la entidad
            
        Returns:
            URL de DBpedia en el idioma correspondiente
        """
        domain = self.LANGUAGE_DOMAINS.get(self.language, "dbpedia.org")
        # Formatear nombre: reemplazar espacios por guiones bajos
        formatted_name = entity_name.replace(" ", "_")
        
        # Si el idioma es inglés, usar dbpedia.org; sino, usar el subdominio de idioma
        if self.language == "en":
            return f"https://dbpedia.org/resource/{formatted_name}"
        else:
            return f"https://{domain}/resource/{formatted_name}"
    
    def transform_dbpedia_url_to_language(self, dbpedia_uri: str) -> str:
        """
        Transformar URL de DBpedia al dominio del idioma configurado
        
        Args:
            dbpedia_uri: URI de DBpedia (ej: http://dbpedia.org/resource/The_Beatles)
            
        Returns:
            URL de DBpedia en el idioma configurado (ej: http://fr.dbpedia.org/resource/The_Beatles)
        """
        if not dbpedia_uri or "dbpedia.org" not in dbpedia_uri:
            return dbpedia_uri
        
        # Extraer el nombre de recurso
        if "/resource/" in dbpedia_uri:
            resource_name = dbpedia_uri.split("/resource/")[-1]
        elif "/page/" in dbpedia_uri:
            resource_name = dbpedia_uri.split("/page/")[-1]
        else:
            return dbpedia_uri
        
        # Obtener dominio del idioma
        domain = self.LANGUAGE_DOMAINS.get(self.language, "dbpedia.org")
        
        # Si el idioma es inglés, usar dbpedia.org; sino, usar el subdominio de idioma
        if self.language == "en":
            return f"https://dbpedia.org/resource/{resource_name}"
        else:
            return f"https://{domain}/resource/{resource_name}"
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
            self.sparql.setTimeout(30)  # Aumentado a 30 segundos para consultas complejas
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
        Buscar artistas en DBpedia con múltiples estrategias incluyendo búsqueda por palabras clave
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de artistas encontrados
        """
        # Primero intentar búsqueda directa
        results = self._search_artists_direct(query, limit * 2)
        
        # Si no hay resultados, intentar búsqueda por palabras individuales
        if not results and " " in query:
            words = query.split()
            for word in words:
                if len(word) >= 3:  # Solo palabras de 3+ caracteres
                    results.extend(self._search_artists_direct(word, limit))
        
        # Deduplicar y ordenar por relevancia
        seen_uris = set()
        unique_results = []
        for artist in results:
            uri = artist.get("uri", "")
            if uri not in seen_uris:
                seen_uris.add(uri)
                unique_results.append(artist)
        
        # Ordenar: primero búsquedas exactas, luego por relevancia del nombre
        sorted_results = sorted(
            unique_results,
            key=lambda a: (
                query.lower() not in a.get("name", "").lower(),
                len(a.get("name", "")) 
            )
        )
        
        return sorted_results[:limit]
    
    def _search_artists_direct(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Búsqueda directa de artistas con múltiples estrategias"""
        lang = self.language if self.language else "en"
        safe_query = query.replace('"', '\\"').replace('\\', '\\\\')
        
        # Estrategia 1: Búsqueda específica en recursos musicales conocidos
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        
        SELECT DISTINCT ?artist ?name ?abstract
        WHERE {{
            ?artist foaf:name ?name ;
                    a ?type .
            VALUES ?type {{ 
                dbo:MusicalArtist 
                dbo:Band 
                dbo:Musician
            }}
            
            FILTER(
                CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                REGEX(?name, ".*{safe_query}.*", "i")
            )
            
            OPTIONAL {{ 
                ?artist dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
        }}
        LIMIT {limit}
        """
        
        try:
            results = self._execute_sparql(sparql_query)
            artists = self._map_to_local_format(results, "artist")
            if artists:
                return artists
        except:
            pass
        
        # Estrategia 2: Búsqueda sin restricción de tipo pero con propiedades musicales
        try:
            sparql_query_prop = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            
            SELECT DISTINCT ?artist ?name ?abstract
            WHERE {{
                ?artist foaf:name ?name .
                {{
                    ?artist dbo:genre ?_ .
                }} UNION {{
                    ?artist dbo:associatedBand ?_ .
                }} UNION {{
                    ?artist dbo:associatedMusicalArtist ?_ .
                }} UNION {{
                    ?artist dbo:bandMember ?_ .
                }}
                
                FILTER(
                    CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                    REGEX(?name, ".*{safe_query}.*", "i")
                )
                
                OPTIONAL {{ 
                    ?artist dbo:abstract ?abstract .
                    FILTER(LANG(?abstract) = "{lang}")
                }}
            }}
            LIMIT {limit}
            """
            
            results = self._execute_sparql(sparql_query_prop)
            artists = self._map_to_local_format(results, "artist")
            if artists:
                return artists
        except:
            pass
        
        # Estrategia 3: Búsqueda muy amplia pero con timeout bajo
        try:
            sparql_query_broad = f"""
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            
            SELECT DISTINCT ?artist ?name ?abstract
            WHERE {{
                ?artist foaf:name ?name ;
                        dbo:abstract ?abstract .
                
                FILTER(
                    CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) && 
                    LANG(?abstract) = "{lang}"
                )
            }}
            LIMIT {limit}
            """
            
            results = self._execute_sparql(sparql_query_broad, use_cache=False)
            artists = self._map_to_local_format(results, "artist")
            if artists:
                return artists
        except:
            pass
        
        return []
    
    def query_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar álbumes en DBpedia con múltiples estrategias
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de álbumes encontrados
        """
        # Usar idioma configurado o inglés como fallback
        lang = self.language if self.language else "en"
        # Escapar caracteres especiales en la consulta SPARQL
        safe_query = query.replace('"', '\\"')
        
        # Consulta mejorada que busca en múltiples tipos
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?album ?name ?artist ?artistName ?releaseDate ?genre ?abstract
        WHERE {{
            {{
                ?album a dbo:Album ;
                       foaf:name ?name .
            }} UNION {{
                ?album a dbo:MusicalWork ;
                       foaf:name ?name .
            }} UNION {{
                ?album a dbo:Single ;
                       foaf:name ?name .
            }} UNION {{
                ?album a dbo:Compilation ;
                       foaf:name ?name .
            }}
            
            FILTER(
                CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                REGEX(?name, "{safe_query}", "i") ||
                REGEX(?name, ".*{safe_query}.*", "i")
            )
            
            OPTIONAL {{ 
                ?album dbo:artist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ ?album dbo:releaseDate ?releaseDate }}
            OPTIONAL {{ ?album dbo:genre ?genre }}
            OPTIONAL {{ 
                ?album dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "album")
    
    def query_songs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar canciones en DBpedia con múltiples estrategias
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de canciones encontradas
        """
        # Usar idioma configurado o inglés como fallback
        lang = self.language if self.language else "en"
        # Escapar caracteres especiales en la consulta SPARQL
        safe_query = query.replace('"', '\\"')
        
        # Consulta mejorada que busca en múltiples tipos
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?song ?name ?artist ?artistName ?album ?runtime ?abstract
        WHERE {{
            {{
                ?song a dbo:Song ;
                      foaf:name ?name .
            }} UNION {{
                ?song a dbo:Single ;
                      foaf:name ?name .
            }} UNION {{
                ?song a dbo:MusicalWork ;
                      foaf:name ?name .
            }} UNION {{
                ?song a dbo:Composition ;
                      foaf:name ?name .
            }}
            
            FILTER(
                CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                REGEX(?name, "{safe_query}", "i") ||
                REGEX(?name, ".*{safe_query}.*", "i")
            )
            
            OPTIONAL {{ 
                ?song dbo:musicalArtist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ 
                ?song dbo:artist ?artist .
                ?artist foaf:name ?artistName .
            }}
            OPTIONAL {{ ?song dbo:album ?album }}
            OPTIONAL {{ ?song dbo:runtime ?runtime }}
            OPTIONAL {{ 
                ?song dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "song")
    
    def query_instruments(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar instrumentos en DBpedia con múltiples estrategias
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de instrumentos encontrados
        """
        # Usar idioma configurado o inglés como fallback
        lang = self.language if self.language else "en"
        # Escapar caracteres especiales en la consulta SPARQL
        safe_query = query.replace('"', '\\"')
        
        # Consulta mejorada para instrumentos
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?instrument ?name ?abstract ?type ?classification
        WHERE {{
            {{
                ?instrument a dbo:Instrument ;
                            foaf:name ?name .
            }} UNION {{
                ?instrument a dbo:MusicalInstrument ;
                            foaf:name ?name .
            }} UNION {{
                ?instrument a dbo:StringInstrument ;
                            foaf:name ?name .
            }} UNION {{
                ?instrument a dbo:KeyboardInstrument ;
                            foaf:name ?name .
            }} UNION {{
                ?instrument a dbo:PercussionInstrument ;
                            foaf:name ?name .
            }} UNION {{
                ?instrument a dbo:WindInstrument ;
                            foaf:name ?name .
            }}
            
            FILTER(
                CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                REGEX(?name, "{safe_query}", "i") ||
                REGEX(?name, ".*{safe_query}.*", "i")
            )
            
            OPTIONAL {{ 
                ?instrument dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
            OPTIONAL {{ ?instrument dbo:instrumentType ?type }}
            OPTIONAL {{ ?instrument dbo:classification ?classification }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "instrument")
    
    def query_genres(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Buscar géneros en DBpedia con múltiples estrategias
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de géneros encontrados
        """
        # Usar idioma configurado o inglés como fallback
        lang = self.language if self.language else "en"
        # Escapar caracteres especiales en la consulta SPARQL
        safe_query = query.replace('"', '\\"')
        
        # Consulta mejorada para géneros
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?genre ?name ?abstract ?parent ?originated
        WHERE {{
            {{
                ?genre a dbo:Genre ;
                       foaf:name ?name .
            }} UNION {{
                ?genre a dbo:MusicGenre ;
                       foaf:name ?name .
            }} UNION {{
                ?genre rdfs:label ?name .
                ?genre rdfs:subClassOf ?parent .
                ?parent rdfs:label "Genre"@en .
            }}
            
            FILTER(
                CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || 
                REGEX(?name, "{safe_query}", "i") ||
                REGEX(?name, ".*{safe_query}.*", "i")
            )
            
            OPTIONAL {{ 
                ?genre dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
            OPTIONAL {{ ?genre dbo:parentGenre ?parent }}
            OPTIONAL {{ ?genre dbo:dateOfOrigin ?originated }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        return self._map_to_local_format(results, "genre")
    def query_general(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Búsqueda general en DBpedia (artistas, álbumes, canciones, instrumentos y géneros)
        Utiliza una estrategia de múltiples búsquedas para capturar más resultados
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados por tipo
            
        Returns:
            Lista combinada de resultados sin duplicados
        """
        results = []
        seen_uris = set()  # Para evitar duplicados
        
        # Intentar búsqueda normal primero
        # Distribuir el límite entre 5 tipos de búsqueda
        limit_per_type = max(limit // 5, 3)
        
        # Buscar artistas
        artists = self.query_artists(query, limit_per_type)
        for artist in artists:
            uri = artist.get("uri", "")
            if uri and uri not in seen_uris:
                results.append({"type": "artist", "data": artist, "source": "dbpedia_live"})
                seen_uris.add(uri)
        
        # Buscar álbumes
        albums = self.query_albums(query, limit_per_type)
        for album in albums:
            uri = album.get("uri", "")
            if uri and uri not in seen_uris:
                results.append({"type": "album", "data": album, "source": "dbpedia_live"})
                seen_uris.add(uri)
        
        # Buscar canciones
        songs = self.query_songs(query, limit_per_type)
        for song in songs:
            uri = song.get("uri", "")
            if uri and uri not in seen_uris:
                results.append({"type": "song", "data": song, "source": "dbpedia_live"})
                seen_uris.add(uri)
        
        # Buscar instrumentos
        instruments = self.query_instruments(query, limit_per_type)
        for instrument in instruments:
            uri = instrument.get("uri", "")
            if uri and uri not in seen_uris:
                results.append({"type": "instrument", "data": instrument, "source": "dbpedia_live"})
                seen_uris.add(uri)
        
        # Buscar géneros
        genres = self.query_genres(query, limit_per_type)
        for genre in genres:
            uri = genre.get("uri", "")
            if uri and uri not in seen_uris:
                results.append({"type": "genre", "data": genre, "source": "dbpedia_live"})
                seen_uris.add(uri)
        
        # Si no hay resultados, intentar búsqueda más amplia
        if not results:
            results = self._query_broad_search(query, limit)
        
        return results
    
    def _query_broad_search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Búsqueda muy amplia para capturar resultados que podrían haber sido perdidos
        Busca en labels, aliases y abstracts de todas las entidades musicales
        
        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista combinada de resultados
        """
        safe_query = query.replace('"', '\\"')
        lang = self.language if self.language else "en"
        
        sparql_query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        
        SELECT DISTINCT ?entity ?name ?abstract ?type
        WHERE {{
            ?entity foaf:name ?name .
            
            FILTER(CONTAINS(LCASE(STR(?name)), LCASE("{safe_query}")) || REGEX(?name, "{safe_query}", "i"))
            
            {{
                ?entity a dbo:MusicalArtist .
                BIND("artist" as ?type)
            }} UNION {{
                ?entity a dbo:Band .
                BIND("artist" as ?type)
            }} UNION {{
                ?entity a dbo:Musician .
                BIND("artist" as ?type)
            }} UNION {{
                ?entity a dbo:Album .
                BIND("album" as ?type)
            }} UNION {{
                ?entity a dbo:MusicalWork .
                BIND("song" as ?type)
            }} UNION {{
                ?entity a dbo:Song .
                BIND("song" as ?type)
            }} UNION {{
                ?entity a dbo:Single .
                BIND("album" as ?type)
            }} UNION {{
                ?entity a dbo:Instrument .
                BIND("instrument" as ?type)
            }} UNION {{
                ?entity a dbo:MusicalInstrument .
                BIND("instrument" as ?type)
            }} UNION {{
                ?entity a dbo:Genre .
                BIND("genre" as ?type)
            }} UNION {{
                ?entity a dbo:MusicGenre .
                BIND("genre" as ?type)
            }}
            
            OPTIONAL {{ 
                ?entity dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "{lang}")
            }}
        }}
        LIMIT {limit}
        """
        
        results = self._execute_sparql(sparql_query)
        output = []
        for binding in results.get("results", {}).get("bindings", []):
            entity_dict = self._binding_to_dict(binding, binding.get("type", {}).get("value", "artist"))
            if entity_dict:
                output.append({
                    "type": binding.get("type", {}).get("value", "artist"),
                    "data": entity_dict,
                    "source": "dbpedia_live"
                })
        
        return output
    
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
        entity_uri = binding.get(entity_type, {}).get("value", "")
        entity_name = binding.get("name", {}).get("value", "Unknown")
        
        # Generar URL de DBpedia en el idioma configurado
        if entity_uri and "dbpedia.org" in entity_uri:
            dbpedia_url = self.transform_dbpedia_url_to_language(entity_uri)
        else:
            dbpedia_url = self.get_dbpedia_url(entity_name)
        
        entity = {
            "uri": entity_uri,
            "name": entity_name,
            "type": entity_type,
            "dbpediaUrl": dbpedia_url
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
