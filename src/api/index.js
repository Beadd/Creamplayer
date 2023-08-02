import axios from 'axios'

import { 
  openDatabase,
  getDatabase,
  addDatabase,
  closeDatabase 
} from '../useDB';

import { getCookie } from '../useDB/setting.js';
const cookie = await getCookie()
console.log(cookie)
window.ipcRenderer.send('set-cookie', cookie);

export function checkFileName(name) {
  const invalidRegex = /[\\/:*?<>|]/g; // g 标志

  return name.replace(invalidRegex, '-');
}

export function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}


export function getSongDetailsApi(id) {
  return 'http://music.163.com/api/song/detail/?id=' + id + '&ids=%5B' + id + '%5D'
}

export function getPlaylistDetailsApi(id) {
  return 'http://music.163.com/api/v6/playlist/detail/?id=' + id
}

export function SearchDetailsApi(q, limit, offset) {
  return 'http://music.163.com/api/cloudsearch/pc?type=1&s=' + q + '&limit=' + limit + '&offset=' + offset
}

export function getSongLyricsApi(id) {
  return 'http://music.163.com/api/song/lyric?os=pc&id=' + id + '&lv=-1&tv=1'
}

export function getSongUrlApi(id) {
  return 'http://music.163.com/api/song/enhance/player/url?ids=[' + id + ']&br=2147483647'
}

const api = {
  async getSongDetails(id) {
    const database = 'SongCache'
    const store = 'SongCache'
    const db = await openDatabase(database, store);
    const value = await getDatabase(db, String(id), store);
    if (value) {
      closeDatabase(db)
      return value;
    } else {
      try {
        const response = await axios.get(getSongDetailsApi(id));
        const data = response.data;
        if (data['songs'] && data['songs'][0]['id']) {
          await addDatabase(db, String(id), data, store);
          closeDatabase(db)
          return data;
        } else {
          closeDatabase(db)
          throw new Error('Invalid response data');
        }
      } catch (error) {
        closeDatabase(db)
        console.error('API request failed:', error);
        throw error;
      }
    }
  },
  async getPlaylistDetails(id) {
    try {
      const response = await axios.get(getPlaylistDetailsApi(id));
      const data = response.data;
      if (data['playlist'] && data['playlist']['trackIds']) {
        return data;
      } else {
        throw new Error('Invalid response data');
      }
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },
  async searchDetails(q, limit, offset) {
    try {
      const response = await axios.get(SearchDetailsApi(q, limit, offset));
      const data = response.data;
      if (data['code'] == 200) {
        return data;
      } else {
        throw new Error('Invalid response data');
      }
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },
  async getSongLyrics(id) {
    const database = 'LyricsCache'
    const store = 'LyricsCache'
    const db = await openDatabase(database, store);
    const value = await getDatabase(db, String(id), store);
    if (value) {
      closeDatabase(db)
      return value;
    } else {
      try {
        const response = await axios.get(getSongLyricsApi(id));
        const data = response.data;
        console.log(data)
        if (data['code'] == 200) {
          await addDatabase(db, String(id), data, store);
          closeDatabase(db)
          return data;
        } else {
          closeDatabase(db)
          return data;
        }
      } catch (error) {
        closeDatabase(db)
        console.error('API request failed:', error);
        return data
      }
    }
  },
  async getSongUrl(id) {
    try {
      const response = await axios.get(getSongUrlApi(id));
      const data = response.data;
      if (data['data'][0]['url'] !== null) {
        return data;
      } else {
        return data
      }
    } catch (error) {
      console.error('API request failed:', error);
      return data;
    }
  },
  async downloadFile(url, filename) {
    const response = await axios({
      url,
      responseType: 'blob'
    })
  
    const blob = new Blob([response.data], {type: response.headers['content-type']})
  
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.click()
  
    URL.revokeObjectURL(link.href)
  },
  async downloadSongFile(source, 
                         downloadUrl, 
                         downloadCover, 
                         donwloadLyrics, 
                         downloadId, 
                         downloadTitle, 
                         downloadArtist, 
                         downloadAlbum, 
                         donwloadPublishTime) {
    downloadTitle = checkFileName(downloadTitle)
    downloadArtist = checkFileName(downloadArtist)
    downloadAlbum = checkFileName(downloadAlbum)
    const args = 'musicdownloader.exe' 
              + ' ' + '-s' + ' ' + source
              + ' ' + '-f' + ' ' + '"' + downloadTitle + ' - ' + downloadArtist + '"'
              + ' ' + '-u' + ' ' + '"' + downloadUrl + '"'
              + ' ' + '-c' + ' ' + '"' + downloadCover + '"'
              + ' ' + '-l' + ' ' + '"' + donwloadLyrics + '"'
              + ' ' + '-i' + ' ' + '"' + downloadId + '"'
              + ' ' + '-t' + ' ' + '"' + downloadTitle + '"'
              + ' ' + '-ar' + ' ' + '"' + downloadArtist + '"'
              + ' ' + '-al' + ' ' + '"' + downloadAlbum + '"'
              + ' ' + '-p' + ' ' + '"' + donwloadPublishTime+ '"'
    window.ipcRenderer.send('download', args);
  },
  async loadSongDetails(songid) {
    let song 
    try {
      const value = await api.getSongDetails(songid);  
      song = {
        id: value['songs'][0]['id'],
        title: value['songs'][0]['name'],
        artist: value['songs'][0]['artists'].map(item => item.name).join('/'),
        album: value['songs'][0]['album']['name'],
        cover: value['songs'][0]['album']['picUrl'],
        publishTime: formatTimestamp(value['songs'][0]['album']['publishTime'])
      }  
    } catch (error) {
      console.error('Unable to get song details', error)
    }
    return song
  },
  
};
export default api;