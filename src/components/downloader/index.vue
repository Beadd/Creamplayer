<template>
  <div class="flex gap-4 flex-col" v-show="listStore.show">
    <!-- Download All Button -->
    <div class="flex justify-center items-center gap-2">
      <div @click="click" class="btn btn-accent">
        {{ $t("downloader.all") }} ({{ listStore.rowData.length }})
      </div>
      <slot></slot>
    </div>
    <div class="flex justify-center items-center gap-2 cursor-pointer">
      {{ $t("downloader.set_maximum_number_of_processes") }}
      <!-- Process Selection -->
      <div class="join">
        <button
          v-for="process in processes"
          :key="process"
          @click="setActiveProcess(process)"
          :class="[
            'join-item',
            'btn',
            'btn-sm',
            activeProcess === process ? 'btn-accent' : 'btn-info',
          ]"
        >
          {{ process === 0 ? $t("downloader.no_limit") : process }}
        </button>
      </div>
    </div>
    <div class="flex justify-center items-center gap-2">
      <div class="form-control flex-row">
        <label class="label cursor-pointer gap-4">
          <span class="label-text">
            {{ $t("downloader.save_the_lyrics_file_separately") }}
          </span>
          <input
            type="checkbox"
            class="toggle toggle-accent"
            v-model="listStore.saveLyric"
          />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useListStore } from "../../stores/list";

const listStore = useListStore();
const activeProcess = ref(2);
const processes = [1, 2, 3, 4, 0];

async function click() {
  // Pass undefined if "No Limit" is selected (0 represents no limit)
  const maxConcurrent = activeProcess.value === 0 ? 999 : activeProcess.value;
  await listStore.downloadAll(maxConcurrent);
}

// Set the selected process count
function setActiveProcess(process: number) {
  activeProcess.value = process;
}
</script>
