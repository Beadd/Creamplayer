import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import "./style.css";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
import zh from "./locales/zh.json";

const getDefaultLocale = () => {
  const lang = navigator.language || "en";
  return lang.startsWith("zh") ? "zh" : "en";
};

const i18n = createI18n({
  legacy: false,
  locale: getDefaultLocale(),
  messages: {
    en,
    zh,
  },
});

import { AllCommunityModule, ModuleRegistry } from "ag-grid-community";

// Register all Community features
ModuleRegistry.registerModules([AllCommunityModule]);

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
const app = createApp(App);

app.use(i18n);
app.use(pinia);
app.mount("#app");
