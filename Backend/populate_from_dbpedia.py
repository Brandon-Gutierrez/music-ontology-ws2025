#!/usr/bin/env python
"""
Script CLI para poblar la ontología con datos de DBpedia
Uso:
    python populate_from_dbpedia.py --artists "The Beatles,Pink Floyd"
    python populate_from_dbpedia.py --file artists.csv
    python populate_from_dbpedia.py --artists "Beyoncé" --dry-run
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict

# Agregar el directorio app al path
sys.path.insert(0, str(Path(__file__).parent))

from app.enrichment import OntologyEnrichment


def parse_arguments():
    """Parsear argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Poblar ontología musical con datos de DBpedia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --artists "The Beatles,Radiohead,Nirvana"
  %(prog)s --albums "OK Computer,The Wall"
  %(prog)s --file entities.csv
  %(prog)s --artists "Kendrick Lamar" --dry-run
        """
    )
    
    parser.add_argument(
        "--artists",
        type=str,
        help="Lista de artistas separados por comas"
    )
    
    parser.add_argument(
        "--albums",
        type=str,
        help="Lista de álbumes separados por comas"
    )
    
    parser.add_argument(
        "--songs",
        type=str,
        help="Lista de canciones separadas por comas (formato: 'Song - Artist')"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Archivo CSV con entidades (columnas: type,name,artist)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="data/music-ontology.owl",
        help="Ruta del archivo de salida (default: data/music-ontology.owl)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar qué se haría sin realizar cambios"
    )
    
    parser.add_argument(
        "--no-albums",
        action="store_true",
        help="No descargar álbumes automáticamente para artistas"
    )
    
    return parser.parse_args()


def print_header(text: str):
    """Imprimir encabezado formateado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_success(text: str):
    """Imprimir mensaje de éxito"""
    print(f"✓ {text}")


def print_error(text: str):
    """Imprimir mensaje de error"""
    print(f"✗ {text}")


def print_info(text: str):
    """Imprimir mensaje informativo"""
    print(f"ℹ {text}")


def parse_csv_file(filepath: str) -> List[Dict[str, str]]:
    """Parsear archivo CSV con entidades"""
    entities = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Saltar encabezado si existe
        start_idx = 1 if lines and 'type' in lines[0].lower() else 0
        
        for line in lines[start_idx:]:
            line = line.strip()
            if not line:
                continue
                
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) >= 2:
                entity = {
                    "type": parts[0],
                    "name": parts[1]
                }
                
                if len(parts) >= 3:
                    entity["artist"] = parts[2]
                    
                entities.append(entity)
        
        return entities
        
    except FileNotFoundError:
        print_error(f"Archivo no encontrado: {filepath}")
        return []
    except Exception as e:
        print_error(f"Error al leer archivo: {e}")
        return []


