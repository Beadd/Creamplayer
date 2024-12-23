<template>
  <ag-grid-vue
    v-show="listStore.show"
    data-ag-theme-mode="dark-blue"
    :rowData="listStore.rowData"
    :columnDefs="colDefs"
    domLayout="autoHeight"
    class="min-h-[10px]"
  >
  </ag-grid-vue>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { useListStore } from "../../stores/list";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const listStore = useListStore();

const downloaded = (button: any, rowIndex: number) => {
  button.classList.remove("btn-disabled");
  button.classList.add("btn-success");
  button.innerHTML = t("list.open_folder");
  button.onclick = () => {
    console.log(rowIndex);
    listStore.open(rowIndex);
  };
};

const downloading = (button: any) => {
  button.classList.add("btn-disabled");
  button.innerHTML = t("list.downloading");
};

const vip = (button: any) => {
  button.classList.remove("btn-disabled");
  button.classList.add("btn-error");
  button.innerHTML = t("list.vip_retry");
};

const download = (params: any) => {
  const rowIndex = params.node.rowIndex;

  const button = document.createElement("button");
  button.classList.add("btn", "btn-secondary", "btn-sm");

  button.onclick = async () => {
    await listStore.download(rowIndex);
  };

  if (params.data.state === "downloading") {
    downloading(button);
  } else if (params.data.state === "downloaded") {
    downloaded(button, rowIndex);
  } else if (params.data.state === "vip") {
    vip(button);
  } else {
    button.textContent = t("list.download");
  }

  return button;
};

const colDefs = computed(() => [
  { headerName: t("list.state"), width: 150, cellRenderer: download },
  { headerName: t("list.song_name"), field: "name", width: 200 },
  { headerName: t("list.cover"), field: "cover", width: 150 },
  { headerName: t("list.artist"), field: "artist", width: 150 },
  { headerName: t("list.album"), field: "album", width: 150 },
  { headerName: t("list.id"), field: "id", width: 150 },
  { headerName: t("list.publish_time"), field: "publishTime", width: 200 },
]);
</script>

<style>
.ag-center-cols-viewport {
  min-height: unset !important;
}
</style>
