<script setup lang="ts">
const q = defineModel<string>();

function search() {
  if (q.value) {
    useRouter().push(`/search?q=${encodeURIComponent(q.value)}`);
  }
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <input v-model="q" class="input" :placeholder="$t('Song id/url or title')">
    <button
      class="btn w-80"
      @click="search"
    >
      {{ $t("Search") }}
    </button>
  </div>
</template>
