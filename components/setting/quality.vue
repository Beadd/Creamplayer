<script setup lang="ts">
const qualities = [128000, 192000, 256000, 320000, 0];
const downloads = usedownloadstore();

function getbtnclass(quality: number) {
  const baseclasses = ["join-item", "btn", "btn-sm"];
  if (downloads.quality === quality) {
    baseclasses.push("btn-accent");
  } else if (quality === 0) {
    baseclasses.push("btn-error");
  } else {
    baseclasses.push("btn-success");
  }

  return baseclasses.join(" ");
}

function click(quality: number) {
  downloads.quality = quality;
}
</script>

<template>
  <div class="flex cursor-pointer flex-col gap-4">
    {{ $t("Set song bitrate") }}
    <div class="join">
      <button
        v-for="quality in qualities"
        :key="quality"
        :class="getbtnclass(quality)"
        @click="click(quality)"
      >
        {{ quality === 128000 ? "128k" : "" }}
        {{ quality === 192000 ? "192k" : "" }}
        {{ quality === 256000 ? "256k?" : "" }}
        {{ quality === 320000 ? "320k" : "" }}
        {{ quality === 0 ? $t("Lossless") : "" }}
      </button>
    </div>
  </div>
</template>
