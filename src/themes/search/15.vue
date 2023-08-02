<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ReturnSearch from '../../components/ReturnSearch.vue'

const blurContainer = ref(null)
const props = defineProps({
  q: [String, Number],
})

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 1)
}
function returnHome() {
  emit('return')
}

onMounted(() => {
  function setFirstBulr() {
    const firstImg = document.querySelector('.song-cover img')
    if (blurContainer.value && firstImg) {     
      blurContainer.value.style.backgroundImage = `url(${firstImg.src})`
      console.log(firstImg)
      return
    }
    setTimeout(() => {
      setFirstBulr()
    }, 777)
    console.log('setFirstBulr return')
  }
  function bodyBlur() {
    if (!blurContainer.value) return
    const covers = document.querySelectorAll('.song-cover img')
    if(covers.length > 0) {
      const covers = document.querySelectorAll('.song-cover img')
      try {
        covers.forEach(img => {
          img.removeEventListener('mouseenter', () => 
            blurContainer.value.style.backgroundImage = `url(${img.src})`) 
          img.addEventListener('mouseenter', () => 
            blurContainer.value.style.backgroundImage = `url(${img.src})`)
        })
      } catch {
        console.log('addEventListener fail')
      }
    }
  }
  setFirstBulr()
  setInterval(bodyBlur, 777)
})
</script>
<template>
  <div class="blurContainer" ref="blurContainer"></div>
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

.blurContainer {
  position: fixed;
  filter: blur(77px);
  width: 100%;
  height: 100%;
  background-image: none;
  background-attachment: fixed;
  background-position: center center;
  background-size: cover;
  background-repeat: no-repeat;
  z-index: -200;
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
  padding: 10px;
  overflow: hidden;
}

:deep().song-id {
  position: absolute;
  display: none;
}

:deep().song-title {
  position: absolute;
  bottom: 0px;
  left: 50%;
  width: max-content; 
  max-width: calc(93.3% - 20px);
  transform: translate(-50%, 0);
  cursor: default;
  overflow-wrap: break-word;
  word-break: keep-all;
  pointer-events: none; 
  overflow: hidden;

  text-align: center;
  white-space: nowrap;

  position: absolute;
  border: 1px solid black;
  background-color: white;
  font-size: 12px;
  font-family: 'Microsoft YaHei';
  padding-left: 7px;
  padding-right: 7px;
  padding-top: 3px;
  padding-bottom: 3px;

  color: #000000c4;
}
:deep().song-title-artist {
  display: contents!important;
}
:deep().song-title-album {
  display: contents!important;
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