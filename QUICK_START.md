# 🎵 GUÍA DE INICIO - BUSCADOR SEMÁNTICO DE MÚSICA

## 🚀 Inicio Rápido

### Opción 1: Iniciar ambos servidores en paralelo (RECOMENDADO)

#### Terminal 1 - Backend (FastAPI)
```bash
cd Backend
python run_server.py
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
- [ ] Terminal muestra: `✓ Ontología cargada: 248 triplas`
- [ ] Terminal muestra: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Accede a http://127.0.0.1:8000/docs para ver Swagger UI

### ✅ Frontend Verificado
- [ ] Terminal muestra: `VITE v7.2.2` con `Local: http://localhost:5173`
- [ ] Abre navegador en http://localhost:5173
- [ ] Verifica que el header dice "🟢 API conectada"

---

## 🔍 Pruebas de Búsqueda

Una vez que ambos servidores estén corriendo:

### Búsquedas de Ejemplo

1. **Buscar "john"** (encontrará a John Lennon)
2. **Buscar "abbey"** (encontrará Abbey Road)
3. **Buscar "rock"** (encontrará canciones de rock)
4. **Buscar "guitar"** (encontrará instrumentos y canciones)

### Con Filtros

- **Todos** 🔍: Búsqueda general en toda la ontología
- **Artistas** 🎤: Solo busca artistas
- **Álbumes** 💿: Solo busca álbumes
- **Canciones** 🎵: Solo busca canciones
- **Instrumentos** 🎸: Solo busca instrumentos
- **Géneros** 🎼: Solo busca géneros

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


## 🔗 URLs Principales

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://127.0.0.1:8000 |
| API Docs | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |

---

## 📝 Estructura del Proyecto

```
music-ontology-ws2025/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── ontology.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── data/
│   │   └── music-ontology.owl
│   ├── requirements.txt
│   ├── run_server.py
│   └── test_api.py
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.tsx
│   ├── .env.local
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## 💡 Tips

- Mantén ambas terminales abiertas durante el desarrollo
- Los cambios en el backend requieren reinicio
- Los cambios en el frontend se recargan automáticamente (HMR)
- Para ver logs del servidor backend, consulta la terminal

---

**¡Listo para comenzar a buscar! 🚀**
