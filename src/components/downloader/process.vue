<template>
  <div class="flex justify-center items-center gap-2 cursor-pointer">
    {{ $t("downloader.set_the_limit_on_the_number_of_download_processes") }}
    <!-- Process Selection -->
    <div class="join">
      <button
        v-for="process in processes"
        :key="process"
        @click="click(process)"
        :class="[
          'join-item',
          'btn',
          'btn-sm',
          downloadStore.process === process ? 'btn-accent' : 'btn-info',
        ]"
      >
        {{ process === 999 ? $t("downloader.no_limit") : process }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDownloadStore } from "../../stores/download";

const processes = [1, 2, 3, 4, 999];
const downloadStore = useDownloadStore();

function click(process: number) {
  downloadStore.process = process;
}
</script>
