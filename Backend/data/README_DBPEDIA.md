# DBpedia Downloaded Data

Este archivo contiene datos descargados desde DBpedia para uso local sin conexión a internet.

## Contenido

El archivo `dbpedia-downloaded.owl` contiene las siguientes entidades descargadas de DBpedia:

### Artistas (5)
- Madonna
- Coldplay
- Adele
- Ed Sheeran
- The Beatles

### Álbumes (4)
- Thriller
- Abbey Road
- 21
- A Head Full of Dreams

### Canciones (4)
- Bohemian Rhapsody
- Imagine
- Hello
- Viva la Vida

## Cómo se marcan los datos

Todas las entidades descargadas de DBpedia tienen la propiedad `dataSource` con el valor `"dbpedia_downloaded"` para distinguirlas de:
- **Datos locales**: `dataSource = "local"` (datos creados manualmente en la ontología)
- **Datos en vivo**: `source = "dbpedia_live"` (resultados de consultas SPARQL en tiempo real)

## Interfaz de Usuario

En la interfaz, cada tipo de fuente se muestra con un badge de color distintivo:
- 🟢 **Verde** - Ontología Local (datos propios)
- 🔵 **Azul** - DBpedia Descargado (datos offline de DBpedia)
- 🟣 **Morado** - DBpedia en Vivo (consultas en tiempo real)

## Descargar Más Datos

Para descargar más entidades de DBpedia, ejecuta:

```bash
python download_dbpedia_data.py --language en --merge
```

### Opciones disponibles:
- `--language` / `-l`: Idioma de las consultas (en, es, fr, de). Por defecto: en
- `--merge` / `-m`: Combinar automáticamente con la ontología principal

### Ejemplo en español:
```bash
python download_dbpedia_data.py --language es --merge
```

## Nota Importante

Se crea automáticamente un archivo de respaldo (`music-ontology.owl.backup`) antes de combinar los datos descargados con la ontología principal.
