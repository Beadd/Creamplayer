<script setup lang="ts">
const toast = useToast();
const { t } = useI18n();

showtoastsuccess(toast, t);
</script>

<template>
  <div class="flex h-dvh w-full items-center justify-center">
    <button class="btn" @click="useRouter().push('home')">
      Home
    </button>
  </div>
</template>
