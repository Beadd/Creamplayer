<template>
  <div @click="click" class="btn btn-error">
    {{ $t("loginer.login_to_netease_to_download_vip") }}
  </div>
</template>

<script setup lang="ts">
function click() {
  console.log("click");
}
</script>
