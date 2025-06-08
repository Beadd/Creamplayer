<script setup lang="ts">
defineProps<{
  song: typesong;
}>();
</script>

<template>
  <button
    class="btn btn-error size-36 bg-cover bg-center"
    :style="{ backgroundImage: `url(${song.cover})` }"
  />
</template>
