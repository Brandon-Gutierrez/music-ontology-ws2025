# 🎵 Buscador Semántico de Música - Ontología RDF

Un buscador inteligente basado en ontologías RDF/OWL que permite explorar información sobre artistas, álbumes, canciones, instrumentos y géneros musicales con una interfaz moderna con modo oscuro y tema verde.

**Versión**: 3.0 | **Estado**: ✅ Operacional | **Ontología**: 618 triplas RDF | **DBpedia**: ✅ Integrado

## 🌟 Nuevas Características v3.0

- 🌐 **Integración con DBpedia**: Acceso a millones de entidades musicales vía SPARQL
- 🔄 **Búsqueda Multi-Modo**: Local, Online (DBpedia) o Híbrida
- 📥 **Enriquecimiento de Ontología**: Poblar datos desde DBpedia mediante API o CLI
- ⚡ **Caché Inteligente**: Resultados de DBpedia cacheados para mejor rendimiento
- 🎯 **Selector Visual de Modo**: UI mejorada con iconos para cada modo de búsqueda

---

## 📋 Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Instalación Rápida](#instalación-rápida)
3. [Configuración Detallada](#configuración-detallada)
4. [Características](#características)
5. [Datos Actuales](#datos-actuales)
6. [API Endpoints](#api-endpoints)
7. [Uso](#uso)
8. [Estructura del Proyecto](#estructura-del-proyecto)
9. [Troubleshooting](#troubleshooting)
10. [Tecnologías](#tecnologías)

---

## 🔧 Requisitos

### Sistema Operativo
- Windows, macOS o Linux

### Software Requerido
- **Python**: 3.9 o superior
  - Verificar: `python --version`
  - Descargar: https://www.python.org/downloads/
  
- **Node.js**: 20.19+ o 22.0+ (LTS recomendado)
  - Verificar: `node --version` y `npm --version`
  - Descargar: https://nodejs.org/
  
- **Git**: (opcional pero recomendado)
  - Descargar: https://git-scm.com/

### Conexión a Internet (Opcional)
- **Requerida para**: Búsqueda en DBpedia y enriquecimiento de ontología
- **No requerida para**: Búsqueda local (modo offline)

---

## 🚀 Instalación Rápida

### Opción 1: Con Git (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/Brandon-Gutierrez/music-ontology-ws2025.git
cd music-ontology-ws2025

# Instalar dependencias Backend
cd Backend
pip install -r requirements.txt

# Instalar dependencias Frontend
cd ../Frontend
npm install
```

### Opción 2: Sin Git

1. Descargar proyecto como ZIP desde GitHub
2. Extraer el archivo
3. Seguir pasos de instalación de dependencias arriba

### Paso 1: Iniciar Backend

```bash
cd Backend
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Esperado ver**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     ✓ Ontología cargada: 618 triplas
```

✅ Backend listo en: `http://127.0.0.1:8000`

### Paso 2: Iniciar Frontend (Nueva Terminal)

```bash
cd Frontend
npm run dev
```

**Esperado ver**:
```
➜  Local:   http://localhost:5173/
```

✅ Frontend listo en: `http://localhost:5173`

### Paso 3: ¡Usa la Aplicación!

1. Abre `http://localhost:5173` en tu navegador
2. Prueba buscando: "john", "abbey", "guitar", etc.
3. Usa los filtros para buscar por tipo

---

## ⚙️ Configuración Detallada

### Variables de Entorno (Opcional)

Crea archivo `Frontend/.env.local` (si no existe):

```env
# URL del backend API
VITE_API_URL=http://localhost:8000

# Puerto frontend (por defecto 5173)
VITE_PORT=5173
```

### Solución de Problemas Comunes

#### ❌ Error: "pip: command not found"
```bash
# Windows
python -m pip install -r Backend/requirements.txt

# macOS/Linux
pip3 install -r Backend/requirements.txt
```

#### ❌ Error: "Port 8000 already in use"
```bash
# Usar puerto diferente
python -m uvicorn app:app --port 8001 --reload
```

#### ❌ Error: "CORS error" o "API connection failed"
- Verificar que el backend esté corriendo: `http://127.0.0.1:8000/health`
- Verificar que el frontend esté en `http://localhost:5173`
- No cambiar el puerto del backend sin actualizar `.env.local`

#### ❌ Error: "Module not found" en Python
```bash
cd Backend
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📋 Estructura del Proyecto

```
music-ontology-ws2025/
├── Backend/
│   ├── app/
│   │   ├── __init__.py              # Inicialización FastAPI
│   │   ├── main.py                  # Entry point
│   │   ├── ontology.py              # Servicio de consulta RDF/OWL
│   │   ├── models.py                # Modelos Pydantic para validación
│   │   └── routes.py                # 22 Endpoints de API REST
│   ├── data/
│   │   └── music-ontology.owl       # Ontología RDF v2.0 (336 triplas)
│   ├── requirements.txt             # Dependencias Python
│   └── README.md                    # Documentación Backend
│
├── Frontend/
│   ├── src/
│   │   ├── components/              # 4 Componentes React
│   │   │   ├── Header.tsx           # Encabezado con logo
│   │   │   ├── SearchBar.tsx        # Barra + filtros con iconos
│   │   │   ├── ResultCard.tsx       # Tarjeta de resultado
│   │   │   └── ResultList.tsx       # Grid de resultados
│   │   ├── services/
│   │   │   └── api.ts               # Cliente HTTP (20+ métodos)
│   │   ├── styles/                  # CSS Modules con dark mode
│   │   ├── types/
│   │   │   └── index.ts             # Tipos TypeScript
│   │   ├── App.tsx                  # Componente principal
│   │   ├── App.css                  # Estilos globales + variables CSS
│   │   ├── main.tsx                 # Entry point React
│   │   └── index.css                # Estilos base
│   ├── .env.local                   # Configuración (crear si no existe)
│   ├── package.json                 # Dependencias Node.js + scripts
│   ├── vite.config.ts               # Configuración Vite
│   ├── tsconfig.json                # Configuración TypeScript
│   └── README.md                    # Documentación Frontend
│
├── LICENSE                          # Licencia MIT
├── README.md                        # Este archivo
└── .gitignore                       # Archivos ignorados en Git
```

---

## ✨ Características

### 🎯 Búsqueda
- ✅ **Búsqueda Semántica**: Busca inteligentemente en toda la ontología (618 triplas)
- ✅ **Búsqueda Filtrada**: Por tipo de entidad (Artistas, Álbumes, Canciones, Instrumentos, Géneros)
- ✅ **Búsqueda Multi-Modo**: 
  - 🔌 **Local**: Búsqueda rápida en ontología local
  - 🌐 **DBpedia**: Acceso a millones de entidades musicales
  - ⚡ **Híbrida**: Combina resultados locales + DBpedia
- ✅ **Resultados Enriquecidos**: Información detallada de cada entidad
- ✅ **Indicador de Estado**: Muestra si el backend está conectado
- ✅ **Badges de Fuente**: Indica origen de cada resultado (Local/DBpedia)

### 🎨 Interfaz
- ✅ **Modo Oscuro**: Fondo oscuro con tema verde (#10B981 - #22C55E)
- ✅ **Iconos Profesionales**: Lucide React en lugar de emojis
- ✅ **Diseño Responsivo**: Perfecto en desktop, tablet y móvil
- ✅ **Gradientes Modernos**: Elementos visuales atractivos
- ✅ **Animaciones Suaves**: Transiciones y efectos hover

### 🔌 API
- ✅ **27+ Endpoints REST**: Acceso completo a la ontología y DBpedia
- ✅ **CORS Habilitado**: Funciona desde cualquier origen
- ✅ **Documentación Interactiva**: Swagger UI en `/docs` y ReDoc en `/redoc`
- ✅ **Health Check**: Endpoint para verificar estado
- ✅ **Endpoints de Enriquecimiento**: `/api/enrich`, `/api/enrich/batch`, `/api/enrich/stats`
- ✅ **Búsqueda con Modo**: Parámetro `mode` en `/api/search` (offline/online/hybrid)

### 📊 Ontología
- ✅ **618 Triplas RDF**: Relaciones semánticas completas (expandible vía DBpedia)
- ✅ **5 Clases**: Artist, Album, Song, Instrument, Genre
- ✅ **11 Propiedades**: hasAlbum, containsSong, usesInstrument, etc.
- ✅ **53+ Instancias**: 10 artistas, 11 álbumes, 16 canciones, 10 instrumentos, 8 géneros
- ✅ **Enriquecimiento Dinámico**: Agregar datos desde DBpedia sin editar OWL manualmente

---

## 📊 Datos Actuales (v2.0)

La ontología contiene:
- **10 Artistas**: John Lennon, Paul McCartney, Miles Davis, Taylor Swift, David Bowie, Aretha Franklin, Bob Dylan, Björk, Kendrick Lamar, Pink Floyd
- **11 Álbumes**: Abbey Road, A Kind of Blue, Fearless, Red, Hunky Dory, Ziggy Stardust, Young Gifted and Black, Blonde on Blonde, Post, Good Kid m.A.A.d City, The Dark Side of the Moon
- **16 Canciones**: Come Together, Something, The End, So What, Blue in Green, Love Story, You Belong With Me, All Too Well, We Are Never Ever, Changes, Respect, Rainy Day Women, Time, Money
- **10 Instrumentos**: Guitar, Bass, Piano, Drums, Saxophone, Violin, Synth, Flute, Cello, Trumpet
- **8 Géneros**: Rock, Jazz, Pop, Classical, Electronic, Hip-Hop, Blues, Folk
- **336 RDF Triplas**: Relaciones semánticas completas (+35% vs v1.0)

---

---

## 📖 Troubleshooting

### Frontend no carga
```bash
# Verificar que el servidor frontend esté corriendo
# Si no, en Frontend/:
npm run dev

# Limpiar cache
rm -rf node_modules
npm install
npm run dev
```

### Backend no responde
```bash
# Verificar que está corriendo
curl http://127.0.0.1:8000/health

# Si falla, reiniciar desde Backend/:
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### CORS Error
- ✅ Ya está configurado (CORS habilitado en el backend)
- Si persiste: Verificar que Frontend está en `http://localhost:5173` (no `127.0.0.1`)

### "Ontología no encontrada"
- Verificar que `Backend/data/music-ontology.owl` existe
- Reiniciar el backend para recargar la ontología

### Port already in use
```bash
# Windows - Encontrar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

---

## 🛠️ Tecnologías

### Backend
- **FastAPI 0.121.2** - Framework web async moderno
- **RDFlib 7.4.0** - Procesamiento RDF/OWL semántico
- **SPARQLWrapper 2.0.0** - Consultas SPARQL a DBpedia
- **Pydantic 2.12.4** - Validación de datos con tipos
- **Uvicorn 0.38.0** - Servidor ASGI de alto rendimiento
- **Python 3.9+** - Lenguaje de programación

### Frontend
- **React 19.2.0** - UI framework moderno
- **TypeScript 5.9.3** - Tipado estático para JavaScript
- **Vite 7.2.2** - Build tool ultrarrápido
- **Axios 1.13.2** - Cliente HTTP para API calls
- **Lucide React** - Iconografía profesional
- **CSS Modules** - Estilos encapsulados y componibles
- **Node.js 22.11.0** - Entorno de ejecución JavaScript

### Utilities
- **Git** - Control de versiones
- **npm** - Gestor de paquetes Node.js
- **pip** - Gestor de paquetes Python

---

## 🎮 Uso

### Ejemplos de Búsqueda

```
1. Búsqueda General
   - Abre: http://localhost:5173
   - Ingresa: "john"
   - Resultado: John Lennon, sus álbumes y canciones

2. Búsqueda Filtrada por Álbum
   - Selecciona filtro: "Álbumes"
   - Ingresa: "abbey"
   - Resultado: Abbey Road con detalles

3. Búsqueda por Instrumento
   - Selecciona filtro: "Instrumentos"
   - Ingresa: "guitar"
   - Resultado: Guitarra y todas sus usos en canciones

4. Búsqueda por Género
   - Selecciona filtro: "Géneros"
   - Ingresa: "rock"
   - Resultado: Todos los artistas y álbumes rock
```

### Filtros Disponibles

| Filtro | Busca |
|--------|-------|
| 🔍 Todos | En toda la ontología |
| 👥 Artistas | Solo artistas |
| 💿 Álbumes | Solo álbumes |
| 🎵 Canciones | Solo canciones |
| ⚡ Instrumentos | Solo instrumentos |
| 🏷️ Géneros | Solo géneros |

---

## 🔗 API Endpoints

### Búsqueda General
```bash
# Búsqueda local (por defecto)
GET /api/search?q=john

# Búsqueda en DBpedia
GET /api/search?q=beatles&mode=online

# Búsqueda híbrida (local + DBpedia)
GET /api/search?q=rock&mode=hybrid
```

### Enriquecimiento desde DBpedia
```bash
# Enriquecer un artista
POST /api/enrich
Body: {"entity_type": "artist", "name": "Radiohead", "fetch_albums": true}

# Enriquecimiento por lotes
POST /api/enrich/batch
Body: {"entities": [{"type": "artist", "name": "Nirvana"}, ...]}

# Obtener estadísticas de enriquecimiento
GET /api/enrich/stats

# Recargar ontología
POST /api/enrich/reload
```

### Por Tipo
```bash
GET /api/artists              # Todos los artistas
GET /api/albums               # Todos los álbumes
GET /api/songs                # Todas las canciones
GET /api/instruments          # Todos los instrumentos
GET /api/genres               # Todos los géneros
```

### Búsquedas Específicas
```bash
GET /api/search/artists?q=taylor       # Buscar artistas
GET /api/search/albums?q=abbey         # Buscar álbumes
GET /api/search/songs?q=love           # Buscar canciones
GET /api/search/instruments?q=guitar   # Buscar instrumentos
GET /api/search/genres?q=rock          # Buscar géneros
```

### Relaciones
```bash
GET /api/artist/{uri}/albums           # Álbumes de artista
GET /api/album/{uri}/songs             # Canciones de álbum
GET /api/song/{uri}/instruments        # Instrumentos en canción
```

### Utilitarios
```bash
GET /health                    # Estado del servidor
GET /api/stats                 # Estadísticas de la ontología
```

---

## 🌐 Enriquecimiento de Ontología con DBpedia

### Método 1: Script CLI (Recomendado para lotes)

```bash
cd Backend

# Agregar un artista
python populate_from_dbpedia.py --artists "Radiohead"

# Agregar múltiples artistas
python populate_from_dbpedia.py --artists "Nirvana,Foo Fighters,Pearl Jam"

# Agregar álbumes (con formato "Álbum - Artista")
python populate_from_dbpedia.py --albums "OK Computer - Radiohead,In Utero - Nirvana"

# Preview sin guardar (dry-run)
python populate_from_dbpedia.py --artists "Pink Floyd" --dry-run

# Desde archivo CSV
python populate_from_dbpedia.py --file entities.csv
```

**Formato CSV** (entities.csv):
```csv
type,name,artist
artist,Radiohead,
album,OK Computer,Radiohead
song,Creep,Radiohead
```

### Método 2: API REST

```bash
# Usando curl
curl -X POST http://localhost:8000/api/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type": "artist",
    "name": "Radiohead",
    "fetch_albums": true
  }'

# Enriquecimiento por lotes
curl -X POST http://localhost:8000/api/enrich/batch \
  -H "Content-Type: application/json" \
  -d '{
    "entities": [
      {"type": "artist", "name": "Nirvana"},
      {"type": "album", "name": "Nevermind", "artist": "Nirvana"}
    ]
  }'
```

### Método 3: Desde el Frontend (Próximamente)

Panel de enriquecimiento integrado en la interfaz web (en desarrollo).

---

## 🔍 Modos de Búsqueda

### Modo Local (Offline)
- ✅ Búsqueda rápida sin latencia
- ✅ Funciona sin conexión a internet
- ✅ Datos curados manualmente
- **Cuándo usar**: Cuando trabajas sin internet o solo necesitas datos locales

### Modo DBpedia (Online)
- ✅ Acceso a millones de entidades musicales
- ✅ Datos actualizados de Wikipedia
- ✅ Información rica y estructurada
- ⚠️ Requiere conexión a internet
- ⚠️ Latencia de 1-5 segundos
- **Cuándo usar**: Cuando buscas artistas/álbumes que no están en tu ontología local

### Modo Híbrido
- ✅ Combina resultados locales + DBpedia
- ✅ Máxima cobertura
- ✅ Elimina duplicados automáticamente
- ✅ Muestra origen de cada resultado
- **Cuándo usar**: Para obtener los mejores resultados posibles

---

## 📍 URLs Principales

| Recurso | URL | Descripción |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Aplicación web |
| **Backend** | http://127.0.0.1:8000 | API REST |
| **Swagger API** | http://127.0.0.1:8000/docs | Documentación interactiva |
| **ReDoc API** | http://127.0.0.1:8000/redoc | Documentación alternativa |
| **Health Check** | http://127.0.0.1:8000/health | Verificar estado del backend |

---

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para cambios significativos:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📚 Recursos Adicionales

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [RDFlib Docs](https://rdflib.readthedocs.io/)
- [Vite Docs](https://vitejs.dev/)

### Tutoriales
- [Búsqueda semántica con RDF](https://www.w3.org/RDF/)
- [Construcción de APIs con FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [React + TypeScript](https://react.dev/learn/typescript)

---

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en GitHub.

---

**Última actualización**: 26 de noviembre de 2025  
**Versión**: 3.0 (DBpedia Integration)  
**Estado**: ✅ Operacional y funcional  
**Nuevas Características**: 🌐 Búsqueda en DBpedia | 📥 Enriquecimiento de ontología | ⚡ Caché inteligente
