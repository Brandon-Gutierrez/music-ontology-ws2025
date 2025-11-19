# Backend - Buscador Semántico de Música API

API REST basada en FastAPI que proporciona acceso semántico a una ontología RDF/OWL de música con 336 triplas.

**Versión**: 2.0 | **Status**: ✅ Operacional | **Endpoints**: 22

---

## 📋 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [API Endpoints](#api-endpoints)
5. [Estructura](#estructura)
6. [Módulos](#módulos)
7. [Ejemplos](#ejemplos)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes Python)

### Instalación en 2 Pasos

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servidor
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

✅ API disponible en: `http://127.0.0.1:8000`  
📚 Documentación interactiva: `http://127.0.0.1:8000/docs`

---

## 📦 Instalación Detallada

### Paso 1: Verificar Python

```bash
python --version      # Debe ser 3.9 o superior
pip --version         # Verificar que pip está instalado
```

Si no está instalado: https://www.python.org/downloads/

### Paso 2: Instalar Dependencias

```bash
# Instalación estándar
pip install -r requirements.txt

# En Windows, si falla:
python -m pip install -r requirements.txt

# En macOS/Linux:
pip3 install -r requirements.txt

# Si hay conflictos:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Paso 3: Iniciar Servidor

```bash
# Opción 1: Con reload automático (desarrollo)
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Opción 2: Sin reload (producción)
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Opción 3: Con especificación completa
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000 --log-level info
```

**Salida esperada**:
```
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     ✓ Ontología cargada: 336 triplas
```

---

## ⚙️ Configuración

### Variables de Entorno (Opcional)

Crear archivo `.env`:

```env
# Host y puerto
HOST=127.0.0.1
PORT=8000

# Modo de desarrollo
DEBUG=True

# Paths
ONTOLOGY_PATH=./data/music-ontology.owl
```

### Configuración CORS

✅ Ya configurado automáticamente para permitir todas las origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Para restringir orígenes en producción, editar `app/__init__.py`:

```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
],
```

---

## 📚 Estructura del Proyecto

```
Backend/
├── app/
│   ├── __init__.py              # Inicialización FastAPI + CORS
│   ├── main.py                  # Entry point (uvicorn.run)
│   ├── ontology.py              # OntologyService (296 líneas)
│   │                            # - Carga RDF/OWL
│   │                            # - Consultas semánticas
│   │                            # - 12 métodos principales
│   ├── models.py                # Modelos Pydantic (80 líneas)
│   │                            # - Artist, Album, Song
│   │                            # - Instrument, Genre
│   │                            # - SearchResult, ApiResponse
│   └── routes.py                # Endpoints (295 líneas)
│                                # - 22 endpoints REST
│                                # - Validación de entrada
│                                # - Manejo de errores
│
├── data/
│   └── music-ontology.owl       # Ontología RDF/OWL v2.0
│                                # - 336 triplas
│                                # - 5 clases
│                                # - 11 propiedades
│                                # - 53 instancias
│
├── requirements.txt             # Dependencias Python
├── README.md                    # Este archivo
└── .env.example                 # Template de variables
```

---

## 🔗 API Endpoints

### Health Check

```bash
GET /health

# Respuesta
{
  "status": "healthy"
}
```

### Búsqueda General

```bash
GET /api/search?q=john

# Parámetros
- q: string (requerido, mín. 1 carácter)

# Respuesta
{
  "success": true,
  "data": [
    {
      "type": "artist",
      "data": {
        "uri": "http://example.org/music-ontology#artist-john-lennon",
        "name": "John Lennon",
        "description": "...",
        "genre": "Rock"
      }
    }
  ],
  "message": "Se encontraron 5 resultados"
}
```

### Obtener Todos los Datos

```bash
# Artistas
GET /api/artists

# Álbumes
GET /api/albums

# Canciones
GET /api/songs

# Instrumentos
GET /api/instruments

# Géneros
GET /api/genres
```

### Búsqueda Específica por Tipo

```bash
GET /api/search/artists?q=taylor
GET /api/search/albums?q=abbey
GET /api/search/songs?q=love
GET /api/search/instruments?q=guitar
GET /api/search/genres?q=rock
```

### Relaciones

```bash
# Álbumes de un artista
GET /api/artist/{uri}/albums

# Canciones de un álbum
GET /api/album/{uri}/songs

# Instrumentos en una canción
GET /api/song/{uri}/instruments

# Canciones con instrumento específico
GET /api/instrument/{uri}/songs
```

### Estadísticas

```bash
GET /api/stats

# Respuesta
{
  "totalTriplas": 336,
  "artists": 10,
  "albums": 11,
  "songs": 16,
  "instruments": 10,
  "genres": 8,
  "ontologyVersion": "2.0"
}
```

### Documentación Interactiva

```bash
# Swagger UI
GET /docs

# ReDoc
GET /redoc

# OpenAPI JSON
GET /openapi.json
```

---

## 🧩 Módulos

### ontology.py

**OntologyService** - Gestor principal de la ontología RDF

```python
class OntologyService:
    def __init__(self, ontology_path: str)
    def _load_ontology()                    # Cargar OWL
    def _entity_to_dict(uri, type)          # Convertir RDF a dict
    def search(query)                       # Búsqueda general
    def search_artists(query)               # Buscar artistas
    def search_albums(query)                # Buscar álbumes
    def search_songs(query)                 # Buscar canciones
    def search_instruments(query)           # Buscar instrumentos
    def search_genres(query)                # Buscar géneros
    def get_all_artists()                   # Obtener todos
    def get_all_albums()                    # Obtener todos
    def get_all_songs()                     # Obtener todos
    def get_all_instruments()               # Obtener todos
    def get_all_genres()                    # Obtener todos
    def get_artist_albums(uri)              # Relaciones
    def get_album_songs(uri)                # Relaciones
    def get_song_instruments(uri)           # Relaciones
```

### models.py

**Modelos Pydantic** para validación

```python
class Artist(BaseModel):
    uri: str
    name: str
    description: str
    genre: Optional[str]

class Album(BaseModel):
    uri: str
    name: str
    description: str
    releaseYear: Optional[int]
    genre: Optional[str]

class Song(BaseModel):
    uri: str
    name: str
    description: str
    duration: Optional[int]
    releaseYear: Optional[int]
    instruments: Optional[List[Instrument]]

class SearchResult(BaseModel):
    type: str
    data: Union[Artist, Album, Song, Instrument, Genre]

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: List[T]
    message: str
```

### routes.py

**Endpoints REST** - 22 rutas principales

```python
# 3 Rutas de búsqueda general
router.get("/search")                   # GET /api/search?q=...
router.get("/search/artists")           # GET /api/search/artists?q=...
router.get("/search/albums")            # GET /api/search/albums?q=...
router.get("/search/songs")             # GET /api/search/songs?q=...
router.get("/search/instruments")       # GET /api/search/instruments?q=...
router.get("/search/genres")            # GET /api/search/genres?q=...

# 5 Rutas para obtener todos
router.get("/artists")                  # GET /api/artists
router.get("/albums")                   # GET /api/albums
router.get("/songs")                    # GET /api/songs
router.get("/instruments")              # GET /api/instruments
router.get("/genres")                   # GET /api/genres

# 4 Rutas de relaciones
router.get("/artist/{uri}/albums")      # GET /api/artist/{uri}/albums
router.get("/album/{uri}/songs")        # GET /api/album/{uri}/songs
router.get("/song/{uri}/instruments")   # GET /api/song/{uri}/instruments
router.get("/instrument/{uri}/songs")   # GET /api/instrument/{uri}/songs

# 2 Rutas de utilidad
router.get("/stats")                    # GET /api/stats
router.get("/health")                   # GET /health (En app/__init__.py)
```

---

## 📊 Datos de la Ontología

### Estadísticas

- **Triplas RDF**: 336 (v2.0)
- **Clases**: 5 (Artist, Album, Song, Instrument, Genre)
- **Propiedades**: 11 (hasAlbum, containsSong, usesInstrument, etc.)
- **Instancias**: 53

### Contenido

```
Artistas (10)
- John Lennon, Paul McCartney, Miles Davis, Taylor Swift
- David Bowie, Aretha Franklin, Bob Dylan, Björk
- Kendrick Lamar, Pink Floyd

Álbumes (11)
- Abbey Road, A Kind of Blue, Fearless, Red
- Hunky Dory, Ziggy Stardust, Young Gifted and Black
- Blonde on Blonde, Post, Good Kid m.A.A.d City
- The Dark Side of the Moon

Canciones (16)
- Come Together, Something, The End, So What, Blue in Green
- Love Story, You Belong With Me, All Too Well, We Are Never Ever
- Changes, Respect, Rainy Day Women, Time, Money

Instrumentos (10)
- Guitar, Bass, Piano, Drums, Saxophone
- Violin, Synth, Flute, Cello, Trumpet

Géneros (8)
- Rock, Jazz, Pop, Classical, Electronic
- Hip-Hop, Blues, Folk
```

---

## 💡 Ejemplos de Uso

### Con cURL

```bash
# Búsqueda general
curl "http://127.0.0.1:8000/api/search?q=john"

# Buscar artistas específicamente
curl "http://127.0.0.1:8000/api/search/artists?q=taylor"

# Obtener todos los álbumes
curl "http://127.0.0.1:8000/api/albums"

# Estadísticas
curl "http://127.0.0.1:8000/api/stats"

# Health check
curl "http://127.0.0.1:8000/health"
```

### Con Python

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Búsqueda general
response = requests.get(f"{BASE_URL}/api/search?q=john")
results = response.json()
print(results)

# Obtener artistas
artists = requests.get(f"{BASE_URL}/api/artists").json()
print(f"Artistas: {artists['data']}")

# Estadísticas
stats = requests.get(f"{BASE_URL}/api/stats").json()
print(f"Total triplas: {stats['data']['totalTriplas']}")
```

### Con JavaScript/TypeScript

```typescript
const API_URL = "http://127.0.0.1:8000";

// Búsqueda
const search = async (query: string) => {
  const response = await fetch(`${API_URL}/api/search?q=${query}`);
  return await response.json();
};

// Usar
const results = await search("john");
console.log(results);
```

---

## 🔧 Desarrollo

### Estructura de Desarrollo

```bash
# Terminal 1: Backend
cd Backend
python -m uvicorn app:app --reload

# Terminal 2: Frontend
cd Frontend
npm run dev

# Terminal 3: Tests (opcional)
python -m pytest tests/ -v
```

### Recargar Ontología

```bash
# La ontología se carga automáticamente en startup
# Para recargarla, reinicia el servidor:
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Agregar Nuevos Endpoints

Editar `app/routes.py`:

```python
@router.get("/api/mi-endpoint")
def mi_endpoint(param: str = Query(..., min_length=1)):
    """Descripción del endpoint"""
    try:
        resultado = ontology_service.mi_metodo(param)
        return ApiResponse(
            success=True,
            data=resultado,
            message="Éxito"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🐛 Troubleshooting

### "Module not found" - rdflib

```bash
pip install rdflib --upgrade
pip install -r requirements.txt --force-reinstall
```

### "Port 8000 already in use"

```bash
# Encontrar proceso usando puerto 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# O usar puerto diferente
python -m uvicorn app:app --port 8001
```

### "Ontología no encontrada"

```bash
# Verificar que archivo existe
ls Backend/data/music-ontology.owl

# Verificar ruta relativa es correcta
# La ruta debe ser relativa a donde se ejecuta uvicorn
```

### "CORS error" desde Frontend

✅ Ya está habilitado automáticamente  
Si persiste, editar `app/__init__.py`

### "Connection refused" desde Frontend

- Verificar backend está corriendo: `curl http://127.0.0.1:8000/health`
- Verificar URL en `.env.local` del frontend
- Reiniciar ambos servidores

### Lentitud en búsquedas

- Aumentar tamaño de caché RDF
- Usar índices en ontología
- Considerar índice Elasticsearch para grandes conjuntos

---

## 📦 Dependencias

Ver `requirements.txt`:

```
fastapi==0.121.2
uvicorn==0.38.0
rdflib==7.4.0
pydantic==2.12.4
python-multipart==0.0.6
```

Actualizar todas:

```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

---

## 🚀 Deployment

### Producción con Gunicorn

```bash
pip install gunicorn

gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Con Docker (opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t music-api .
docker run -p 8000:8000 music-api
```

---

## 📚 Recursos

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [RDFlib Docs](https://rdflib.readthedocs.io/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SPARQL/RDF](https://www.w3.org/TR/rdf-sparql-query/)

### Tutoriales
- [Building APIs with FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [RDF and OWL Tutorial](https://www.w3.org/RDF/)
- [Python SPARQL Queries](https://rdflib.readthedocs.io/en/stable/plugin_parsers.html)

---

**Última actualización**: 19 de noviembre de 2025  
**Versión**: 2.0  
**Status**: ✅ Totalmente funcional
