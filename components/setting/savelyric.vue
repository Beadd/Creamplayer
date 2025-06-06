<script setup lang="ts">
const downloads = usedownloadstore();
</script>

<template>
  <label class="label flex cursor-pointer items-center justify-between gap-4">
    <span class="whitespace-break-spaces">
      {{ $t("Save the lyrics file separately") }}
    </span>
    <input
      v-model="downloads.ifsavelyric"
      type="checkbox"
      class="toggle toggle-accent"
    >
  </label>
</template>
