import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import en from './locales/en.json';
import es from './locales/es.json';
import fr from './locales/fr.json';
import de from './locales/de.json';

// Configuración de i18next
i18n
    .use(LanguageDetector) // Detecta el idioma del navegador
    .use(initReactI18next) // Conecta i18next con React
    .init({
        resources: {
            en: { translation: en },
            es: { translation: es },
            fr: { translation: fr },
            de: { translation: de },
        },
        fallbackLng: 'es', // Idioma por defecto
        supportedLngs: ['en', 'es', 'fr', 'de'],
        interpolation: {
            escapeValue: false, // React ya escapa por defecto
        },
        detection: {
            order: ['localStorage', 'navigator'],
            caches: ['localStorage'],
        },
    });

export default i18n;
