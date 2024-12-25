import { defineStore } from "pinia";
import { ref } from "vue";
import { useListStore } from "./list";
import { useSearchStore } from "./search";
import netease from "../api/netease";

export const useLoadStore = defineStore("load", () => {
  const show = ref(false);

  const limit = 20;

  async function loadMore() {
    const listStore = useListStore();
    const searchStore = useSearchStore();

    const res: any = await netease.search(
      searchStore.value,
      limit + 1,
      listStore.rowData.length,
    );

    if (res.length > 0) {
      const itemsToAdd = res.slice(0, limit);
      listStore.rowData = listStore.rowData.concat(itemsToAdd);

      show.value = res.length > limit;
      return true;
    } else {
      return false;
    }
  }

  return {
    show,
    loadMore,
  };
});
