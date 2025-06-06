<script setup lang="ts">
const cookies = usecookiestore();

async function get() {
  const res = await (window as any).electron.invoke("get-netease-login");
  if (res) {
    cookies.netease = res;
    return true;
  } else {
    return false;
  }
}
</script>

<template>
  <button class="btn btn-warning" @click="get">
    {{ $t('Get the cookie of netease login window') }}
  </button>
  <input v-model="cookies.netease" :placeholder="$t('Cookie')" class="input">
</template>
