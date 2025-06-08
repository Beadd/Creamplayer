<script setup lang="ts">
const cookies = usecookiestore();

async function get() {
  const res = await (window as any).electron.invoke("get-netease-login");
  if (res) {
    cookies.netease = res;
  } else {
    (window as any).electron.invoke("netease-login");
    cookies.netease = await (window as any).electron.invoke("get-netease-login");
    (window as any).electron.invoke("close-netease-login");
  }
}
</script>

<template>
  <button class="btn btn-warning" @click="get">
    {{ $t('Get the cookie of netease login window') }}
  </button>
  {{ $t('Or you can manually enter the cookie') }}
  <input
    v-model="cookies.netease" :placeholder="$t('Netease cookie')" class="input"
  >
</template>
