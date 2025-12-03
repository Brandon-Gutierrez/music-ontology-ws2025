# 🎵 Inicio Rápido

## 🚀 3 Pasos para Empezar

### Terminal 1: Backend

```bash
cd Backend
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**Esperado**: `Uvicorn running on http://127.0.0.1:8000`

✅ Backend: **http://127.0.0.1:8000**

### Terminal 2: Frontend

```bash
cd Frontend
npm install
npm run dev
```

**Esperado**: `Local: http://localhost:5173`

✅ Frontend: **http://localhost:5173**

---

## ✅ Verificación

### Backend
- [ ] API en `http://127.0.0.1:8000`
- [ ] Docs en `http://127.0.0.1:8000/docs`
- [ ] Health: `curl http://127.0.0.1:8000/health`

### Frontend
- [ ] Abierto en `http://localhost:5173`
- [ ] Selector de idioma visible (arriba derecha)
- [ ] Campo de búsqueda funciona

---

## 🔍 Pruebas

### Modo Offline

1. Selecciona "Offline"
2. Busca: "beatles", "john", "abbey", "rock"
3. Resultados: color **verde** (local) o **azul** (descargado)

### Modo Online

1. Selecciona "Online"
2. Elige idioma (EN/ES/FR)
3. Busca: "beatles", "taylor swift", "miles davis"
4. Resultados con enlace a DBpedia en el idioma seleccionado

---

## 🌍 Idiomas

- 🇬🇧 English
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch

---

## 📚 Documentación Completa

- **Backend**: Ver `Backend/README.md`
- **Frontend**: Ver `Frontend/README.md`
- **Proyecto**: Ver `README.md`
