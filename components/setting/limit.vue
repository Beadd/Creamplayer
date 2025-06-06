<script setup lang="ts">
const processes = [1, 2, 3, 4, 999];
const downloads = usedownloadstore();

function click(process: number) {
  downloads.process = process;
}
</script>

<template>
  <div class="flex cursor-pointer flex-col justify-center gap-4">
    {{ $t("Set the limit on the number of download processes") }}
    <div class="join">
      <button
        v-for="process in processes"
        :key="process"
        class="join-item btn"
        :class="[downloads.process === process ? 'btn-accent' : 'btn-info']"
        @click="click(process)"
      >
        {{ process === 999 ? $t("No limit") : process }}
      </button>
    </div>
  </div>
</template>
