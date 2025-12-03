# Backend - Buscador Semántico de Música API

API REST basada en FastAPI que proporciona búsqueda semántica en ontología RDF/OWL de música. Soporta búsqueda en **modo offline** (local + datos descargados) y **modo online** (DBpedia en vivo).

**Versión**: 4.0 | **Status**: ✅ Producción | **Endpoints**: 22 | **Idiomas**: 4 (EN, ES, FR, DE)

---

## 📋 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Instalación](#instalación)
3. [Uso](#uso)
4. [API Endpoints](#api-endpoints)
5. [Estructura](#estructura)
6. [Ejemplos](#ejemplos)

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes Python)

### 2 Pasos para Empezar

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servidor
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

✅ API disponible en: `http://127.0.0.1:8000`  
📚 Docs interactivos: `http://127.0.0.1:8000/docs`

---

## 📦 Instalación

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Iniciar Servidor

```bash
# Desarrollo (con reload automático)
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Producción
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Paso 3: Verificar

```bash
curl http://127.0.0.1:8000/health
```

---

## 💡 Uso

### Búsqueda Offline

```bash
curl "http://127.0.0.1:8000/api/search?q=beatles&mode=offline"
```

**Fuentes de datos**:
- Ontología Local: 618 triplas
- DBpedia Descargado: 41 triplas

### Búsqueda Online

```bash
curl "http://127.0.0.1:8000/api/search?q=beatles&mode=online&lang=en"
```

**Parámetros**:
- `lang`: `en` | `es` | `fr` | `de` (DBpedia URL será del idioma indicado)

### Búsqueda por Tipo

```bash
curl "http://127.0.0.1:8000/api/artists?q=john"
curl "http://127.0.0.1:8000/api/albums?q=abbey"
curl "http://127.0.0.1:8000/api/songs?q=hey"
```

---

## 📚 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Estado del servidor |
| `/api/search` | GET | Búsqueda general multimodal |
| `/api/artists` | GET | Buscar/listar artistas |
| `/api/albums` | GET | Buscar/listar álbumes |
| `/api/songs` | GET | Buscar/listar canciones |
| `/api/genres` | GET | Buscar/listar géneros |
| `/docs` | GET | Swagger UI |

---

## 🗂️ Estructura

```
app/
├── __init__.py              # Configuración FastAPI + CORS
├── main.py                  # Entry point
├── ontology.py              # Búsqueda semántica offline/online
├── dbpedia_service.py       # Queries SPARQL a DBpedia
├── models.py                # Modelos Pydantic
└── routes.py                # 22 endpoints REST

data/
├── music-ontology.owl       # Ontología local (618 triplas)
└── dbpedia-downloaded.owl   # Datos DBpedia descargados

requirements.txt             # Dependencias
```

---

## 📊 Características

✅ **Modo Offline**: Búsqueda rápida sin internet  
✅ **Modo Online**: Enriquecimiento con DBpedia Live  
✅ **Multiidioma**: Soporte EN/ES/FR/DE  
✅ **URLs Inteligentes**: DBpedia URLs adaptan idioma  
✅ **Deduplicación**: Automática en modo online  
✅ **CORS Habilitado**: Listo para frontend  
✅ **Timeout SPARQL**: 10 segundos para queries  

---

## 🔍 Ejemplo de Respuesta

**Request**: `GET /api/search?q=beatles&mode=offline`

```json
{
  "success": true,
  "data": [
    {
      "type": "artist",
      "source": "local",
      "data": {
        "uri": "http://example.org/music-ontology#beatles",
        "name": "The Beatles",
        "origin": "Liverpool, England",
        "yearFormed": 1960
      }
    }
  ],
  "count": 1
}
```

---

## 🔧 Dependencias

```
fastapi==0.121.2        # Framework REST
uvicorn==0.38.0         # Servidor ASGI
rdflib==7.4.0           # Procesamiento RDF/OWL
pydantic==2.12.4        # Validación de datos
SPARQLWrapper==2.0.0    # Queries SPARQL
```

---

## 🐛 Troubleshooting

**Puerto en uso**:
```bash
python -m uvicorn app:app --port 8001
```

**Ontología no encontrada**:
```bash
# Verificar que existe data/music-ontology.owl
# Reiniciar servidor
```

**CORS error**:
✅ Ya habilitado automáticamente en `app/__init__.py`

---

## 📝 Notas

- **Offline Mode**: Respuestas rápidas, sin dependencia de internet
- **Online Mode**: Búsqueda enriquecida con DBpedia, requiere conexión
- **CORS**: Habilitado para desarrollo (cualquier origen)
- **Timeout**: 10 segundos para queries SPARQL
- **Deduplicación**: Automática en modo online

---

**Versión**: 4.0  
**Última actualización**: 3 de diciembre de 2025
