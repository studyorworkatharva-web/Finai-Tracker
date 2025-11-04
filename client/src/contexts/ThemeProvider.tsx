import React, { createContext, useContext, useEffect, useState, useMemo } from 'react';

type Theme = 'light' | 'dark' | 'system';

interface ThemeProviderState {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: 'light' | 'dark';
}

const ThemeProviderContext = createContext<ThemeProviderState | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setThemeState] = useState<Theme>(
    () => (localStorage.getItem('theme') as Theme) || 'system'
  );

  const [systemTheme, setSystemTheme] = useState<'light' | 'dark'>(
    () => window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => setSystemTheme(mediaQuery.matches ? 'dark' : 'light');
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const resolvedTheme = theme === 'system' ? systemTheme : theme;

  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(resolvedTheme);
  }, [resolvedTheme]);

  const setTheme = (newTheme: Theme) => {
    localStorage.setItem('theme', newTheme);
    setThemeState(newTheme);
  };

  const value = useMemo(() => ({ theme, setTheme, resolvedTheme }), [theme, resolvedTheme]);

  return (
    <ThemeProviderContext.Provider value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeProviderContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};