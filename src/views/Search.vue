<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useCounterStore } from '../stores/counter.js'
import { initTheme, updateTheme } from '../useDB/setting.js'

// Add Theme Here
import Theme1 from '../themes/search/1.vue';
import Theme2 from '../themes/search/2.vue';
import Theme3 from '../themes/search/3.vue';
import Theme4 from '../themes/search/4.vue';
import Theme5 from '../themes/search/5.vue';
import Theme6 from '../themes/search/6.vue';
import Theme7 from '../themes/search/7.vue';
import Theme8 from '../themes/search/8.vue';
import Theme9 from '../themes/search/9.vue';
import Theme10 from '../themes/search/10.vue';
import Theme11 from '../themes/search/11.vue';
import Theme12 from '../themes/search/12.vue';
import Theme13 from '../themes/search/13.vue';
import Theme14 from '../themes/search/14.vue';
import Theme15 from '../themes/search/15.vue';


const router = useRouter()

const props = defineProps({
  q: [String, Number],
})
const counterStore = useCounterStore()
counterStore.setLastSearch(props.q)

const searchTheme = ref(15) 
const darkTheme = ref(false)

const database = 'CreamPlayer'
const store = 'Setting'
const settingKey = 'searchTheme'
const settingDark = 'darkTheme'

onMounted(async () => {
  initTheme(database, store, settingKey, searchTheme);
  await initTheme(database, store, settingDark, darkTheme);
  if (darkTheme.value && !document.body.classList.contains('dark')) {
    document.body.classList.toggle('dark');
  }
})

function switchTheme(newValue) {
  console.log('Setting')
  updateTheme(database, store, settingKey, searchTheme, newValue)
}

function returnHome() {
  router.push({ path: '/'})
  console.log('home')
}

</script>
<template>
  <div class="for-return" @click="returnHome"></div>
  <Theme1 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 1"/>
  <Theme2 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 2"/>
  <Theme3 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 3"/>
  <Theme4 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 4"/>
  <Theme5 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 5"/>
  <Theme6 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 6"/>
  <Theme7 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 7"/>
  <Theme8 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 8"/>
  <Theme9 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 9"/>
  <Theme10 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 10"/>
  <Theme11 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 11"/>
  <Theme12 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 12"/>
  <Theme13 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 13"/>
  <Theme14 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 14"/>
  <Theme15 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 15"/>
</template>
<style>
.for-return {
  position: fixed;
  height: 100%;
  width: 100%;
  cursor: pointer;
  z-index: -100;
}
</style>