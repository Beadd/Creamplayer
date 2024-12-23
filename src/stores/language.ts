import { defineStore } from "pinia";
import { ref } from "vue";

export const useLanguageStore = defineStore(
  "language",
  () => {
    const local = ref("");

    return { local };
  },
  { persist: true },
);
