export const api = {
  netease: {
    search: (q: string, limit: number, offset: number) => `api/cloudsearch/pc?type=1&s=${q}&limit=${limit}&offset=${offset}`,
    playlist: (id: string) => `api/v6/playlist/detail/?id=${id}`,
    detail: (id: string) => `api/song/detail/?id=${id}&ids=%5B${id}%5D`,
    url: (id: string, quality: number) => `api/song/enhance/player/url?ids=[${id}]&br=${quality}`,
    lyric: (id: string) => `http://music.163.com/api/song/lyric?os=pc&id=${id}&lv=-1&tv=1`,
  },
};
