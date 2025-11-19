# Frontend - Buscador Semántico de Música

Interfaz web moderna construida con React y TypeScript para realizar búsquedas semánticas en la ontología de música.

**Versión**: 2.0 | **Status**: ✅ Operacional | **Dark Mode**: ✅ Activo

---

## 📋 Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso](#uso)
5. [Estructura](#estructura)
6. [Componentes](#componentes)
7. [Servicios](#servicios)
8. [Estilos](#estilos)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Node.js 20.19+ o 22.0+ LTS
- npm 10.9.0+
- Backend corriendo en `http://127.0.0.1:8000`

### Instalación en 2 Pasos

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev
```

✅ La aplicación estará disponible en: `http://localhost:5173`

---

## 📦 Instalación Detallada

### Paso 1: Verificar Requisitos

```bash
node --version      # Debe ser 20.19+ o 22.0+
npm --version       # Debe ser 10+
```

### Paso 2: Instalar Dependencias

```bash
# Instalación normal
npm install

# Si tienes problemas, intenta:
npm install --legacy-peer-deps

# Para actualizar a versiones más nuevas:
npm update
```

### Paso 3: Configuración de Entorno

Crear archivo `.env.local` en la raíz de Frontend (opcional):

```env
# URL del backend API
VITE_API_URL=http://localhost:8000

# Puerto del frontend (por defecto 5173)
VITE_PORT=5173

# Modo de desarrollo
VITE_NODE_ENV=development
```

---

## 🎮 Uso

### Desarrollo Local

```bash
# Iniciar servidor con hot reload
npm run dev
```

Abre `http://localhost:5173` en tu navegador.

### Build para Producción

```bash
# Compilar archivos optimizados
npm run build

# Previewizar la compilación
npm run preview
```

### Linting

```bash
# Verificar código
npm run lint

# Arreglar problemas automáticamente
npm run lint --fix
```

---

## 🏗️ Estructura del Proyecto

```
Frontend/src/
├── components/
│   ├── Header.tsx           # Encabezado (logo, título, estado API)
│   ├── SearchBar.tsx        # Búsqueda + filtros con iconos
│   ├── ResultCard.tsx       # Tarjeta individual de resultado
│   └── ResultList.tsx       # Grid container de resultados
│
├── services/
│   └── api.ts              # Cliente HTTP centralizado (20+ métodos)
│
├── styles/
│   ├── Header.module.css   # Estilos encapsulados Header
│   ├── SearchBar.module.css # Estilos SearchBar con dark mode
│   └── ResultCard.module.css # Estilos ResultCard + grid
│
├── types/
│   └── index.ts            # Definiciones TypeScript
│
├── App.tsx                 # Componente principal (lógica de búsqueda)
├── App.css                 # Estilos globales + variables CSS
├── main.tsx                # Entry point React
├── index.css               # Base styles
│
├── assets/                 # Recursos estáticos (si existen)
│
├── vite.config.ts          # Configuración Vite
├── tsconfig.json           # Configuración TypeScript
├── package.json            # Dependencias
├── .env.local              # Variables de entorno (no versionar)
├── .env.example            # Template de .env.local
└── README.md               # Este archivo
```

---

## 🧩 Componentes

### Header

**Ubicación**: `src/components/Header.tsx`

Muestra:
- 🎵 Logo del buscador
- Título y descripción
- Estado de conexión con API (✓ conectado o ✗ desconectado)

**Props**:
```typescript
interface HeaderProps {
  apiStatus?: boolean;  // true si conectado, false si no
}
```

### SearchBar

**Ubicación**: `src/components/SearchBar.tsx`

Proporciona:
- Input para ingreso de búsqueda
- 6 botones de filtro con iconos:
  - 🔍 Todos
  - 👥 Artistas
  - 💿 Álbumes
  - 🎵 Canciones
  - ⚡ Instrumentos
  - 🏷️ Géneros
- Estados de carga y habilitación

**Props**:
```typescript
interface SearchBarProps {
  onSearch: (query: string, filter: string) => void;
  isLoading: boolean;
}
```

### ResultCard

**Ubicación**: `src/components/ResultCard.tsx`

Renderiza tarjeta individual con:
- Icono del tipo
- Nombre de la entidad
- Descripción
- Información específica según tipo:
  - **Artista**: Género que interpreta
  - **Álbum**: Año, género
  - **Canción**: Duración, año, instrumentos
  - **Instrumento**: Tipo
  - **Género**: Descripción

**Props**:
```typescript
interface ResultCardProps {
  result: SearchResult;
}
```

### ResultList

**Ubicación**: `src/components/ResultList.tsx`

Contenedor grid que maneja:
- Estado de carga
- Lista vacía / sin resultados
- Errores
- Grid responsive

**Props**:
```typescript
interface ResultListProps {
  results: SearchResult[];
  isLoading: boolean;
  error?: string;
}
```

---

## 🔌 Servicios

### API Service

**Ubicación**: `src/services/api.ts`

Cliente HTTP centralizado con método base y 20+ métodos específicos:

#### Métodos Principales

```typescript
// Verificar conexión
await api.healthCheck()          // GET /health

// Búsqueda general
await api.search(query)          // GET /api/search?q=...

// Obtener todos
await api.getArtists()           // GET /api/artists
await api.getAlbums()            // GET /api/albums
await api.getSongs()             // GET /api/songs
await api.getInstruments()       // GET /api/instruments
await api.getGenres()            // GET /api/genres

// Búsqueda específica
await api.searchArtists(query)   // GET /api/search/artists?q=...
await api.searchAlbums(query)    // GET /api/search/albums?q=...
await api.searchSongs(query)     // GET /api/search/songs?q=...
await api.searchInstruments(query) // GET /api/search/instruments?q=...
await api.searchGenres(query)    // GET /api/search/genres?q=...

// Relaciones
await api.getArtistAlbums(uri)   // GET /api/artist/{uri}/albums
await api.getAlbumSongs(uri)     // GET /api/album/{uri}/songs
await api.getSongInstruments(uri) // GET /api/song/{uri}/instruments

// Estadísticas
await api.getStats()             // GET /api/stats
```

---

## 🎨 Estilos

### Sistema de Variables CSS

**Archivo**: `src/App.css`

Variables globales para dark mode + tema verde:

```css
:root {
  --bg-primary: #0f172a;           /* Fondo principal oscuro */
  --bg-secondary: #1e293b;         /* Fondo secundario */
  --bg-tertiary: #334155;          /* Fondo terciario */
  --color-green-primary: #10b981;  /* Verde esmeralda */
  --color-green-bright: #22c55e;   /* Verde lima */
  --color-green-dark: #16a34a;     /* Verde bosque */
  --text-primary: #f1f5f9;         /* Texto principal */
  --text-secondary: #cbd5e1;       /* Texto secundario */
  --border-color: #334155;         /* Bordes */
}
```

### CSS Modules

Cada componente tiene su módulo CSS encapsulado:

- **Header.module.css** - 40 líneas
- **SearchBar.module.css** - 100+ líneas
- **ResultCard.module.css** - 150+ líneas

### Paleta de Colores

| Uso | Color | Código |
|-----|-------|--------|
| Fondo Principal | Azul Oscuro | #0F172A |
| Verde Primario | Esmeralda | #10B981 |
| Verde Acento | Lima | #22C55E |
| Texto Principal | Gris Claro | #F1F5F9 |
| Bordes | Gris Oscuro | #334155 |
| Error | Rojo | #EF4444 |

---

## 📝 Scripts Disponibles

```bash
npm run dev              # Inicia servidor de desarrollo con HMR
npm run build            # Compila para producción
npm run preview          # Previewiza build local
npm run lint             # Valida código con ESLint
npm run lint --fix       # Arregla problemas automáticamente
npm run type-check       # Verifica tipos TypeScript
npm run clean            # Limpia cache de Vite
```

---

## 🐛 Troubleshooting

### "Port 5173 already in use"

```bash
# Usar puerto diferente
npm run dev -- --port 3000
```

### "Cannot find module" error

```bash
# Limpiar e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### "CORS error" o "API not responding"

1. Verificar que backend está corriendo: `http://127.0.0.1:8000/health`
2. Revisar `.env.local` - URL debe ser exacta
3. Reiniciar ambos servidores

### Cambios no se reflejan

```bash
# Limpiar cache de Vite
npm run clean
npm run dev
```

### Build falla

```bash
# Verificar tipos
npm run type-check

# Limpiar e reconstruir
rm -rf dist
npm run build
```

---

## 🚀 Optimizaciones

- ✅ Dark mode completo
- ✅ Iconos profesionales (Lucide React)
- ✅ Variables CSS para fácil mantenimiento
- ✅ Estilos encapsulados con CSS Modules
- ✅ Componentes funcionales con hooks
- ✅ Tipado completo con TypeScript
- ✅ Responsive design mobile-first
- ✅ Hot reload en desarrollo

---

## 📚 Recursos

### Documentación
- [React 19 Docs](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Documentation](https://vitejs.dev/)
- [Lucide React Icons](https://lucide.dev/)

---

**Última actualización**: 19 de noviembre de 2025  
**Versión**: 2.0  
**Status**: ✅ Funcional y optimizado

# Frontend - Buscador Semántico de Música

## Descripción

Frontend desarrollado con React y TypeScript que proporciona una interfaz intuitiva para realizar búsquedas semánticas en la ontología de música.

## Estructura del Proyecto

```
Frontend/src/
├── components/           # Componentes React
│   ├── Header.tsx       # Encabezado de la aplicación
│   ├── SearchBar.tsx    # Barra de búsqueda con filtros
│   ├── ResultCard.tsx   # Tarjeta individual de resultado
│   └── ResultList.tsx   # Contenedor de resultados
├── services/            # Servicios de API
│   └── api.ts          # Cliente HTTP para comunicación con backend
├── styles/             # Módulos CSS
│   ├── Header.module.css
│   ├── SearchBar.module.css
│   └── ResultCard.module.css
├── types/              # Tipos TypeScript
│   └── index.ts       # Definiciones de tipos
├── App.tsx            # Componente principal
├── App.css            # Estilos globales
├── main.tsx           # Entry point
└── index.css          # Estilos base (CSS-in-JS)
```

## Características

### 🔍 Búsqueda Semántica
- Búsqueda general en toda la ontología
- Filtrado por tipo de entidad (Artistas, Álbumes, Canciones, Instrumentos, Géneros)
- Autocompletado y sugerencias

### 🎯 Filtros Disponibles
- **Todos**: Busca en toda la ontología
- **🎤 Artistas**: Busca solo artistas
- **💿 Álbumes**: Busca solo álbumes
- **🎵 Canciones**: Busca solo canciones
- **🎸 Instrumentos**: Busca solo instrumentos
- **🎼 Géneros**: Busca solo géneros

### 📱 Características de la UI
- Interfaz responsiva (mobile, tablet, desktop)
- Diseño moderno con gradientes y sombras
- Tarjetas de resultados con información detallada
- Estado de carga y manejo de errores
- Indicador de conexión con API

### 💎 Tarjetas de Resultados
Cada tarjeta muestra:
- Ícono y tipo de entidad
- Nombre y descripción
- Información específica:
  - **Artistas**: Género que interpreta
  - **Álbumes**: Año de lanzamiento, género
  - **Canciones**: Duración, año, instrumentos utilizados
  - **Instrumentos**: Tipo de instrumento
  - **Géneros**: Descripción

## Instalación

```bash
cd Frontend
npm install
```

## Variables de Entorno

Crear archivo `.env.local`:

```
VITE_API_URL=http://localhost:8000
```

## Desarrollo

```bash
npm run dev
```

La aplicación se abrirá en `http://localhost:5173`

## Build

```bash
npm run build
```

## Linting

```bash
npm run lint
```

## Preview

```bash
npm run preview
```

## Dependencias Principales

- **React 19**: Framework UI
- **TypeScript**: Tipado estático
- **Vite**: Build tool
- **Axios**: Cliente HTTP
- **CSS Modules**: Estilos encapsulados

## Arquitectura

### Componentes

#### Header
- Muestra el título y descripción de la aplicación
- Indica estado de conexión con la API

#### SearchBar
- Input para ingreso de consulta
- Botones de filtro para seleccionar tipo de búsqueda
- Estados de carga y deshabilitación

#### ResultCard
- Tarjeta individual de resultado
- Renderizado condicional según tipo de entidad
- Muestra información relevante para cada tipo

#### ResultList
- Contenedor grid de tarjetas
- Maneja estados: cargando, sin resultados, error
- Proporciona retroalimentación al usuario

### Servicios

#### API Service
- Cliente HTTP centralizado
- Métodos para cada tipo de búsqueda
- Endpoints:
  - `GET /health` - Verificar conexión
  - `GET /api/search` - Búsqueda general
  - `GET /api/artists` - Obtener artistas
  - `GET /api/albums` - Obtener álbumes
  - `GET /api/songs` - Obtener canciones
  - `GET /api/instruments` - Obtener instrumentos
  - `GET /api/genres` - Obtener géneros
  - Y más métodos específicos para búsquedas filtradas

### Tipos

- `Artist`, `Album`, `Song`, `Instrument`, `Genre` - Modelos de datos
- `SearchResult` - Resultado de búsqueda con tipo y datos
- `ApiResponse<T>` - Respuesta genérica de API

## Estilos

Utilizamos CSS Modules para encapsulación de estilos:
- **Header.module.css**: Estilos del encabezado
- **SearchBar.module.css**: Estilos de barra de búsqueda
- **ResultCard.module.css**: Estilos de tarjetas y resultados
- **App.css**: Estilos globales

### Paleta de Colores

- **Gradiente principal**: #667eea → #764ba2
- **Fondo neutral**: #ffffff
- **Texto primario**: #333333
- **Texto secundario**: #666666 / #999999
- **Acentos**: #667eea, #764ba2
- **Estados**: Verde (#388e3c), Rojo (#ff6b6b), Naranja (#e65100)

## Responsive Design

- **Desktop**: Grid de 3-4 columnas
- **Tablet**: Grid de 2 columnas
- **Mobile**: Grid de 1 columna

## Mejoras Futuras

- [ ] Detalles expandibles en tarjetas
- [ ] Historial de búsquedas
- [ ] Favoritos/Marcadores
- [ ] Búsqueda avanzada con operadores
- [ ] Visualización de relaciones entre entidades
- [ ] Exportación de resultados
- [ ] Tema oscuro
- [ ] Modo offline
- [ ] Paginación de resultados

---

**Última actualización**: 18 de noviembre de 2025

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
