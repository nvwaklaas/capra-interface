/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
      'logo-blue': '#154273',
      'licht-blue': '#8fcae7',
      'hemel-blue': '#007bc7',
      'donker-blue': '#01689B',
      'nvwa-rood': '#d52b1e',
      'nvwa-groen': '#39870c',
      'nvwa-grijs-1': '#f3f3f3',
      'nvwa-grijs-2': '#e6e6e6'
    }},
    
  },
  plugins: [],
}

