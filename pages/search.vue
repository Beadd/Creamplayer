<script setup lang="ts">
const query = useRoute().query.q as string;
const q = ref(decodeURIComponent(query));
</script>

<template>
  <AppFrame>
    <Search v-model="q" />
  </AppFrame>
</template>
