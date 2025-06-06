<script setup lang="ts">
const q = ref("");
</script>

<template>
  <AppFrame>
    <div class="flex w-80 flex-col gap-4">
      <Search v-model="q" />
      <SettingLimit />
      <SettingQuality />
    </div>
  </AppFrame>
</template>
