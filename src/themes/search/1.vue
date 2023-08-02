<script setup>
import ReturnSearch from '../../components/ReturnSearch.vue'

const props = defineProps({
  q: [String, Number],
})

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 2)
}
function returnHome() {
  emit('return')
}
</script>
<template>
  <div id="ResultView" @contextmenu.prevent="changeTheme" @click="returnHome">
    <ReturnSearch :q="q"></ReturnSearch>
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
  margin: 10px;
}

:deep().song-id {
  position: absolute;
  display: none;
}

:deep().song-title {
  position: absolute;
  display: none;
}

:deep().song-container:hover .song-title {
  display: block;
  position: fixed;
  top: 7vh;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-size: 7vw;
  color: white;

  word-break: keep-all;
  overflow-wrap: break-word;
  width: 99%;

  font-family: 'SuperBlack', Arial, sans-serif;
  pointer-events: none; 
  -webkit-text-stroke: 1px black;
  -webkit-text-fill-color: white;
  
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