import React, { useState } from 'react';
import { Search, Users, Disc3, Music, Zap, Tag, Database, Globe } from 'lucide-react';
import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query, filter, searchMode);
    }
  };

  const filterOptions: FilterOption[] = [
    { value: 'all', label: t('search.filter.all'), icon: <Search size={18} /> },
    { value: 'artist', label: t('search.filter.artist'), icon: <Users size={18} /> },
    { value: 'album', label: t('search.filter.album'), icon: <Disc3 size={18} /> },
    { value: 'song', label: t('search.filter.song'), icon: <Music size={18} /> },
    { value: 'instrument', label: t('search.filter.instrument'), icon: <Zap size={18} /> },
    { value: 'genre', label: t('search.filter.genre'), icon: <Tag size={18} /> },
  ];

  const modeOptions = [
    { value: 'offline' as SearchMode, label: t('search.mode.offline'), icon: <Database size={16} />, tooltip: t('search.mode.offlineTooltip') },
    { value: 'online' as SearchMode, label: t('search.mode.online'), icon: <Globe size={16} />, tooltip: t('search.mode.onlineTooltip') },
  ];

  return (
    <div className={styles['search-bar']}>
      <form onSubmit={handleSearch}>
        <div className={styles['search-input-group']}>
          <input
            type="text"
            className={styles['search-input']}
            placeholder={t('search.placeholder')}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className={styles['search-button']}
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? t('search.searching') : t('search.button')}
          </button>
        </div>
      </form>

      {/* Modo de búsqueda */}
      <div className={styles['mode-selector']}>
        <span className={styles['mode-label']}>{t('search.mode.label')}</span>
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
