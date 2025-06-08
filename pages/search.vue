<script setup lang="ts">
const query = useRoute().query.q as string;
const q = ref(decodeURIComponent(query));

const offset = ref(0);
const limit = 10;
const more = ref(true);
const songs = usesongstore();

async function search() {
  const single = q.value.match(/music\.163\.com\/#\/song\?id=(\d+)/);
  const playlist = q.value.match(/music\.163\.com\/#\/playlist\?id=(\d+)/);

  if (single) {
    songs.search = [single[1]];
  } else if (playlist) {
    const res: any = await useFetch(api.netease.playlist(playlist[1]));
    const list = res.playlist.trackIds.map((track: any) => track.id);
    songs.search = list.slice(offset.value, offset.value + limit);
  } else {
    const res: any = await useFetch(api.netease.search(q.value, limit, offset.value));
    songs.search = res.result.songs.map((song: any) => song.id);
  }
}
</script>

<template>
  <AppFrame>
    <Search v-model="q" />
    <AppLoadder :load="search" :more="more" />
  </AppFrame>
</template>
