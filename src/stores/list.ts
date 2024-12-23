import { defineStore } from "pinia";
import { ref, watch } from "vue";
import netease from "../api/netease";
import type { Song } from "../types/song";
import { electron } from "../api/download";

export const useListStore = defineStore("list", () => {
  const show = ref(false);
  const value = ref("");
  const rowData = ref<Song[]>([]);
  const hasMore = ref(true);

  const limit = 20;

  watch(value, () => {
    show.value = false;
    rowData.value = [];
    hasMore.value = true;
  });

  async function search() {
    const res: any = await netease.search(value.value, 5, 0);

    if (res.length > 0) {
      rowData.value = res;
      show.value = true;
      hasMore.value = res.length === 5;
    }

    console.log(res);
    return true;
  }

  async function loadMore() {
    if (!hasMore.value) return;

    const res: any = await netease.search(
      value.value,
      limit + 1,
      rowData.value.length,
    );

    if (res.length > 0) {
      const itemsToAdd = res.slice(0, limit);
      rowData.value = rowData.value.concat(itemsToAdd);

      hasMore.value = res.length > limit;
      return true;
    } else {
      return false;
    }
  }

  async function download(index: number) {
    rowData.value[index].state = "downloading";

    const res = await netease.download(rowData.value[index]);
    rowData.value[index] = res;

    const result = await electron.download(rowData.value[index]);

    if (result) {
      rowData.value[index].path = result;
      rowData.value[index].state = "downloaded";
      return true;
    } else {
      rowData.value[index].state = "vip";
      return false;
    }
  }

  function open(index: number) {
    const res = electron.open(rowData.value[index].path || "");
    return res;
  }

  async function downloadAll(maxConcurrent: number = 3) {
    let completedDownloads = 0;
    const totalSongs = rowData.value.length;

    for (let i = 0; i < totalSongs; i += maxConcurrent) {
      const batch = rowData.value
        .slice(i, i + maxConcurrent)
        .map((_, index) => {
          return download(i + index);
        });

      const results = await Promise.all(batch);

      completedDownloads += results.filter((result) => result).length;
    }

    console.log(`Completed ${completedDownloads} downloads.`);
    return completedDownloads;
  }

  return {
    rowData,
    search,
    show,
    value,
    loadMore,
    hasMore,
    download,
    open,
    downloadAll,
  };
});
