"""
Script para descargar datos de DBpedia y guardarlos localmente en la ontología.
Este script descarga algunos artistas, álbumes y canciones de DBpedia para pruebas locales.
"""

from app.dbpedia_service import DBpediaService
from rdflib import Graph, Namespace, RDF, Literal, URIRef
import os
import sys

# Configuraciones
ONTOLOGY_PATH = os.path.join(os.path.dirname(__file__), "data", "music-ontology.owl")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "dbpedia-downloaded.owl")

# Namespace de la ontología
MUSIC = Namespace("http://example.org/music-ontology#")

# Entidades de ejemplo para descargar
SAMPLE_ENTITIES = {
    "artists": ["Madonna", "Coldplay", "Adele", "Ed Sheeran", "The Beatles"],
    "albums": ["Thriller", "Abbey Road", "21", "A Head Full of Dreams"],
    "songs": ["Bohemian Rhapsody", "Imagine", "Hello", "Viva la Vida"]
}

def download_dbpedia_data(language: str = "en"):
    """
    Descarga datos de DBpedia para las entidades de ejemplo
    
    Args:
        language: Idioma para las consultas (en, es, fr, de)
    """
    print(f"\n🌐 Descargando datos de DBpedia ({language})...")
    print("=" * 60)
    
    # Inicializar servicio DBpedia
    dbpedia_service = DBpediaService(language=language)
    
    # Crear grafo para almacenar los datos descargados
    graph = Graph()
    graph.bind("music", MUSIC)
    graph.bind("rdf", RDF)
    
    total_downloaded = 0
    
    # Descargar artistas
    print(f"\n📥 Descargando artistas...")
    for artist_name in SAMPLE_ENTITIES["artists"]:
        print(f"  • Buscando: {artist_name}...")
        try:
            results = dbpedia_service.query_artists(artist_name, limit=1)
            if results:
                artist_data = results[0]
                artist_uri = URIRef(artist_data["uri"])
                
                # Agregar triplas al grafo
                graph.add((artist_uri, RDF.type, MUSIC.Artist))
                graph.add((artist_uri, MUSIC.name, Literal(artist_data["name"])))
                
                if "description" in artist_data:
                    graph.add((artist_uri, MUSIC.description, Literal(artist_data["description"])))
                if "nationality" in artist_data:
                    graph.add((artist_uri, MUSIC.nationality, Literal(artist_data["nationality"])))
                if "birthYear" in artist_data:
                    graph.add((artist_uri, MUSIC.birthYear, Literal(artist_data["birthYear"])))
                if "activeYears" in artist_data:
                    graph.add((artist_uri, MUSIC.activeYears, Literal(artist_data["activeYears"])))
                if "genre" in artist_data:
                    graph.add((artist_uri, MUSIC.genre, Literal(artist_data["genre"])))
                
                # Marcar como descargado de DBpedia
                graph.add((artist_uri, MUSIC.dataSource, Literal("dbpedia_downloaded")))
                
                total_downloaded += 1
                print(f"    ✓ Descargado: {artist_data['name']}")
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
    
    # Descargar álbumes
    print(f"\n📥 Descargando álbumes...")
    for album_name in SAMPLE_ENTITIES["albums"]:
        print(f"  • Buscando: {album_name}...")
        try:
            results = dbpedia_service.query_albums(album_name, limit=1)
            if results:
                album_data = results[0]
                album_uri = URIRef(album_data["uri"])
                
                # Agregar triplas al grafo
                graph.add((album_uri, RDF.type, MUSIC.Album))
                graph.add((album_uri, MUSIC.name, Literal(album_data["name"])))
                
                if "description" in album_data:
                    graph.add((album_uri, MUSIC.description, Literal(album_data["description"])))
                if "releaseYear" in album_data:
                    graph.add((album_uri, MUSIC.releaseYear, Literal(album_data["releaseYear"])))
                if "genre" in album_data:
                    graph.add((album_uri, MUSIC.genre, Literal(album_data["genre"])))
                if "artist" in album_data:
                    graph.add((album_uri, MUSIC.artist, Literal(album_data["artist"])))
                
                # Marcar como descargado de DBpedia
                graph.add((album_uri, MUSIC.dataSource, Literal("dbpedia_downloaded")))
                
                total_downloaded += 1
                print(f"    ✓ Descargado: {album_data['name']}")
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
    
    # Descargar canciones
    print(f"\n📥 Descargando canciones...")
    for song_name in SAMPLE_ENTITIES["songs"]:
        print(f"  • Buscando: {song_name}...")
        try:
            results = dbpedia_service.query_songs(song_name, limit=1)
            if results:
                song_data = results[0]
                song_uri = URIRef(song_data["uri"])
                
                # Agregar triplas al grafo
                graph.add((song_uri, RDF.type, MUSIC.Song))
                graph.add((song_uri, MUSIC.name, Literal(song_data["name"])))
                
                if "description" in song_data:
                    graph.add((song_uri, MUSIC.description, Literal(song_data["description"])))
                if "duration" in song_data:
                    graph.add((song_uri, MUSIC.duration, Literal(song_data["duration"])))
                if "artist" in song_data:
                    graph.add((song_uri, MUSIC.artist, Literal(song_data["artist"])))
                
                # Marcar como descargado de DBpedia
                graph.add((song_uri, MUSIC.dataSource, Literal("dbpedia_downloaded")))
                
                total_downloaded += 1
                print(f"    ✓ Descargado: {song_data['name']}")
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
    
    # Guardar el grafo
    print(f"\n💾 Guardando datos descargados...")
    graph.serialize(destination=OUTPUT_PATH, format='xml')
    print(f"✓ Archivo guardado: {OUTPUT_PATH}")
    print(f"✓ Total de entidades descargadas: {total_downloaded}")
    print(f"✓ Total de triplas: {len(graph)}")
    
    return graph


