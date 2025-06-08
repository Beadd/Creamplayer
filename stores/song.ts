export const usesongstore = defineStore("song", () => {
  const search = ref<typesong[]>();

  return { search };
});
