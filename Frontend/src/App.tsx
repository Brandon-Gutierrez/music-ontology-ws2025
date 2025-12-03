import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import './App.css';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { ResultList } from './components/ResultList';
import type { SearchResult, SearchMode } from './types';
import { apiService } from './services/api';

function App() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [hasSearched, setHasSearched] = useState(false);
  const [apiStatus, setApiStatus] = useState<boolean | undefined>();
  const { i18n, t } = useTranslation();

  // Verificar estado de la API al cargar
  useEffect(() => {
    const checkApi = async () => {
      try {
        const isHealthy = await apiService.healthCheck();
        setApiStatus(isHealthy);
      } catch (err) {
        console.error('Failed to check API health:', err);
        setApiStatus(false);
      }
    };

    checkApi();
  }, []);

  const handleSearch = async (query: string, filter: string, mode: SearchMode = 'offline') => {
    setIsLoading(true);
    setError(undefined);
    setHasSearched(true);

    try {
      let searchResults: SearchResult[] = [];

      if (!query.trim()) {
        setError(t('errors.emptySearch'));
        setResults([]);
        setIsLoading(false);
        return;
      }

      // Búsqueda con modo seleccionado y idioma actual
      searchResults = await apiService.searchWithMode(query, mode, i18n.language);

      // Aplicar filtro si no es "all"
      if (filter !== 'all') {
        searchResults = searchResults.filter((r) => r.type === filter);
      }

      if (searchResults.length === 0) {
        setError(`No se encontraron resultados para "${query}" en la categoría ${filter !== 'all' ? filter : 'general'} (modo: ${mode})`);
      }

      setResults(searchResults);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : t('errors.apiConnection');
      setError(message);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Header apiStatus={apiStatus} />
      <div className="container">
        <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        <ResultList
          results={results}
          isLoading={isLoading}
          error={error}
          hasSearched={hasSearched}
        />
      </div>
    </div>
  );
}

export default App;

