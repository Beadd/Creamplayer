<template>
  <div
    v-show="listStore.show && listStore.hasMore"
    @click="click"
    class="btn btn-accent"
  >
    {{ $t("loader.more") }}
  </div>
</template>

<script setup lang="ts">
import { useListStore } from "../../stores/list";

const listStore = useListStore();

async function click() {
  await listStore.loadMore();
}
</script>
