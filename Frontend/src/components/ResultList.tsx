import React from 'react';
import type { SearchResult } from '../types';
import { ResultCard } from './ResultCard';
import styles from '../styles/ResultCard.module.css';

interface ResultListProps {
  results: SearchResult[];
  isLoading: boolean;
  error?: string;
  hasSearched: boolean;
}

export const ResultList: React.FC<ResultListProps> = ({
  results,
  isLoading,
  error,
  hasSearched,
}) => {
  if (isLoading) {
    return <div className={styles.loading}>⏳ Buscando resultados...</div>;
  }

  if (error) {
    return (
      <div className={styles.error}>
        ❌ Error: {error}
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className={styles['no-results']}>
        <div className={styles['no-results-icon']}>🎵</div>
        <p>Ingresa una búsqueda para comenzar a explorar la ontología musical</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className={styles['no-results']}>
        <div className={styles['no-results-icon']}>🔍</div>
        <p>No se encontraron resultados. Intenta con otro término de búsqueda.</p>
      </div>
    );
  }

  return (
    <div className={styles['results-container']}>
      {results.map((result) => (
        <ResultCard key={result.data.uri} result={result} />
      ))}
    </div>
  );
};
