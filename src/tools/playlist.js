import api from '../api'
import { getSongLyricsApi } from '../api'

async function loadIds(playlistId) {
  let ids 
  await api.getPlaylistDetails(playlistId)
    .then(value => {
      ids = value['playlist']['trackIds']
    })
    .catch(error => {
      console.error('Failed to get playlist details:', error)
    })
  return ids
}

async function loadSong(songid) {
  try {
    return api.loadSongDetails(songid)
  } catch (error) {
    console.error('API request failed:', error);
    setTimeout(() => {
      api.loadSongDetails(songid)
    }, 777);
  }
}

async function downloadSong(song) {
  console.log('Downloading')
  let songUrl
  try {
    await api.getSongUrl(song.id).then(res => {
      songUrl = res['data'][0]['url']
    })
  } catch (error) {
    console.error('Get Song URL fail:', error);
    songUrl = 0
  }
  console.log(songUrl)
  api.downloadSongFile('netease',
                       songUrl, 
                       song.cover, 
                       getSongLyricsApi(song.id),
                       song.id, 
                       song.title, 
                       song.artist, 
                       song.album, 
                       song.publishTime)
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
export async function downloadPlaylist(playlistId) {
  let ids = await loadIds(playlistId)
  console.log(ids)
  for (const id of ids) {
    const song = await loadSong(id.id)
    console.log(song)
    await downloadSong(song)
    // await sleep(777); 
  }
}

export async function downloadSingleSong(songId) {
  const song = await loadSong(songId)
  console.log(song)
  await downloadSong(song)
}