# 🎵 GUÍA DE INICIO - BUSCADOR SEMÁNTICO DE MÚSICA

## 🚀 Inicio Rápido

### Opción 1: Iniciar ambos servidores en paralelo (RECOMENDADO)

#### Terminal 1 - Backend (FastAPI)
```bash
cd Backend
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```
El servidor estará disponible en: **http://127.0.0.1:8000**

#### Terminal 2 - Frontend (React + Vite)
```bash
cd Frontend
npm run dev
```
El frontend estará disponible en: **http://localhost:5173**

---

## 📋 Verificación

### ✅ Backend Verificado
- [ ] Terminal muestra: `✓ Ontología cargada: 618 triplas`
- [ ] Terminal muestra: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Accede a http://127.0.0.1:8000/docs para ver Swagger UI

### ✅ Frontend Verificado
- [ ] Terminal muestra: `VITE v7.2.2` con `Local: http://localhost:5173`
- [ ] Abre navegador en http://localhost:5173
- [ ] Verifica que el header dice "🟢 API conectada"
- [ ] Verás selector de modo (Local/DBpedia/Híbrido) sobre los filtros

---

## 🔍 Pruebas de Búsqueda

Una vez que ambos servidores estén corriendo:

### Búsquedas de Ejemplo - Modo Local

1. **Buscar "john"** (encontrará a John Lennon)
2. **Buscar "abbey"** (encontrará Abbey Road)
3. **Buscar "rock"** (encontrará canciones de rock)
4. **Buscar "guitar"** (encontrará instrumentos y canciones)

### Búsquedas de Ejemplo - Modo DBpedia

1. **Selecciona modo "DBpedia"** en el selector
2. **Buscar "radiohead"** (consultará DBpedia)
3. **Buscar "beatles"** (obtendrá datos de Wikipedia/DBpedia)
4. **Buscar "pink floyd"** (información completa desde DBpedia)

### Búsquedas de Ejemplo - Modo Híbrido

1. **Selecciona modo "Híbrido"**
2. **Buscar "rock"** (combinará resultados locales y DBpedia)
3. Verás badges indicando la fuente de cada resultado

### Con Filtros

- **Todos** 🔍: Búsqueda general en toda la ontología
- **Artistas** 🎤: Solo busca artistas
- **Álbumes** 💿: Solo busca álbumes
- **Canciones** 🎵: Solo busca canciones
- **Instrumentos** 🎸: Solo busca instrumentos
- **Géneros** 🎼: Solo busca géneros

---

## 🌐 Enriquecimiento con DBpedia

### Agregar Artistas a tu Ontología

```bash
cd Backend

# Agregar un artista con sus álbumes
python populate_from_dbpedia.py --artists "Radiohead"

# Agregar múltiples artistas
python populate_from_dbpedia.py --artists "Nirvana,Foo Fighters,Pearl Jam"

# Preview sin guardar
python populate_from_dbpedia.py --artists "Pink Floyd" --dry-run
```

Después de enriquecer, **reinicia el backend** para que cargue los nuevos datos.

---

## 🛠️ Troubleshooting

### El frontend dice "🔴 API desconectada"

1. Verifica que el backend esté corriendo
2. Abre http://127.0.0.1:8000/health en el navegador
3. Deberías ver: `{"status":"healthy"}`
4. Si no, reinicia el backend

### Las búsquedas no devuelven resultados

1. Verifica la ortografía (la búsqueda es sensible a mayúsculas)
2. Intenta términos más generales (ej: "john" en lugar de "john lennon")
3. Abre http://127.0.0.1:8000/docs y prueba los endpoints manualmente

### Error de CORS

Si ves errores de CORS en la consola:
1. Verifica que el backend está en `127.0.0.1:8000`
2. Verifica que el frontend está en `localhost:5173`
3. Los CORS ya están configurados, no debería haber problemas

### Búsqueda DBpedia muy lenta

1. Es normal: consultas a DBpedia pueden tardar 1-5 segundos
2. Los resultados se cachean por 1 hora
3. La segunda búsqueda del mismo término será más rápida
4. Usa modo "Local" si prefieres velocidad sobre cobertura

### El enriquecimiento no encuentra la entidad

1. Verifica la ortografía exacta del nombre
2. DBpedia usa nombres en inglés (ej: "The Beatles" no "Los Beatles")
3. Prueba con nombres alternativos o más conocidos
4. Usa `--dry-run` para ver qué encontraría antes de guardar

---

## 🔗 URLs Principales

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://127.0.0.1:8000 |
| API Docs (Swagger) | http://127.0.0.1:8000/docs |
| API Docs (ReDoc) | http://127.0.0.1:8000/redoc |
| Health Check | http://127.0.0.1:8000/health |
| Enrichment Stats | http://127.0.0.1:8000/api/enrich/stats |

---

## 📝 Estructura del Proyecto

```
music-ontology-ws2025/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── ontology.py           # Servicio de búsqueda
│   │   ├── dbpedia_service.py    # Consultas SPARQL 
│   │   ├── enrichment.py         # Enriquecimiento 
│   │   ├── models.py             # Modelos Pydantic
│   │   └── routes.py             # 27+ Endpoints REST
│   ├── data/
│   │   └── music-ontology.owl    # Ontología RDF (618 triplas)
│   ├── requirements.txt          # Incluye SPARQLWrapper
│   ├── populate_from_dbpedia.py  # Script CLI 
│   └── test_api.py
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.tsx     # Con selector de modo 
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.ts            # Cliente HTTP (25+ métodos)
│   │   ├── types/
│   │   │   └── index.ts          # Tipos + DBpedia types
│   │   └── App.tsx               # searchWithMode 
│   ├── package.json
│   └── vite.config.ts
└── README.md                      # Documentación completa
```

---

## 💡 Tips

- Mantén ambas terminales abiertas durante el desarrollo
- Los cambios en el backend requieren reinicio
- Los cambios en el frontend se recargan automáticamente (HMR)
- Para ver logs del servidor backend, consulta la terminal
- **Modo Local** es el más rápido para búsquedas frecuentes
- **Modo DBpedia** es ideal para descubrir nuevos artistas
- **Modo Híbrido** combina lo mejor de ambos mundos
- Usa el script CLI para poblar tu ontología con datos de artistas populares

---

## 🌟 Características 

✅ **Búsqueda Multi-Modo**: Local, Online (DBpedia) o Híbrida  
✅ **Enriquecimiento Fácil**: Script CLI y API para poblar datos  
✅ **Caché Inteligente**: Resultados de DBpedia cacheados  
✅ **UI**: Selector visual de modo con iconos  
✅ **27+ Endpoints**: API extendida con enriquecimiento  

---

**¡Listo para comenzar a buscar! 🚀**
