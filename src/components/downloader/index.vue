<template>
  <div class="flex gap-2" v-show="listStore.show">
    <!-- Download All Button -->
    <div @click="click" class="btn btn-accent">
      {{ $t("downloader.all") }} ({{ listStore.rowData.length }})
    </div>

    <!-- Process Selection -->
    <div class="join">
      <button class="join-item btn btn-info btn-md btn-disabled">
        {{ $t("downloader.set_maximum_number_of_processes") }}
      </button>
      <button
        v-for="process in processes"
        :key="process"
        @click="setActiveProcess(process)"
        :class="[
          'join-item',
          'btn',
          'btn-md',
          activeProcess === process ? 'btn-accent' : 'btn-info',
        ]"
      >
        {{ process === 0 ? $t("downloader.no_limit") : process }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useListStore } from "../../stores/list";

// Store reference
const listStore = useListStore();

// Active process selection
const activeProcess = ref(2); // Default to 2 processes
// Add "No Limit" option (represented as 0)
const processes = [1, 2, 3, 4, 0]; // 0 represents "No Limit"

// Handle the click event for the "Download All" button
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
