<script setup lang="ts">
const query = useRoute().query.q as string;
const q = ref(decodeURIComponent(query));
</script>

<template>
  <AppFrame>
    <div class="flex flex-col gap-4">
      <input v-model="q" class="input">
      <div class="btn w-80" @click="useRouter().push(`/search?q=${encodeURIComponent(q)}`)">
        {{ $t('Search') }}
      </div>
    </div>
  </AppFrame>
</template>
