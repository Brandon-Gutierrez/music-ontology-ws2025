"""
Script simplificado para descargar ~20 entidades de DBpedia para uso local
Este script NO modifica la ontología local, guarda los datos en un archivo separado.
"""

from app.dbpedia_service import DBpediaService
from rdflib import Graph, Namespace, RDF, Literal, URIRef
import os

# Configuraciones
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "dbpedia-downloaded.owl")

# Namespace de la ontología
MUSIC = Namespace("http://example.org/music-ontology#")

# Entidades para descargar (~20 total)
SAMPLE_ENTITIES = {
    "artists": ["Madonna", "Coldplay", "Adele", "Ed Sheeran", "The Beatles", "Queen", "Pink Floyd"],
    "albums": ["Thriller", "Abbey Road", "21", "A Head Full of Dreams", "The Dark Side of the Moon"],
    "songs": ["Bohemian Rhapsody", "Imagine", "Hello", "Viva la Vida", "Hey Jude", "Hotel California", "Stairway to Heaven", "Billie Jean"]
}

def download_dbpedia_data(language: str = "en"):
    """
    Descarga datos de DBpedia para las entidades de ejemplo (sin modificar ontología local)
    
    Args:
        language: Idioma para las consultas (en, es, fr, de)
    """
    print(f"\n🌐 Descargando ~20 entidades de DBpedia ({language})...")
    print("=" * 70)
    
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
                artist_uri = URIRef(f"http://dbpedia.org/resource/{artist_name.replace(' ', '_')}")
                
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
                album_uri = URIRef(f"http://dbpedia.org/resource/{album_name.replace(' ', '_')}")
                
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
                song_uri = URIRef(f"http://dbpedia.org/resource/{song_name.replace(' ', '_')}")
                
                # Agregar triplas al grafo
                graph.add((song_uri, RDF.type, MUSIC.Song))
                graph.add((song_uri, MUSIC.name, Literal(song_data["name"])))
                
                if "description" in song_data:
                    graph.add((song_uri, MUSIC.description, Literal(song_data["description"])))
                if "duration" in song_data:
                    graph.add((song_uri, MUSIC.duration, Literal(song_data["duration"])))
                if "artist" in song_data:
                    graph.add((song_uri, MUSIC.artist, Literal(song_data["artist"])))
                
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
    print(f"\n⚠️  IMPORTANTE: La ontología local NO fue modificada")
    print(f"   Los datos están guardados en: {OUTPUT_PATH}")
    
    return graph


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Descargar ~20 entidades de DBpedia")
    parser.add_argument(
        "--language", 
        "-l", 
        default="en", 
        choices=["en", "es", "fr", "de"],
        help="Idioma para las consultas (default: en)"
    )
    
    args = parser.parse_args()
    
    try:
        download_dbpedia_data(args.language)
        print("\n✅ Descarga completada exitosamente!")
        print("   Los datos están listos para usar en modo offline.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import sys
        sys.exit(1)
