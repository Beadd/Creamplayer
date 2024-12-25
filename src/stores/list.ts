import { defineStore } from "pinia";
import { ref } from "vue";
import type { Song } from "../types/song";
import { useDownloadStore } from "./download";
import { electron } from "../api/download";

export const useListStore = defineStore("list", () => {
  const show = ref(false);
  const rowData = ref<Song[]>([]);

  async function download(index: number) {
    const downloadStore = useDownloadStore();
    rowData.value[index].state = "downloading";

    const res = await downloadStore.download(rowData.value[index]);

    if (res) {
      rowData.value[index].path = res;
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
    show,
    download,
    open,
    downloadAll,
    rowData,
  };
});
