<script setup>
import { ref } from 'vue'

const search = ref('')
const inputRef = ref(null)

const emit = defineEmits(['switch', 'search']) 
function changeTheme() {
  emit('switch', 1)
}
function searchEnter() {
  emit('search', search.value)
}

function onClick() {
  inputRef.value.focus()
}
</script>
<template>
  <div class="home" @contextmenu.prevent="changeTheme" @click="onClick">
      <div class="home-search">
        <input class="home-input" placeholder="歌曲名或歌单歌曲链接" v-model="search" @keyup.enter="searchEnter" autofocus ref="inputRef"> 
      </div>
    </div>
</template>
<style scoped>
.home {
  position: absolute;
  height: 100%;
  width: 100%;
}
.home-input {
  border: 1px solid;
  position: absolute;
  top: 50%;
  left: 50%;
  width: 99%;
  transform: translate(-50%, -50%);
  font-size: 7.7vw; 
  text-align: center;
  border-color: transparent;
}
.home-input:focus {
  outline: none;
  border: none;
}

body.dark .home-input {
  color: #c4c4c4;
  background-color: black;
}
</style>