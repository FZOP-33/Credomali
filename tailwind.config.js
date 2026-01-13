/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './Credoapp/templates/**/*.html',
    './templates/**/*.html',
    './Credoapp/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        'credo-blue': '#0A3D62', // Bleu foncé du cercle/texte
        'credo-orange': '#F58634', // Orange des barres
        'credo-green': '#2ECC71', // Vert de la flèche
        'credo-lightblue': '#3498DB', // Bleu clair des barres
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    // require('@tailwindcss/forms'), // Si besoin
  ],
}
