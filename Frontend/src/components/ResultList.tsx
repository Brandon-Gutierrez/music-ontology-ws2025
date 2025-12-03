import React from 'react';
import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation();

  if (isLoading) {
    return <div className={styles.loading}>⏳ {t('results.searching')}</div>;
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
        <p>{t('results.noSearch')}</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className={styles['no-results']}>
        <div className={styles['no-results-icon']}>🔍</div>
        <p>{t('results.noResults')}</p>
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
