const { fontFamily } = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class', // Use 'class' strategy
  theme: {
    extend: {
      colors: {
        // As per design guidelines
        background: 'var(--color-bg)',
        foreground: 'var(--color-fg)',
        card: 'var(--color-card-bg)',
        primary: {
          DEFAULT: 'var(--color-primary)',
          foreground: '#ffffff',
        },
        accent: {
          DEFAULT: 'var(--color-accent)',
          foreground: '#ffffff',
        },
        success: 'var(--color-success)',
        danger: 'var(--color-danger)',
        muted: 'var(--color-muted)',
      },
      fontFamily: {
        // Add custom fonts
        sans: ['Inter', ...fontFamily.sans],
        serif: ['DM Serif Display', ...fontFamily.serif],
      },
      borderRadius: {
        lg: 'var(--radius-lg)', // 1rem
        md: 'var(--radius-md)', // 0.5rem
      },
      boxShadow: {
        card: '0 8px 24px rgba(12, 20, 40, 0.12)',
      },
      // Custom gradient
      backgroundImage: {
        'primary-gradient': 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};