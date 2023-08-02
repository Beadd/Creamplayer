import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => {
    return {
      lastSearch: '',
      volume: 0.7
    }
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'lastSearch',
        storage: localStorage
      },
      { 
        key: 'volume',
        storage: localStorage  
      }
    ]
  },
  actions: {
    setLastSearch(searchTerm) {
      this.lastSearch = searchTerm
    },

    increaseVolume() {
      this.volume = Math.min(1, this.volume + 0.1)
      this.volume = Math.round(this.volume* 10) / 10
    },
    decreaseVolume() {
      this.volume = Math.max(0, this.volume - 0.1)
      this.volume = Math.round(this.volume* 10) / 10
    }
  }
})
