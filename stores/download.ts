export const usedownloadstore = defineStore("download", () => {
  const process = ref(2);
  const quality = ref(320000);
  const ifsavelyric = ref(false);
  const ifanonymous = ref(true);

  return { process, quality, ifsavelyric, ifanonymous };
}, { persist: true });
