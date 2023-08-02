<script setup>
import ReturnSearch from '../../components/ReturnSearch.vue'

const props = defineProps({
  q: [String, Number],
})

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 15)
}
function returnHome() {
  emit('return')
}
</script>
<template>
  <div id="ResultView" @contextmenu.prevent="changeTheme" @click="returnHome">
    <ReturnSearch :q="q" :blurCover=true></ReturnSearch>
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

:deep().song-cover-blur {
  position: absolute;
  width: 227px;
  height: 227px;
  background-size: cover;
  background-position: center center;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  filter: blur(5px);
  z-index: -3;
}

:deep().song-container {
  display: flex;
  flex-wrap: nowrap;
  justify-content: flex-start; 
  position: relative;
  padding: 10px;
  overflow: hidden;
}

:deep().song-id {
  position: absolute;
  display: none;
}

:deep().song-title {
  position: absolute;
  display: none;
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