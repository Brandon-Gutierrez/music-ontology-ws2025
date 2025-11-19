# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

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
