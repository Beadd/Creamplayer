<script setup lang="ts">
const q = defineModel<string>();
</script>

<template>
  <div class="flex flex-col gap-4">
    <input v-model="q" class="input">
    <div
      class="btn w-80"
      @click="useRouter().push(`/search?q=${encodeURIComponent(q || '')}`)"
    >
      {{ $t("Search") }}
    </div>
  </div>
</template>
