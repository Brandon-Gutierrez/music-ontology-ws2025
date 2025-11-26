// Tipos para la ontología de música

export type SearchMode = 'offline' | 'online' | 'hybrid';
export type DataSource = 'local' | 'dbpedia';

export interface Artist {
  uri: string;
  name: string;
  description?: string;
  genre?: string;
  nationality?: string;
  birthYear?: number;
  activeYears?: string;
  trajectory?: string;
  discography?: string;
  awards?: string;
}

export interface Album {
  uri: string;
  name: string;
  description?: string;
  releaseYear?: number;
  genre?: string;
  songs?: Song[];
}

export interface Song {
  uri: string;
  name: string;
  description?: string;
  duration?: number;
  releaseYear?: number;
  artist?: string;
  instruments?: Instrument[];
  language?: string;
  composers?: string;
  lyrics?: string;
  lyricist?: string;
  collaborators?: Artist[];
}

export interface Instrument {
  uri: string;
  name: string;
  type?: string;
  description?: string;
}

export interface Genre {
  uri: string;
  name: string;
  description?: string;
}

export interface SearchResult {
  type: 'artist' | 'album' | 'song' | 'instrument' | 'genre';
  data: Artist | Album | Song | Instrument | Genre;
  source?: DataSource; // Nuevo campo para indicar fuente
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
  message?: string;
}

// Tipos para enriquecimiento desde DBpedia
export interface EnrichmentRequest {
  entity_type: 'artist' | 'album' | 'song';
  name: string;
  artist?: string;
  fetch_albums?: boolean;
}

export interface EnrichmentResponse {
  success: boolean;
  message: string;
  entities_added?: number;
  triples_added?: number;
  errors?: string[];
}

export interface EnrichmentStats {
  artists_added: number;
  albums_added: number;
  songs_added: number;
  total_triples_added: number;
  total_triples: number;
  artists_in_ontology: number;
  albums_in_ontology: number;
  songs_in_ontology: number;
  last_enrichment?: string;
}

