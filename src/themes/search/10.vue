<script setup>
import ReturnSearch from '../../components/ReturnSearch.vue'

const props = defineProps({
  q: [String, Number],
})

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 11)
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
  border-radius: .75rem;
  cursor: pointer;

}

:deep().song-cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: .75rem;
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