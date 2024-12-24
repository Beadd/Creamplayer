// vite.config.js
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  base: "./",
  plugins: [vue()],
  server: {
    proxy: {
      "/api": {
        target: "http://music.163.com/",
        changeOrigin: true,
      },
    },
  },
});
