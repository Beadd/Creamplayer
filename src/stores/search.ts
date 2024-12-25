import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { useListStore } from "./list";
import netease from "../api/netease";
import { useLoadStore } from "./load";
import { useDownloadStore } from "./download";
import { useLoginStore } from "./login";

export const useSearchStore = defineStore("search", () => {
  const value = ref("");
  const listStore = useListStore();
  const downloadStore = useDownloadStore();
  const loadStore = useLoadStore();
  const loginStore = useLoginStore();

  const limit = 5;

  watch(value, () => {
    listStore.show = false;
    downloadStore.show = false;
    loadStore.show = false;
    loginStore.show = false;
    listStore.rowData = [];
  });

  async function search() {
    const loadStore = useLoadStore();
    const res: any = await netease.search(value.value, limit, 0);

    if (res.length > 0) {
      listStore.rowData = res;
      listStore.show = true;
      loginStore.show = true;
      downloadStore.show = true;
      loadStore.show = res.length === 5;
    }

    return true;
  }

  return {
    value,
    search,
  };
});
