<script setup lang="ts">
const downloads = usedownloadstore();
</script>

<template>
  <div class="form-control flex-row">
    <label class="label cursor-pointer gap-2">
      <span class="label-text">
        {{ $t("Save the lyrics file separately") }}
      </span>
      <input
        v-model="downloads.ifsavelyric"
        type="checkbox"
        class="toggle toggle-accent"
      >
    </label>
  </div>
</template>
