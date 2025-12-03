# 🎵 Buscador Semántico de Música

Aplicación web moderna con búsqueda semántica en ontología RDF/OWL de música, con soporte multiidioma y dos modos de operación: **offline** (local) y **online** (DBpedia en vivo).

**Versión**: 4.0 | **Status**: ✅ Producción | **Idiomas**: 4 (EN, ES, FR, DE)

---

## 🌟 Características

✅ **Búsqueda Offline**: Rápida sin internet (ontología local + DBpedia descargado)  
✅ **Búsqueda Online**: Enriquecida en vivo con DBpedia  
✅ **Multiidioma**: Interfaz + URLs de DBpedia adaptadas (EN/ES/FR/DE)  
✅ **Diferenciación Visual**: Colores distintos por fuente de datos  
✅ **URLs Inteligentes**: Botones a DBpedia con dominio según idioma  
✅ **Deduplicación Automática**: Sin resultados duplicados  
✅ **Responsive**: Adaptable a cualquier dispositivo  

---

## 🚀 Inicio Rápido

### Requisitos

- Python 3.9+
- Node.js 20.19+ o 22.0+
- npm 10+

### 3 Pasos para Empezar

```bash
# Terminal 1: Backend
cd Backend
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd Frontend
npm install
npm run dev
```

✅ Abierto en `http://localhost:5173`

---

## 📂 Estructura

```
.
├── Backend/
│   ├── app/
│   │   ├── __init__.py        # FastAPI + CORS
│   │   ├── ontology.py        # Lógica búsqueda
│   │   ├── dbpedia_service.py # SPARQL queries
│   │   ├── models.py          # Pydantic models
│   │   └── routes.py          # 22 endpoints
│   ├── data/
│   │   ├── music-ontology.owl       # Local (618 triplas)
│   │   └── dbpedia-downloaded.owl   # Descargado (41 triplas)
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Cliente API
│   │   ├── i18n/              # Traducciones
│   │   └── styles/            # CSS Modules
│   ├── package.json
│   └── vite.config.ts
│
├── README.md
└── LICENSE
```

---

## 🔍 Ejemplos de Uso

### Búsqueda Offline

```bash
curl "http://127.0.0.1:8000/api/search?q=beatles&mode=offline"
```

**Respuesta**: 1 resultado de ontología local

### Búsqueda Online (Español)

```bash
curl "http://127.0.0.1:8000/api/search?q=beatles&mode=online&lang=es"
```

**Respuesta**: Resultados de DBpedia con URLs en `es.dbpedia.org`

### Búsqueda por Tipo

```bash
curl "http://127.0.0.1:8000/api/artists?q=john"
curl "http://127.0.0.1:8000/api/albums?q=abbey"
curl "http://127.0.0.1:8000/api/songs?q=imagine"
```

---

## 📚 Documentación

- **Backend**: Ver `Backend/README.md`
- **Frontend**: Ver `Frontend/README.md`

---

## 🔧 Tecnologías

### Backend
- **FastAPI** 0.121.2
- **RDFLib** 7.4.0
- **SPARQLWrapper** 2.0.0
- **Pydantic** 2.12.4

### Frontend
- **React** 18.3
- **TypeScript** 5.6
- **Vite** 5.3
- **i18next** 23.15

---

## 💡 Modos de Operación

### Offline Mode
```
Búsqueda → Ontología Local (618 triplas) + DBpedia Descargado (41 triplas)
Ventaja: Rápido, sin internet, determinista
Desventaja: Limitado a datos cargados
```

### Online Mode
```
Búsqueda → SPARQL DBpedia en Vivo + Deduplicación + URL adaptada por idioma
Ventaja: Acceso a millones de entidades, datos actualizados
Desventaja: Requiere internet, más lento
```

---

## 🌍 Idiomas

| Idioma | Código | DBpedia Domain |
|--------|--------|----------------|
| English | `en` | dbpedia.org |
| Español | `es` | es.dbpedia.org |
| Français | `fr` | fr.dbpedia.org |
| Deutsch | `de` | de.dbpedia.org |

---

## 📊 Datos Incluidos

### Ontología Local (618 triplas)
- 12 artistas
- 16 álbumes
- 20 canciones
- 10 instrumentos
- 8 géneros

### DBpedia Descargado (41 triplas)
- Datos preparados para búsqueda offline de DBpedia

---

## 🐛 Troubleshooting

**Backend no inicia**:
```bash
python -m pip install -r requirements.txt --upgrade
```

**Frontend da error CORS**:
- Backend tiene CORS habilitado automáticamente
- Verificar URL en `Frontend/.env.local`

**Puerto 8000 en uso**:
```bash
python -m uvicorn app:app --port 8001
```

---

## 📝 API Endpoints

| Endpoint | Descripción |
|----------|-------------|
| `GET /health` | Estado del servidor |
| `GET /api/search?q=...` | Búsqueda general |
| `GET /api/artists?q=...` | Buscar artistas |
| `GET /api/albums?q=...` | Buscar álbumes |
| `GET /api/songs?q=...` | Buscar canciones |
| `GET /docs` | Swagger UI |

---

## 📄 Licencia

Ver archivo `LICENSE`

---

**Versión**: 4.0  
**Última actualización**: 3 de diciembre de 2025  
**Estado**: ✅ Producción
