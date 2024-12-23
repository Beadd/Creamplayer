<template>
  <div :class="$style.wrapper">
    <div class="absolute top-0 right-0 p-4">
      <languager></languager>
    </div>
    <search></search>
    <downloader></downloader>
    <div class="w-full">
      <list></list>
    </div>
    <loader></loader>
  </div>
</template>

<script setup lang="ts">
import search from "./components/search/index.vue";
import list from "./components/list/index.vue";
import loader from "./components/loader/index.vue";
import downloader from "./components/downloader/index.vue";
import languager from "./components/languager/index.vue";
</script>

<style lang="postcss" module>
.wrapper {
  @apply flex flex-col justify-center items-center;
  @apply p-4 gap-4 min-h-screen;
}
</style>
