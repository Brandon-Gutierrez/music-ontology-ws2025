import React from 'react';
import { Users, Disc3, Music, Zap, Tag, ExternalLink } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { SearchResult, Artist, Album, Song, Instrument, Genre, DataSource } from '../types';
import styles from '../styles/ResultCard.module.css';

interface ResultCardProps {
  result: SearchResult;
}

const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
};

const getIconByType = (type: string): React.ReactNode => {
  const icons: Record<string, React.ReactNode> = {
    artist: <Users size={20} />,
    album: <Disc3 size={20} />,
    song: <Music size={20} />,
    instrument: <Zap size={20} />,
    genre: <Tag size={20} />,
  };
  return icons[type] || <Music size={20} />;
};

export const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  const { type, data, source } = result;
  const icon = getIconByType(type);
  const { t } = useTranslation();

  // Generar label de tipo traducido
  const typeLabel = t(`entity.${type}`);

  // Generar label de fuente traducida
  const sourceLabel = t(`results.source.${source || 'local'}`);

  // Función para obtener clase CSS según fuente
  const getSourceClass = (src: DataSource | string | undefined): string => {
    const sourceMap: Record<string, string> = {
      'local': 'source-local',
      'dbpedia_downloaded': 'source-downloaded',
      'dbpedia_live': 'source-live'
    };
    return sourceMap[src || 'local'] || 'source-local';
  };

  const renderArtistContent = (artist: Artist) => (
    <>
      <p className={styles['result-card-description']}>{artist.description}</p>
      <div className={styles['result-card-details']}>
        {artist.nationality && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.nationality')}</span>
            <span className={styles['detail-value']}>{artist.nationality}</span>
          </div>
        )}
        {artist.birthYear && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.birthYear')}</span>
            <span className={styles['detail-value']}>{artist.birthYear}</span>
          </div>
        )}
        {artist.activeYears && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.activeYears')}</span>
            <span className={styles['detail-value']}>{artist.activeYears}</span>
          </div>
        )}
      </div>
      {artist.trajectory && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.trajectory')}</div>
          <p className={styles['text-content']}>{artist.trajectory}</p>
        </div>
      )}
      {artist.discography && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.discography')}</div>
          <p className={styles['text-content']}>{artist.discography}</p>
        </div>
      )}
      {artist.awards && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.awards')}</div>
          <p className={styles['text-content']}>{artist.awards}</p>
        </div>
      )}
      {artist.genre && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.genre')}</div>
          <div className={styles.tags}>
            <span className={`${styles.badge} ${styles.genre}`}>{artist.genre}</span>
          </div>
        </div>
      )}
    </>
  );

  const renderAlbumContent = (album: Album) => (
    <>
      <p className={styles['result-card-description']}>{album.description}</p>
      <div className={styles['result-card-details']}>
        {album.releaseYear && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.releaseYear')}</span>
            <span className={styles['detail-value']}>{album.releaseYear}</span>
          </div>
        )}
        {album.genre && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.genre')}</span>
            <span className={styles['detail-value']}>{album.genre}</span>
          </div>
        )}
      </div>
    </>
  );

  const renderSongContent = (song: Song) => (
    <>
      <p className={styles['result-card-description']}>{song.description}</p>
      <div className={styles['result-card-details']}>
        {song.duration && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.duration')}</span>
            <span className={styles['detail-value']}>
              {formatDuration(song.duration)}
            </span>
          </div>
        )}
        {song.releaseYear && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.releaseYear')}</span>
            <span className={styles['detail-value']}>{song.releaseYear}</span>
          </div>
        )}
        {song.language && (
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.language')}</span>
            <span className={styles['detail-value']}>{song.language}</span>
          </div>
        )}
      </div>
      {song.composers && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.composers')}</div>
          <p className={styles['text-content']}>{song.composers}</p>
        </div>
      )}
      {song.lyricist && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.lyricist')}</div>
          <p className={styles['text-content']}>{song.lyricist}</p>
        </div>
      )}
      {song.lyrics && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.lyrics')}</div>
          <p className={styles['lyrics-content']}>{song.lyrics}</p>
        </div>
      )}
      {song.instruments && song.instruments.length > 0 && (
        <div className={styles['tags-container']}>
          <div className={styles['tags-title']}>{t('properties.instruments')}</div>
          <div className={styles.tags}>
            {song.instruments.map((instr) => (
              <span
                key={instr.uri}
                className={`${styles.badge} ${styles.instrument}`}
              >
                {instr.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </>
  );

  const renderInstrumentContent = (instrument: Instrument) => (
    <>
      <p className={styles['result-card-description']}>{instrument.description}</p>
      {instrument.type && (
        <div className={styles['result-card-details']}>
          <div className={styles['detail-row']}>
            <span className={styles['detail-label']}>{t('properties.type')}</span>
            <span className={styles['detail-value']}>{instrument.type}</span>
          </div>
        </div>
      )}
    </>
  );

  const renderGenreContent = (genre: Genre) => (
    <p className={styles['result-card-description']}>{genre.description}</p>
  );

  const renderContent = () => {
    switch (type) {
      case 'artist':
        return renderArtistContent(data as Artist);
      case 'album':
        return renderAlbumContent(data as Album);
      case 'song':
        return renderSongContent(data as Song);
      case 'instrument':
        return renderInstrumentContent(data as Instrument);
      case 'genre':
        return renderGenreContent(data as Genre);
      default:
        return null;
    }
  };

  return (
    <div className={styles['result-card']}>
      <div className={styles['result-card-header']}>
        <div className={styles['result-header-left']}>
          <div className={styles['result-icon']}>{icon}</div>
          <div>
            <h3 className={styles['result-card-title']}>{data.name}</h3>
            <div className={styles['result-meta']}>
              <small className={styles['result-card-type']}>{typeLabel}</small>
              <span className={`${styles['source-badge']} ${styles[getSourceClass(source)]}`}>
                {sourceLabel}
              </span>
            </div>
          </div>
        </div>
        {(source === 'dbpedia_live' || source === 'dbpedia_downloaded') && ('dbpediaUrl' in data) && data.dbpediaUrl && (
          <a
            href={data.dbpediaUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={styles['dbpedia-button']}
            title={t('results.viewInDBpedia')}
          >
            <ExternalLink size={18} />
            <span>{t('results.viewInDBpedia')}</span>
          </a>
        )}
      </div>
      {renderContent()}
    </div>
  );
};
