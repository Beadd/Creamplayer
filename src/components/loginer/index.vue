<template>
  <div class="flex gap-2" v-show="loginStore.show">
    <div @click="click" class="btn btn-error">
      {{ $t("loginer.login_to_netease_to_download_vip_and_lossless") }}
    </div>
    <div class="btn" :class="btnClass" @click="clickCheck">
      <text v-if="status === 0">{{
        $t(
          "loginer.after_login_or_logout_please_click_me_before_closing_login_window",
        )
      }}</text>
      <text v-else-if="status === 1">
        {{ $t("loginer.cookie_set_successfully") }}
      </text>
      <text v-else-if="status === 2">
        {{ $t("loginer.sorry_please_try_again_or_open_window_again") }}
      </text>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useLoginStore } from "../../stores/login";

const loginStore = useLoginStore();
const status = ref(0);
const btnClass = ref("btn-warning");

function click() {
  loginStore.login();
}

async function clickCheck() {
  if (await loginStore.get()) {
    status.value = 1;
    btnClass.value = "btn-success";
  } else {
    status.value = 2;
    btnClass.value = "btn-error";
  }
}
</script>
