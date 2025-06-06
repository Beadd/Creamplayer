<script setup lang="ts">
const downloads = usedownloadstore();
</script>

<template>
  <label class="label flex cursor-pointer items-center justify-between gap-4">
    <span class="whitespace-break-spaces">
      {{ $t("Use anonymous downloading of non lossless songs") }}
    </span>
    <input
      v-model="downloads.ifanonymous"
      type="checkbox"
      class="toggle toggle-accent"
    >
  </label>
</template>
