export const usedownloadstore = defineStore("download", () => {
  const ifshow = ref(false);
  const ifsavelyric = ref(false);
  const quality = ref(320000);
  const process = ref(2);
  const ifanonymous = ref(true);

  return { ifshow, ifsavelyric, process, quality, ifanonymous };
}, { persist: true });
