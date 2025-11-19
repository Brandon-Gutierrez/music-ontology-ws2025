import { useState, useEffect } from 'react';
import './App.css';
import { Header } from './components/Header';
import { SearchBar } from './components/SearchBar';
import { ResultList } from './components/ResultList';
import type { SearchResult } from './types';
import { apiService } from './services/api';

function App() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [hasSearched, setHasSearched] = useState(false);
  const [apiStatus, setApiStatus] = useState<boolean | undefined>();

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

  const handleSearch = async (query: string, filter: string) => {
    setIsLoading(true);
    setError(undefined);
    setHasSearched(true);

    try {
      let searchResults: SearchResult[] = [];

      if (!query.trim()) {
        setError('Por favor ingresa un término de búsqueda');
        setResults([]);
        setIsLoading(false);
        return;
      }

      // Búsqueda general con filtro opcional
      searchResults = await apiService.search(query);

      // Aplicar filtro si no es "all"
      if (filter !== 'all') {
        searchResults = searchResults.filter((r) => r.type === filter);
      }

      if (searchResults.length === 0) {
        setError(`No se encontraron resultados para "${query}" en la categoría ${filter !== 'all' ? filter : 'general'}`);
      }

      setResults(searchResults);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Error al conectar con la API. Verifica que el servidor backend esté en ejecución.';
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

