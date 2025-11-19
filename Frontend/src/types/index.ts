// Tipos para la ontología de música

export interface Artist {
  uri: string;
  name: string;
  description?: string;
  genre?: string;
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
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}
