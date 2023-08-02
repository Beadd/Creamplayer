<script setup>
import ReturnSearch from '../../components/ReturnSearch.vue'

const props = defineProps({
  q: [String, Number],
})

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 12)
}
function returnHome() {
  emit('return')
}
</script>
<template>
  <div id="ResultView" @contextmenu.prevent="changeTheme" @click="returnHome">
    <ReturnSearch :q="q" :autoFont="true"></ReturnSearch>
  </div>
</template>
<style scoped>
#ResultView {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

:deep().song-cover {
  width: 207px;
  height: 207px;
  cursor: pointer;

}

:deep().song-cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

:deep().song-container {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-start; 
  position: relative;
  margin: 10px;
  overflow: hidden;
}

:deep().song-id {
  position: absolute;
  display: none;
}

:deep().song-title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  padding: 10px;
  cursor: default;
  word-break: keep-all;
  width: 99%;
  overflow-wrap: break-word;
  font-weight: bold;
  font-family: 'SuperBlack', Arial, sans-serif;
  -webkit-text-stroke: 1px black;
  -webkit-text-fill-color: white;

  pointer-events: none; 
}

:deep().song-artist {
  position: absolute;
  display: none;
}

:deep().song-album {
  position: absolute;
  display: none;
}

:deep().song-publish-time {
  position: absolute;
  display: none;
}
</style>