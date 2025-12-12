/** @type {import('tailwindcss').Config} */
export default {
     content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
     theme: {
          extend: {
               colors: {
                    primary: "#1b4332",
                    success: "#10b981",
                    warning: "#f59e0b",
                    danger: "#ef4444",
               },
          },
     },
     plugins: [],
};
