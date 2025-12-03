import React from 'react';
import { Globe } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { SupportedLanguage } from '../types';
import styles from '../styles/LanguageSelector.module.css';

const LANGUAGES: { code: SupportedLanguage; name: string }[] = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
    { code: 'de', name: 'Deutsch' },
];

export const LanguageSelector: React.FC = () => {
    const { i18n } = useTranslation();

    const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const newLang = e.target.value as SupportedLanguage;
        i18n.changeLanguage(newLang);
    };

    return (
        <div className={styles.languageSelector}>
            <Globe size={18} className={styles.icon} />
            <select
                value={i18n.language}
                onChange={handleLanguageChange}
                className={styles.select}
                aria-label="Select language"
            >
                {LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                        {lang.name}
                    </option>
                ))}
            </select>
        </div>
    );
};
