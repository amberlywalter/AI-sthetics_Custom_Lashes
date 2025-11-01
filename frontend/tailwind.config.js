/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#6366F1", // Soft indigo
          light: "#A5B4FC",   // Pastel indigo
          dark: "#4F46E5",    // Deep accent
        },
        neutral: {
          50: "#FAFAFA",
          100: "#F5F5F5",
          200: "#E5E5E5",
          300: "#D4D4D4",
          400: "#A3A3A3",
          500: "#737373",
          600: "#525252",
          700: "#404040",
          800: "#262626",
          900: "#171717",
        },
        blush: {
          50: "#FFF5F7",
          100: "#FFE4E8",
          200: "#FBCFE8",
          300: "#F9A8D4",
          400: "#F472B6",
          500: "#EC4899",
        },
      },
      fontFamily: {
        sans: ["'Poppins'", "Inter", "sans-serif"],
        display: ["'Playfair Display'", "serif"],
      },
    },
  },
  plugins: [],
};
