import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        display: ['"Libre Franklin Variable"', '"Inter Variable"', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4 Variable"', 'Georgia', 'serif'],
        sans: ['"Inter Variable"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono Variable"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      colors: {
        brand: { 50:'#fdf3ec', 100:'#fae5d3', 500:'#e0510a', 600:'#c2410c', 700:'#93300a' },
        ink: '#16130e',
        paper: '#f7f2e9',
        hairline: '#e3d9c6',
      },
      boxShadow: {
        card: '0 1px 2px rgba(22,19,14,.07), 0 8px 24px -12px rgba(22,19,14,.20)',
      },
      keyframes: {
        ticker: { '0%': { transform: 'translateX(0)' }, '100%': { transform: 'translateX(-50%)' } },
      },
      animation: {
        ticker: 'ticker 38s linear infinite',
      },
    },
  },
  plugins: [typography],
}
