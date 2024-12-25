<template>
  <div class="flex gap-4 flex-col" v-show="downloadStore.show">
    <!-- Download All Button -->
    <div class="flex justify-center items-center gap-2">
      <div @click="click" class="btn btn-accent">
        {{ $t("downloader.all") }} ({{ listStore.rowData.length }})
      </div>
      <slot></slot>
    </div>
    <process></process>
    <quality></quality>
    <div class="flex justify-center items-center gap-2">
      <div class="form-control flex-row">
        <label class="label cursor-pointer gap-4">
          <span class="label-text">
            {{ $t("downloader.save_the_lyrics_file_separately") }}
          </span>
          <input
            type="checkbox"
            class="toggle toggle-accent"
            v-model="downloadStore.saveLyric"
          />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useListStore } from "../../stores/list";
import { useDownloadStore } from "../../stores/download";
import process from "./process.vue";
import quality from "./quality.vue";

const downloadStore = useDownloadStore();
const listStore = useListStore();

async function click() {
  await listStore.downloadAll(downloadStore.process);
}
</script>
