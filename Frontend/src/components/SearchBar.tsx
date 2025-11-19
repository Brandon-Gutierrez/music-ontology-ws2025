import React, { useState } from 'react';
import { Search, Users, Disc3, Music, Zap, Tag } from 'lucide-react';
import styles from '../styles/SearchBar.module.css';

interface SearchBarProps {
  onSearch: (query: string, filter: string) => void;
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

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query, filter);
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

      <div className={styles['filter-tabs']}>
        {filterOptions.map((option) => (
          <button
            key={option.value}
            className={`${styles['filter-tab']} ${
              filter === option.value ? styles.active : ''
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
