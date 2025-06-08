<script setup lang="ts">
function open() {
  (window as any).electron.invoke("netease-login");
}
</script>

<template>
  {{ $t('App only') }}
  <button class="btn btn-error" @click="open">
    {{ $t('Open the login window of netease') }}
  </button>
</template>
