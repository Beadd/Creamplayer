<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

import { initTheme, updateTheme } from '../useDB/setting.js'

import { downloadPlaylist, downloadSingleSong } from '../tools/playlist.js'

// Add Theme Here
import Theme1 from '../themes/home/1.vue';
import Theme2 from '../themes/home/2.vue';

const router = useRouter()

const homeTheme = ref(1) 
const darkTheme = ref(true)

const database = 'CreamPlayer'
const store = 'Setting'
const settingKey = 'homeTheme'
const settingDark = 'darkTheme'

onMounted(async () => {
  initTheme(database, store, settingKey, homeTheme);
  await initTheme(database, store, settingDark, darkTheme);
  if (darkTheme.value && !document.body.classList.contains('dark')) {
    document.body.classList.toggle('dark');
  }
})

function switchTheme(newValue) {
  updateTheme(database, store, settingKey, homeTheme, newValue)
}

function switchDarkMode(event) {
  if (event.button !== 1) return
  event.preventDefault();
  document.body.classList.toggle('dark');
  updateTheme(database, store, settingDark, darkTheme, !darkTheme.value)
}
onMounted(() => {
  window.addEventListener('mousedown', switchDarkMode)
})
onUnmounted(() => {
  window.removeEventListener('mousedown', switchDarkMode)
})


function searchEnter(value) {
  if (value.includes('playlist')) {
    if (value.includes('id=')) {
      let id = value.match(/id=(.*?)$/)[1];
      console.log(id)
      downloadPlaylist(id)
    }
  } else if (value.includes('song')) {
    if (value.includes('id=')) {
      let id = value.match(/id=(.*?)$/)[1];
      console.log(id)
      downloadSingleSong(id)
    }
  } else {
    router.push({
      name: 'search',
      params: {
        q: value
      }  
    })
  }
}
</script>
<template>
  <Theme1 @search="searchEnter" @switch="switchTheme" v-if="homeTheme == 1"></Theme1>
  <Theme2 @search="searchEnter" @switch="switchTheme" v-if="homeTheme == 2"></Theme2>
</template>