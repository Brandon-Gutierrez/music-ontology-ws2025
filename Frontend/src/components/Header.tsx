import React from 'react';
import { Music } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { LanguageSelector } from './LanguageSelector';
import styles from '../styles/Header.module.css';

interface HeaderProps {
  apiStatus?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ apiStatus }) => {
  const { t } = useTranslation();

  return (
    <header className={styles.header}>
      <div className={styles['header-logo']}>
        <Music size={32} />
        <LanguageSelector />
      </div>
      <h1 className={styles['header-title']}>{t('app.title')}</h1>
      <p className={styles['header-subtitle']}>
        {t('app.subtitle')}
      </p>
      <div className={styles['header-divider']}></div>
      <p className={styles['header-description']}>
        {t('app.description')}
      </p>
      {apiStatus !== undefined && (
        <p className={styles['status-text']} data-status={apiStatus ? 'connected' : 'disconnected'}>
          {apiStatus ? `✓ ${t('header.status.connected')} (http://127.0.0.1:8000)` : `✗ ${t('header.status.disconnected')} - ${t('header.status.backendWarning')}`}
        </p>
      )}
    </header>
  );
};
