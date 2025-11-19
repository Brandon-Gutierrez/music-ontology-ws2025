import axios from 'axios';
import type { SearchResult, ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await api.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },

  // Búsqueda semántica general
  search: async (query: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        '/api/search',
        { params: { q: query } }
      );
      return response.data.data;
    } catch (error) {
      console.error('Search error:', error);
      throw error;
    }
  },

  // Obtener todos los artistas
  getArtists: async (): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>('/api/artists');
      return response.data.data;
    } catch (error) {
      console.error('Get artists error:', error);
      throw error;
    }
  },

  // Obtener artista por URI
  getArtistById: async (uri: string): Promise<SearchResult> => {
    try {
      const response = await api.get<ApiResponse<SearchResult>>(
        `/api/artists/${encodeURIComponent(uri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get artist error:', error);
      throw error;
    }
  },

  // Obtener todos los álbumes
  getAlbums: async (): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>('/api/albums');
      return response.data.data;
    } catch (error) {
      console.error('Get albums error:', error);
      throw error;
    }
  },

  // Obtener álbumes por artista
  getAlbumsByArtist: async (artistUri: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/albums/artist/${encodeURIComponent(artistUri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get albums by artist error:', error);
      throw error;
    }
  },

  // Obtener álbum por URI
  getAlbumById: async (uri: string): Promise<SearchResult> => {
    try {
      const response = await api.get<ApiResponse<SearchResult>>(
        `/api/albums/${encodeURIComponent(uri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get album error:', error);
      throw error;
    }
  },

  // Obtener todas las canciones
  getSongs: async (): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>('/api/songs');
      return response.data.data;
    } catch (error) {
      console.error('Get songs error:', error);
      throw error;
    }
  },

  // Obtener canciones por álbum
  getSongsByAlbum: async (albumUri: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/songs/album/${encodeURIComponent(albumUri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get songs by album error:', error);
      throw error;
    }
  },

  // Obtener canciones por artista
  getSongsByArtist: async (artistUri: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/songs/artist/${encodeURIComponent(artistUri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get songs by artist error:', error);
      throw error;
    }
  },

  // Obtener canciones por instrumento
  getSongsByInstrument: async (instrumentUri: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/songs/instrument/${encodeURIComponent(instrumentUri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get songs by instrument error:', error);
      throw error;
    }
  },

  // Obtener canción por URI
  getSongById: async (uri: string): Promise<SearchResult> => {
    try {
      const response = await api.get<ApiResponse<SearchResult>>(
        `/api/songs/${encodeURIComponent(uri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get song error:', error);
      throw error;
    }
  },

  // Obtener todos los instrumentos
  getInstruments: async (): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        '/api/instruments'
      );
      return response.data.data;
    } catch (error) {
      console.error('Get instruments error:', error);
      throw error;
    }
  },

  // Obtener instrumentos por tipo
  getInstrumentsByType: async (type: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/instruments/type/${encodeURIComponent(type)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get instruments by type error:', error);
      throw error;
    }
  },

  // Obtener todos los géneros
  getGenres: async (): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        '/api/genres'
      );
      return response.data.data;
    } catch (error) {
      console.error('Get genres error:', error);
      throw error;
    }
  },

  // Obtener géneros por artista
  getGenresByArtist: async (artistUri: string): Promise<SearchResult[]> => {
    try {
      const response = await api.get<ApiResponse<SearchResult[]>>(
        `/api/genres/artist/${encodeURIComponent(artistUri)}`
      );
      return response.data.data;
    } catch (error) {
      console.error('Get genres by artist error:', error);
      throw error;
    }
  },
};
