<script setup lang="ts">
const query = useRoute().query.q as string;
const q = ref(decodeURIComponent(query));

const offset = ref(0);
const limit = 20;
const more = ref(true);
const songs = usesongstore();

async function search() {
  const single = q.value.match(/music\.163\.com\/#\/song\?id=(\d+)/);
  const playlist = q.value.match(/music\.163\.com\/#\/playlist\?id=(\d+)/);

  if (single) {
    const res: any = await useFetch(api.netease.detail(single[1]));
    songs.search = res;
    more.value = false;
  } else if (playlist) {
    const res: any = await useFetch(api.netease.playlist(playlist[1]));
    const list = res.playlist.trackIds.map((track: any) => track.id);
    songs.search = list.slice(offset.value, offset.value + limit);
  } else {
    const { data } = await useFetch<any>(api.netease.search(q.value, limit, offset.value));
    const parsed = JSON.parse(data.value as string).result.songs;
    if (parsed.length < limit)
      more.value = false;

    songs.search = await parsed.map((song: any) => ({
      id: song.id,
      name: song.name,
      cover: song.al.picUrl,
    }));
    more.value = false;
  }
}
</script>

<template>
  <AppFrame>
    <Search v-model="q" />
    <div class="flex flex-wrap justify-center gap-4 p-4">
      <Song v-for="(song, index) in songs.search" :key="index" :song="song" />
    </div>
    <AppLoadder :load="search" :more="more" />
  </AppFrame>
</template>
