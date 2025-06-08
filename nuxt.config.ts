import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: false },
  css: ["~/assets/css/main.css", "boxicons/css/boxicons.min.css"],
  vite: {
    plugins: [tailwindcss()],
    server: {
      proxy: {
        "/api": {
          target: "http://music.163.com/",
          changeOrigin: true,
        },
      },
    },
  },
  modules: [
    "@pinia/nuxt",
    "pinia-plugin-persistedstate",
    "@nuxtjs/i18n",
    "@vueuse/nuxt",
    "@nuxt/eslint",
    "@primevue/nuxt-module",
  ],
  eslint: {
    checker: true,
  },
  i18n: {
    defaultLocale: "zh",
    strategy: "no_prefix",
    locales: [
      { code: "zh", name: "简体中文", file: "zh.json" },
      { code: "en", name: "English", file: "en.json" },
    ],
    bundle: {
      optimizeTranslationDirective: false,
    },
  },
  typescript: {
    typeCheck: true,
  },
});
