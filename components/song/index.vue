<script setup lang="ts">
defineProps<{
  song: typesong;
}>();
</script>

<template>
  <button
    class="btn btn-error h-32 w-32 bg-cover bg-center"
    :style="{ backgroundImage: `url(${song.cover})` }"
  />
</template>
