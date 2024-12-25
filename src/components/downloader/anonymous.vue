<template>
  <div class="form-control flex-row">
    <label class="label cursor-pointer gap-2">
      <span class="label-text">
        {{ $t("downloader.use_anonymous_downloading_of_non_lossless_songs") }}
      </span>
      <input
        type="checkbox"
        class="toggle toggle-accent"
        v-model="downloadStore.anonymous"
      />
    </label>
  </div>
</template>

<script setup lang="ts">
import { useDownloadStore } from "../../stores/download";

const downloadStore = useDownloadStore();
</script>
