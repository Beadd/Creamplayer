<template>
  <div v-show="loadStore.show" @click="click" class="btn btn-accent">
    {{ $t("loader.more") }}
  </div>
</template>

<script setup lang="ts">
import { useLoadStore } from "../../stores/load";

const loadStore = useLoadStore();

async function click() {
  await loadStore.loadMore();
}
</script>
