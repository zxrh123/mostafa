/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00D9FF',
          dark: '#00B8D4',
          light: '#40E0FF',
        },
        secondary: {
          DEFAULT: '#FF00FF',
          dark: '#CC00CC',
          light: '#FF33FF',
        },
        dark: {
          DEFAULT: '#0A0A0F',
          lighter: '#1A1A2E',
          lightest: '#2A2A3E',
        },
      },
      fontFamily: {
        'cairo': ['Cairo', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00D9FF, 0 0 10px #00D9FF' },
          '100%': { boxShadow: '0 0 10px #00D9FF, 0 0 20px #00D9FF, 0 0 30px #00D9FF' },
        },
      },
    },
  },
  plugins: [],
}
