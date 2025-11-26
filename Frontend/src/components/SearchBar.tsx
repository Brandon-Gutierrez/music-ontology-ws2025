import React, { useState } from 'react';
import { Search, Users, Disc3, Music, Zap, Tag, Database, Globe, Zap as Lightning } from 'lucide-react';
import styles from '../styles/SearchBar.module.css';
import type { SearchMode } from '../types';

interface SearchBarProps {
  onSearch: (query: string, filter: string, mode: SearchMode) => void;
  isLoading: boolean;
}

type FilterType = 'all' | 'artist' | 'album' | 'song' | 'instrument' | 'genre';

interface FilterOption {
  value: FilterType;
  label: string;
  icon: React.ReactNode;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<FilterType>('all');
  const [searchMode, setSearchMode] = useState<SearchMode>('offline');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query, filter, searchMode);
    }
  };

  const filterOptions: FilterOption[] = [
    { value: 'all', label: 'Todos', icon: <Search size={18} /> },
    { value: 'artist', label: 'Artistas', icon: <Users size={18} /> },
    { value: 'album', label: 'Álbumes', icon: <Disc3 size={18} /> },
    { value: 'song', label: 'Canciones', icon: <Music size={18} /> },
    { value: 'instrument', label: 'Instrumentos', icon: <Zap size={18} /> },
    { value: 'genre', label: 'Géneros', icon: <Tag size={18} /> },
  ];

  const modeOptions = [
    { value: 'offline' as SearchMode, label: 'Local', icon: <Database size={16} />, tooltip: 'Búsqueda en ontología local' },
    { value: 'online' as SearchMode, label: 'DBpedia', icon: <Globe size={16} />, tooltip: 'Búsqueda en DBpedia (online)' },
    { value: 'hybrid' as SearchMode, label: 'Híbrido', icon: <Lightning size={16} />, tooltip: 'Búsqueda combinada (local + DBpedia)' },
  ];

  return (
    <div className={styles['search-bar']}>
      <form onSubmit={handleSearch}>
        <div className={styles['search-input-group']}>
          <input
            type="text"
            className={styles['search-input']}
            placeholder="Busca artistas, álbumes, canciones..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className={styles['search-button']}
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? 'Buscando...' : 'Buscar'}
          </button>
        </div>
      </form>

      {/* Modo de búsqueda */}
      <div className={styles['mode-selector']}>
        <span className={styles['mode-label']}>Modo:</span>
        {modeOptions.map((mode) => (
          <button
            key={mode.value}
            className={`${styles['mode-button']} ${searchMode === mode.value ? styles['mode-active'] : ''
              }`}
            onClick={() => setSearchMode(mode.value)}
            disabled={isLoading}
            title={mode.tooltip}
          >
            <span className={styles['mode-icon']}>{mode.icon}</span>
            <span>{mode.label}</span>
          </button>
        ))}
      </div>

      <div className={styles['filter-tabs']}>
        {filterOptions.map((option) => (
          <button
            key={option.value}
            className={`${styles['filter-tab']} ${filter === option.value ? styles.active : ''
              }`}
            onClick={() => setFilter(option.value)}
            disabled={isLoading}
          >
            <span className={styles['icon']}>{option.icon}</span>
            <span className={styles['label']}>{option.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
