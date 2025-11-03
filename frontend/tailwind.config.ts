import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        midnight: '#05010f',
        neon: '#4de4ff',
        magenta: '#ff2d95',
        slate: '#0f172a',
        aurora: '#1f2937'
      },
      fontFamily: {
        cairo: ['"Cairo"', 'sans-serif']
      },
      backdropBlur: {
        xs: '2px'
      }
    }
  },
  plugins: []
};

export default config;