def merge_with_ontology():
    """
    Combinar los datos descargados con la ontología principal
    """
    print(f"\n🔗 Combinando con ontología principal...")
    
    if not os.path.exists(OUTPUT_PATH):
        print("⚠ No hay datos descargados para combinar.")
        return
    
    # Cargar ontología principal
    main_graph = Graph()
    main_graph.parse(ONTOLOGY_PATH, format='xml')
    print(f"  • Ontología principal: {len(main_graph)} triplas")
    
    # Cargar datos descargados
    downloaded_graph = Graph()
    downloaded_graph.parse(OUTPUT_PATH, format='xml')
    print(f"  • Datos descargados: {len(downloaded_graph)} triplas")
    
    # Combinar
    for triple in downloaded_graph:
        main_graph.add(triple)
    
    # Guardar ontología combinada
    backup_path = ONTOLOGY_PATH + ".backup"
    print(f"\n💾 Creando respaldo: {backup_path}")
    
    # Hacer backup de la ontología original
    import shutil
    shutil.copy2(ONTOLOGY_PATH, backup_path)
    
    # Guardar ontología combinada
    main_graph.serialize(destination=ONTOLOGY_PATH, format='xml')
    print(f"✓ Ontología combinada guardada: {ONTOLOGY_PATH}")
    print(f"✓ Total de triplas: {len(main_graph)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Descargar datos de DBpedia")
    parser.add_argument(
        "--language", 
        "-l", 
        default="en", 
        choices=["en", "es", "fr", "de"],
        help="Idioma para las consultas (default: en)"
    )
    parser.add_argument(
        "--merge",
        "-m",
        action="store_true",
        help="Combinar datos descargados con la ontología principal"
    )
    
    args = parser.parse_args()
    
    try:
        # Descargar datos
        download_dbpedia_data(args.language)
        
        # Combinar con ontología principal si se especifica
        if args.merge:
            merge_with_ontology()
        
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
