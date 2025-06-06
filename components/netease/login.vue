<script setup lang="ts">
function open() {
  (window as any).electron.invoke("netease-login");
}
</script>

<template>
  <button class="btn btn-error" @click="open">
    {{ $t('Open the login window of netease') }}
  </button>
</template>
