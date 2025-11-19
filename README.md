# 🎵 Buscador Semántico de Música - Ontología RDF

Un buscador inteligente basado en ontologías RDF/OWL que permite explorar información sobre artistas, álbumes, canciones, instrumentos y géneros musicales.

## 🚀 Inicio Rápido

### Requisitos
- Python 3.9+
- Node.js 20.19+ o 22.12+
- npm

### Paso 1: Backend (FastAPI)

```bash
cd Backend
python run_server.py
```

El servidor estará disponible en: `http://127.0.0.1:8000`

### Paso 2: Frontend (React)

En otra terminal:

```bash
cd Frontend
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

---

## 📋 Estructura del Proyecto

```
music-ontology-ws2025/
├── Backend/
│   ├── app/
│   │   ├── __init__.py          # Configuración FastAPI
│   │   ├── main.py              # Entry point
│   │   ├── ontology.py          # Servicio RDF/OWL
│   │   ├── models.py            # Modelos Pydantic
│   │   └── routes.py            # Endpoints API
│   ├── data/
│   │   └── music-ontology.owl   # Ontología RDF
│   ├── requirements.txt         # Dependencias Python
│   └── run_server.py            # Script para iniciar servidor
│
├── Frontend/
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   ├── services/            # Cliente HTTP
│   │   ├── styles/              # CSS Modules
│   │   ├── types/               # TypeScript interfaces
│   │   └── App.tsx              # Componente principal
│   ├── .env.local               # Configuración
│   ├── package.json             # Dependencias Node.js
│   └── vite.config.ts           # Configuración Vite
│
├── QUICK_START.md               # Guía de inicio detallada
├── LICENSE                      # Licencia
└── README.md                    # Este archivo
```

---

## 🔍 Características

✅ **Búsqueda Semántica**: Busca inteligentemente en toda la ontología  
✅ **Filtros Especializados**: Busca por tipo (artistas, álbumes, canciones, etc.)  
✅ **Interfaz Responsiva**: Funciona perfectamente en desktop y móvil  
✅ **API REST Completa**: 22 endpoints para diferentes queries  
✅ **Documentación Interactiva**: Swagger UI en `/docs`

---

## 📊 Datos Actuales

La ontología contiene:
- **4 Artistas**: John Lennon, Paul McCartney, Miles Davis, Taylor Swift
- **4 Álbumes**: Abbey Road, A Kind of Blue, Fearless, Red
- **12 Canciones**: Distribuidas entre los álbumes
- **7 Instrumentos**: Guitar, Bass, Piano, Drums, Saxophone, Violin, Synth
- **4 Géneros**: Rock, Jazz, Pop, Classical
- **248 RDF Triplas**: Relaciones semánticas completas

---

## 🛠️ Tecnologías

**Backend**
- FastAPI 0.121.2 - Framework web moderno
- RDFlib 7.4.0 - Procesamiento RDF/OWL
- Pydantic 2.12.4 - Validación de datos
- Uvicorn 0.38.0 - Servidor ASGI

**Frontend**
- React 19.2.0 - UI framework
- TypeScript 5.9.3 - Type safety
- Vite 7.2.2 - Build tool
- Axios 1.13.2 - HTTP client
- CSS Modules - Styling

---

## 📖 Ejemplos de Uso

### Búsqueda General
```
Abre http://localhost:5173
Ingresa "john" en la búsqueda
Presiona Enter
→ Encontrará a John Lennon y sus relacionados
```

### Con Filtros
```
Busca "abbey" con filtro "Álbumes"
→ Mostrará solo el álbum Abbey Road

Busca "guitar" con filtro "Instrumentos"
→ Mostrará la guitarra y sus usos
```

---

## 🔗 URLs Principales

| Recurso | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://127.0.0.1:8000 |
| Swagger API | http://127.0.0.1:8000/docs |
| ReDoc API | http://127.0.0.1:8000/redoc |
| Health Check | http://127.0.0.1:8000/health |

---

## 📝 Licencia

Ver archivo `LICENSE` para más detalles.

---

**Estado**: ✅ Operativo y funcional