def main():
    """Función principal"""
    args = parse_arguments()
    
    # Validar que se especificó al menos una fuente de datos
    if not any([args.artists, args.albums, args.songs, args.file]):
        print_error("Debe especificar al menos una fuente de datos (--artists, --albums, --songs, o --file)")
        sys.exit(1)
    
    print_header("🎵 Poblador de Ontología Musical desde DBpedia")
    
    # Construir lista de entidades
    entities = []
    
    # Artistas
    if args.artists:
        for artist in args.artists.split(','):
            artist = artist.strip()
            if artist:
                entities.append({
                    "type": "artist",
                    "name": artist,
                    "fetch_albums": not args.no_albums
                })
    
    # Álbumes
    if args.albums:
        for album in args.albums.split(','):
            album = album.strip()
            if album:
                # Intentar parsear formato "Album - Artist"
                if ' - ' in album:
                    album_name, artist_name = album.split(' - ', 1)
                    entities.append({
                        "type": "album",
                        "name": album_name.strip(),
                        "artist": artist_name.strip()
                    })
                else:
                    entities.append({
                        "type": "album",
                        "name": album
                    })
    
    # Canciones
    if args.songs:
        for song in args.songs.split(','):
            song = song.strip()
            if song:
                # Intentar parsear formato "Song - Artist"
                if ' - ' in song:
                    song_name, artist_name = song.split(' - ', 1)
                    entities.append({
                        "type": "song",
                        "name": song_name.strip(),
                        "artist": artist_name.strip()
                    })
                else:
                    entities.append({
                        "type": "song",
                        "name": song
                    })
    
    # Archivo CSV
    if args.file:
        csv_entities = parse_csv_file(args.file)
        entities.extend(csv_entities)
    
    if not entities:
        print_error("No se encontraron entidades para procesar")
        sys.exit(1)
    
    print_info(f"Total de entidades a procesar: {len(entities)}\n")
    
    # Modo dry-run
    if args.dry_run:
        print_header("MODO DRY-RUN - Vista Previa")
        for i, entity in enumerate(entities, 1):
            entity_type = entity["type"]
            name = entity["name"]
            artist = entity.get("artist", "")
            
            if artist:
                print(f"{i}. {entity_type.upper()}: '{name}' por {artist}")
            else:
                print(f"{i}. {entity_type.upper()}: '{name}'")
        
        print("\n" + "-" * 70)
        print("Ejecutar sin --dry-run para realizar los cambios")
        sys.exit(0)
    
    # Inicializar servicio de enriquecimiento
    print_info(f"Cargando ontología desde: {args.output}")
    
    try:
        enrichment = OntologyEnrichment(args.output)
    except Exception as e:
        print_error(f"Error al cargar ontología: {e}")
        sys.exit(1)
    
    # Estadísticas iniciales
    initial_stats = enrichment.get_enrichment_stats()
    print_info(f"Estado inicial: {initial_stats['total_triples']} triplas\n")
    
    # Procesar entidades
    print_header("Procesando Entidades")
    
    successful = 0
    failed = 0
    errors = []
    
    for i, entity in enumerate(entities, 1):
        entity_type = entity["type"]
        name = entity["name"]
        artist = entity.get("artist")
        
        print(f"\n[{i}/{len(entities)}] Procesando {entity_type}: '{name}'...")
        
        try:
            if entity_type == "artist":
                fetch_albums = entity.get("fetch_albums", True)
                result = enrichment.enrich_artist(name, fetch_albums)
            elif entity_type == "album":
                result = enrichment.enrich_album(name, artist)
            elif entity_type == "song":
                result = enrichment.enrich_song(name, artist)
            else:
                print_error(f"Tipo desconocido: {entity_type}")
                failed += 1
                errors.append(f"Tipo desconocido: {entity_type}")
                continue
            
            if result["success"]:
                print_success(result["message"])
                print_info(f"  → {result['entities_added']} entidades, {result.get('triples_added', 0)} triplas agregadas")
                successful += 1
            else:
                print_error(result["message"])
                failed += 1
                errors.append(result["message"])
                
        except Exception as e:
            error_msg = f"Error procesando '{name}': {str(e)}"
            print_error(error_msg)
            failed += 1
            errors.append(error_msg)
    
    # Guardar ontología enriquecida
    if successful > 0:
        print("\n" + "-" * 70)
        print_info("Guardando ontología enriquecida...")
        
        if enrichment.save_enriched_ontology(args.output):
            print_success(f"Ontología guardada en: {args.output}")
        else:
            print_error("Error al guardar ontología")
    
    # Resumen final
    print_header("Resumen Final")
    
    final_stats = enrichment.get_enrichment_stats()
    
    print(f"Entidades procesadas:    {len(entities)}")
    print(f"  ✓ Exitosas:            {successful}")
    print(f"  ✗ Fallidas:            {failed}")
    print()
    print(f"Triplas iniciales:       {initial_stats['total_triples']}")
    print(f"Triplas finales:         {final_stats['total_triples']}")
    print(f"Triplas agregadas:       {final_stats['total_triples'] - initial_stats['total_triples']}")
    print()
    print(f"Artistas agregados:      {final_stats['artists_added']}")
    print(f"Álbumes agregados:       {final_stats['albums_added']}")
    print(f"Canciones agregadas:     {final_stats['songs_added']}")
    
    if errors:
        print("\n" + "-" * 70)
        print("Errores encontrados:")
        for error in errors[:10]:  # Mostrar solo primeros 10 errores
            print(f"  • {error}")
        
        if len(errors) > 10:
            print(f"  ... y {len(errors) - 10} errores más")
    
    print()
    
    if successful > 0:
        print_success("Proceso completado exitosamente")
    else:
        print_error("No se pudo agregar ninguna entidad")
        sys.exit(1)


if __name__ == "__main__":
    main()
