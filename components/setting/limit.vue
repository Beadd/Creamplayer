<script setup lang="ts">
const processes = [1, 2, 3, 4, 999];
const downloads = usedownloadstore();

function click(process: number) {
  downloads.process = process;
}
</script>

<template>
  <div class="flex cursor-pointer items-center justify-center gap-2">
    {{ $t("downloader.set_the_limit_on_the_number_of_download_processes") }}
    <div class="join">
      <button
        v-for="process in processes"
        :key="process"
        class="join-item btn btn-sm"
        :class="[downloads.process === process ? 'btn-accent' : 'btn-info']"
        @click="click(process)"
      >
        {{ process === 999 ? $t("No limit") : process }}
      </button>
    </div>
  </div>
</template>
