import { defineStore } from "pinia";
import { ref } from "vue";
import netease from "../api/netease";
import type { Song } from "../types/song";
import { useLoginStore } from "./login";
import { electron } from "../api/download";

export const useDownloadStore = defineStore("download", () => {
  const show = ref(false);
  const saveLyric = ref(false);
  const quality = ref(2147483647);
  const process = ref(2);

  async function download(song: Song) {
    const loginStore = useLoginStore();
    song = await netease.download(
      song,
      loginStore.neteaseCookie,
      quality.value,
    );

    const result = await electron.download(song, saveLyric.value);

    return result;
  }

  return { show, saveLyric, download, process };
});
