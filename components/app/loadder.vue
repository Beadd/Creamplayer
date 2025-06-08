<script setup lang="ts">
defineProps<{
  load: () => Promise<void>;
  more: boolean;
}>();

const trigger = ref(false);
const target = ref<HTMLElement | null>(null);
const visible = useElementVisibility(target);

watch(visible, () => {
  if (visible.value) {
    trigger.value = true;
  }
});

async function over() {
  trigger.value = false;

  setTimeout(() => {
    if (visible.value)
      trigger.value = true;
  }, 1000);
}
</script>

<template>
  <div ref="target" class="mb-32 flex h-16 w-full items-end justify-center">
    <div class="block">
      <AppLoad v-if="trigger && more" :load="load" :over="over" />
      <span v-else>{{ $t("No more") }}</span>
    </div>
  </div>
</template>
