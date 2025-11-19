import React from 'react';
import { Music } from 'lucide-react';
import styles from '../styles/Header.module.css';

interface HeaderProps {
  apiStatus?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ apiStatus }) => {
  return (
    <header className={styles.header}>
      <div className={styles['header-logo']}>
        <Music size={32} />
      </div>
      <h1 className={styles['header-title']}>Buscador Semántico de Música</h1>
      <p className={styles['header-subtitle']}>
        Explora ontologías musicales con búsqueda semántica
      </p>
      <div className={styles['header-divider']}></div>
      <p className={styles['header-description']}>
        Descubre artistas, álbumes, canciones, instrumentos y géneros mediante búsqueda inteligente
      </p>
      {apiStatus !== undefined && (
        <p className={styles['status-text']} data-status={apiStatus ? 'connected' : 'disconnected'}>
          {apiStatus ? '✓ API conectada (http://127.0.0.1:8000)' : '✗ API desconectada - Asegúrate de que el servidor backend esté corriendo'}
        </p>
      )}
    </header>
  );
};
