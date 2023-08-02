<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'

const props = defineProps({
  songUrl: [String, Number],
  songLyrics: Array,
  title: [String, Number],
  artist: [String, Number],
  album: [String, Number],
  cover: [String, Number],
  publishTime: [String, Number],
  audio: HTMLAudioElement,
  currentHighlight: [String, Number],
})

const pureLyrics = ref([]) 
const lyricsContainer = ref(null)

const emit = defineEmits(['switch', 'return']) 
function changeTheme() {
  emit('switch', 2)
}
function returnSearch() {
  emit('return')
}

function getFontSize(item) {
  if(!item.text) return '3vw'
  if(/^\s+$/.test(item.text)) {
    return '14px'; 
  }
  const maxWidth = window.innerWidth + 'px'
  let size = 1
  while(true) {
    if (size >= 40) return String(size) + 'vw' 
    const fontSize = String(size) + 'vw'
    const result = willTextWrap(item.text, fontSize, maxWidth)
    if (result) {
      return String(size - 1.1) + 'vw'
    } else {
      size++
    }
  }
}

function willTextWrap(text, fontSize, maxWidth) {
  const testEl = document.createElement('div');
  testEl.style.fontSize = fontSize;
  testEl.style.maxWidth = maxWidth;
  testEl.innerText = text;
  testEl.style.fontFamily = "'SuperBlack', Arial, sans-serif";
  testEl.style.overflowWrap = 'anywhere';
  testEl.style.whiteSpace = 'pre';
  document.body.appendChild(testEl);
  const isWrapped = testEl.scrollWidth > testEl.clientWidth;
  document.body.removeChild(testEl);
  return isWrapped;
}

function jumpTo(item) {
  if (item.time != 777404) {
    props.audio.currentTime = item.time
  }
}

// function smoothScrollTo(element, to, duration) {
//   const start = element.scrollTop;
//   const change = to - start;
//   const increment = 20;
//   let currentTime = 0;
  
//   const animateScroll = () => {
//     currentTime += increment;
//     const val = Math.easeInOutQuad(currentTime, start, change, duration);
//     element.scrollTop = val;
//     if(currentTime < duration) {
//       setTimeout(animateScroll, increment);
//     }
//   };
//   animateScroll();
// }
onMounted(async () => {
  watch(() => props.currentHighlight, (newVal, oldVal) => {
    nextTick(() => {  
      try {
        const active = document.getElementsByClassName('active')[0]
        const top = active.offsetTop
        console.log(top)
        const viewportHeight = document.documentElement.clientHeight
        const offset = active.offsetTop - (viewportHeight / 2) + (active.clientHeight / 2)
        document.documentElement.scrollTop = offset 
      } catch (e) {
        console.log('Failed to get active element, skip scrolling'); 
      }
    })
  })
  await new Promise(resolve => {
    watch(() => props.songLyrics, resolve) 
  })

  function wipeLyrics(Lyrics) {
    let firstLine = true
    return Lyrics.value.map(line => {
      if (firstLine) {
        if (line == ""
            || line.text.includes(':') 
            || line.text.includes('：') 
            || line.text.includes('-')
            || line.text.includes('(')
            || line.text.includes('（')
            || line.text.includes('《')) {
          return false
        } else {
          firstLine = false
        }
      }
      return line
    })
  }
  pureLyrics.value = props.songLyrics
  pureLyrics.value = wipeLyrics(pureLyrics)
  pureLyrics.value = pureLyrics.value.reverse() 
  pureLyrics.value = wipeLyrics(pureLyrics)
  pureLyrics.value.push({ time: 0, text: ' ' })
  pureLyrics.value = pureLyrics.value.reverse() 
  console.log(pureLyrics.value)
})

</script>
<template>
  <div class="player">
    <div class="lyrics-container" ref="lyricsContainer">
      <div 
        v-for="item in pureLyrics" 
        class="lyrics" 
        :key="item.time" 
        @click="jumpTo(item)" 
        :style="{fontSize: getFontSize(item)}"
        :class="{ active: item.time === currentHighlight }">
          {{ item.text }}
      </div>
    </div>
  </div>
</template>
<style scoped>
::selection {
  background-color: transparent;
}
.player {
  width: 100%;
  height: 100%;
  position: absolute;
  font-family: 'SuperBlack', Arial, sans-serif;
}
.lyrics-container {
  width: 100%;
  text-align: center;
  position: absolute;
  cursor: default;
  overflow-y: auto;
}
.active {
  color: red;
  
}
body.dark .lyrics-container {
  color: #c4c4c4;
}

</style>