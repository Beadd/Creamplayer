<script setup lang="ts">
const props = defineProps<{
  load: () => Promise<void>;
  over?: () => Promise<void>;
}>();

const pending = ref(true);

onMounted(async () => {
  try {
    await props.load();
    if (props.over) {
      await props.over();
    }
  } finally {
    pending.value = false;
  }
});
</script>

<template>
  <span v-if="pending" :class="$attrs.class" class="loading loading-spinner" />
  <span v-else>Error</span>
</template>
