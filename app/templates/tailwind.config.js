/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      boxShadow: {
        'glow': '0 0 7px 3px rgba(255, 0, 0, 0.7)',
      },
    },
  },
  variants: {},
  plugins: [],
}