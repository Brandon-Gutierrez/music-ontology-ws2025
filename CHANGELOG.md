# Changelog - Music Ontology Web Semantic

## v3.0 - 19 de Noviembre de 2025

### ✨ Nuevas Características

#### Backend - Ontología Expandida
- **618 triplas RDF** (anterior: 336)
- **Nuevas propiedades de Artistas**:
  - `nationality` - Nacionalidad
  - `birthYear` - Año de nacimiento
  - `activeYears` - Años activo (ej: "1960-1980")
  - `trajectory` - Trayectoria profesional
  - `discography` - Listado de álbumes
  - `awards` - Premios y reconocimientos

- **Nuevas propiedades de Canciones**:
  - `language` - Idioma de la canción
  - `composers` - Compositores/Autores
  - `lyricist` - Letrista
  - `lyrics` - Letra o fragmento
  
- **Nuevas propiedades de Objeto**:
  - `collaboratesWith` - Colaboraciones entre artistas
  - `featuringArtist` - Artista invitado

#### Frontend - Componentes Mejorados
- **Visualización extendida de Artistas**:
  - Nacionalidad, año de nacimiento, años activos
  - Trayectoria expandible
  - Discografía completa
  - Premios y reconocimientos

- **Visualización extendida de Canciones**:
  - Idioma
  - Compositores y letristas
  - Letra con scroll y estilos especiales
  - Lenguaje visual mejorado

- **Nuevos estilos CSS**:
  - `.text-content` - Para contenido de texto largo
  - `.lyrics-content` - Para visualización de letras
  - Mejor manejo de word-wrap y overflow

### 📊 Datos Expandidos

| Elemento | v2.0 | v3.0 | Cambio |
|----------|------|------|--------|
| Artistas | 10 | 12 | +2 (Adele, Beyoncé) |
| Álbumes | 11 | 16 | +5 nuevos |
| Canciones | 16 | 20 | +4 nuevas |
| Instrumentos | 10 | 10 | Sin cambios |
| Géneros | 8 | 8 | Sin cambios |
| Triplas RDF | 336 | 618 | +282 (84% aumento) |

### 🔧 Cambios Técnicos

**Backend (app/ontology.py)**:
- Método `_entity_to_dict()` actualizado para procesar 6 nuevas propiedades de Artist
- Método `_entity_to_dict()` actualizado para procesar 4 nuevas propiedades de Song
- Manejo mejorado de tipos de datos (string, int, boolean)

**Frontend (src/)**:
- `types/index.ts` - Interfaces extendidas con 10 nuevas propiedades opcionales
- `components/ResultCard.tsx` - Renderización mejorada con secciones expandibles
- `styles/ResultCard.module.css` - 2 nuevas clases CSS para contenido largo

**Documentación**:
- `Backend/README.md` - Actualizado a v3.0 con nuevas propiedades
- `CHANGELOG.md` - Este archivo

### 🐛 Correcciones
- Escapado correcto de caracteres especiales en XML: `r&b` → `R&amp;B`
- Validación mejorada de propiedades opcionales

### 📈 Impacto

- **Cobertura de datos**: 84% más información semántica
- **Experiencia de usuario**: Visualización más rica y detallada
- **Casos de uso**: Búsqueda y filtrado más sofisticados ahora posibles

### 🔄 Compatibilidad

- ✅ API retrocompatible (nuevas propiedades son opcionales)
- ✅ Búsqueda sigue funcionando con texto anterior
- ✅ Clientes antiguos no se rompen con nuevas propiedades

### 📝 Notas

- La ontología OWL ahora incluye información biográfica completa de artistas
- Las canciones tienen metadatos completos incluyendo composición y letra
- Mejor preparación para futuras integraciones de análisis semántico
- Datos reales de artistas iconos de la música mundial

---

## v2.0 - Anterior

- Ontología base con 336 triplas
- UI redesignado con dark mode y tema verde
- Lucide React para iconografía
- Documentación completa README

---

**Fecha de Release**: 19 de Noviembre de 2025  
**Autor**: Brandon Gutierrez  
**Repository**: music-ontology-ws2025  
**License**: MIT
