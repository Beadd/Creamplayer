<template>
  <div class="flex justify-center items-center gap-2 cursor-pointer">
    {{ $t("downloader.set_song_bitrate") }}
    <!-- Process Selection -->
    <div class="join">
      <button
        v-for="quality in qualities"
        :key="quality"
        @click="click(quality)"
        :class="getBtnClass(quality)"
      >
        {{ quality === 128000 ? "128k" : "" }}
        {{ quality === 192000 ? "192k" : "" }}
        {{ quality === 256000 ? "256k?" : "" }}
        {{ quality === 320000 ? "320k" : "" }}
        {{ quality === 0 ? $t("downloader.lossless") : "" }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDownloadStore } from "../../stores/download";

const qualities = [128000, 192000, 256000, 320000, 0]; // lossless
const downloadStore = useDownloadStore();

function getBtnClass(quality: number) {
  const baseClasses = ["join-item", "btn", "btn-sm"];
  if (downloadStore.quality === quality) {
    baseClasses.push("btn-accent");
  } else if (quality === 0) {
    baseClasses.push("btn-error");
  } else {
    baseClasses.push("btn-success");
  }

  return baseClasses.join(" ");
}

function click(quality: number) {
  downloadStore.quality = quality;
}
</script>
