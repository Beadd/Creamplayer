export const usecookiestore = defineStore("cookie", () => {
  const netease = ref("");

  return { netease };
}, { persist: true });
