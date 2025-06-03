<script setup lang="ts">
useHead({
  htmlAttrs: {
    class: "select-none",
  },
  meta: [
    {
      name: "viewport",
      content: "width=device-width, initial-scale=1, maximum-scale=1",
    },
  ],
});
</script>

<template>
  <NuxtLoadingIndicator :throttle="0" />
  <NuxtPage />
  <AppToast />
</template>
