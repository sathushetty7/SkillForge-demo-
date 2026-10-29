import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: { extend: { colors: { ink: "#090b12", panel: "#111522", accent: "#a6f36b" } } },
  plugins: []
};
export default config;