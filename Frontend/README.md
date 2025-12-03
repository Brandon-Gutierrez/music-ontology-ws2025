# Frontend - Buscador Semántico de Música

Interfaz web moderna construida con React + TypeScript para búsquedas semánticas en ontología de música con soporte multiidioma.

**Versión**: 4.0 | **Status**: ✅ Producción | **Idiomas**: 4 (EN, ES, FR, DE) | **Modo**: Offline/Online

---

## 🚀 Inicio Rápido

### Requisitos

- Node.js 20.19+ o 22.0+ LTS
- npm 10+
- Backend corriendo en `http://127.0.0.1:8000`

### 2 Pasos para Empezar

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev
```

✅ Aplicación disponible en: `http://localhost:5173`

---

## 📦 Instalación

### Verificar Requisitos

```bash
node --version    # Debe ser 20.19+ o 22.0+
npm --version     # Debe ser 10+
```

### Instalar Dependencias

```bash
npm install
```

### Iniciar

```bash
# Desarrollo (con hot reload)
npm run dev

# Build producción
npm run build

# Preview producción
npm run preview
```

---

## ⚙️ Configuración

### Variables de Entorno (.env.local)

```env
VITE_API_URL=http://localhost:8000
```

### Cambiar Puerto

```bash
npm run dev -- --port 3000
```

---

## 🗂️ Estructura

```
src/
├── components/
│   ├── Header.tsx              # Encabezado
│   ├── SearchBar.tsx           # Campo búsqueda
│   ├── LanguageSelector.tsx    # Selector idioma
│   ├── ResultList.tsx          # Lista resultados
│   └── ResultCard.tsx          # Tarjeta resultado
│
├── services/
│   └── api.ts                  # Cliente HTTP
│
├── i18n/
│   ├── config.ts               # Configuración i18n
│   └── locales/
│       ├── en.json
│       ├── es.json
│       ├── fr.json
│       └── de.json
│
├── styles/
│   └── *.module.css            # Estilos CSS Modules
│
├── types/
│   └── index.ts                # TypeScript types
│
├── App.tsx                     # Componente principal
├── main.tsx                    # Entry point
└── index.css                   # Estilos globales
```

---

## 🎨 Características

✅ **Búsqueda Offline**: Rápida sin internet  
✅ **Búsqueda Online**: Enriquecida con DBpedia  
✅ **Multiidioma**: EN/ES/FR/DE con traductor  
✅ **Modo Oscuro**: Tema automático  
✅ **Responsive**: Adaptable a dispositivos  
✅ **URLs Inteligentes**: Botones a DBpedia por idioma  

---

## 🔍 Uso

### Búsqueda Offline

1. Selecciona "Offline" en la barra de búsqueda
2. Escribe el término a buscar
3. Presiona Enter o haz clic en buscar

**Resultados**: Datos locales + DBpedia descargado

### Búsqueda Online

1. Selecciona "Online" en la barra de búsqueda
2. Elige el idioma (EN/ES/FR/DE)
3. Escribe el término
4. Presiona Enter

**Resultados**: Búsqueda en vivo en DBpedia con URLs adaptadas al idioma

### Cambiar Idioma

Usa el selector en la esquina superior derecha:
- 🇬🇧 English
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch

---

## 📊 Ejemplos de Búsqueda

| Término | Offline | Online |
|---------|---------|--------|
| "beatles" | 1 resultado local | 6+ resultados DBpedia |
| "taylor" | Resultados locales | Enriquecidos en vivo |
| "john" | Artistas con "john" | Búsqueda global DBpedia |

---

## 🔧 Scripts

```bash
npm run dev       # Desarrollo con hot reload
npm run build     # Build para producción
npm run preview   # Preview de build
npm run lint      # Validar código ESLint
```

---

## 📦 Dependencias Principales

- **React 18.3** - Framework UI
- **TypeScript 5.6** - Type safety
- **Vite 5.3** - Build tool
- **i18next 23.15** - Internacionalización
- **Lucide Icons 0.344** - Iconografía
- **CSS Modules** - Estilos scoped

---

## 🌍 Idiomas Soportados

### English (en)
- Búsqueda: "Search"
- Offline/Online: "Offline" / "Online"

### Español (es)
- Búsqueda: "Buscar"
- Offline/Online: "Desconectado" / "En Línea"

### Français (fr)
- Recherche: "Rechercher"
- Hors ligne/En ligne: "Hors ligne" / "En ligne"

### Deutsch (de)
- Suche: "Suchen"
- Offline/Online: "Offline" / "Online"

---

## 🎯 Estructura de Datos

### Resultado (SearchResult)

```typescript
{
  type: "artist" | "album" | "song" | "genre",
  source: "local" | "dbpedia_downloaded" | "dbpedia_live",
  data: {
    uri: string,
    name: string,
    description?: string,
    dbpediaUrl?: string  // Solo en online
  }
}
```

---

## 🐛 Troubleshooting

**Error "Cannot GET /"**:
```bash
npm run dev
```

**Backend conexión rechazada**:
- Verificar backend corre en `http://127.0.0.1:8000`
- Verificar `.env.local` tiene `VITE_API_URL` correcto

**Cambios no se reflejan**:
```bash
npm run build
npm run preview
```

**CORS error**:
✅ Backend ya tiene CORS habilitado

---

## 📝 Notas

- **Estilos**: CSS Modules para evitar conflictos
- **Multiidioma**: i18next para traducciones
- **API**: Cliente centralizado en `services/api.ts`
- **Tipos**: TypeScript para seguridad
- **Build**: Vite para rendimiento

---

**Versión**: 4.0  
**Última actualización**: 3 de diciembre de 2025
