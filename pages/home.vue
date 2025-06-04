<script setup lang="ts">
const q = ref("");
</script>

<template>
  <AppFrame>
    <Search v-model="q" />
  </AppFrame>
</template>
