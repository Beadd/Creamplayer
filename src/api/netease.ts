import axios from "axios";
import { format } from "date-fns";
import type { Song } from "../types/song";

const apiClient = axios.create({
  baseURL:
    import.meta.env.MODE === "development"
      ? "/api"
      : "http://music.163.com/api",
  headers: {
    "Content-Type": "application/json",
  },
});

async function detail(id: string) {
  try {
    const res = await apiClient.get(
      "/song/detail/?id=" + id + "&ids=%5B" + id + "%5D",
    );
    return res.data;
  } catch (err: any) {
    console.error("API Error Response:", err.response.data);
    throw err;
  }
}

async function search(q: string, limit: number, offset: number) {
  try {
    const res = await apiClient.get(
      "/cloudsearch/pc?type=1&s=" + q + "&limit=" + limit + "&offset=" + offset,
    );
    return res.data;
  } catch (err: any) {
    console.error("API Error Response:", err.response.data);
    throw err;
  }
}

async function url(
  id: string,
  cookie: string = "",
  quality: number = 2147483647,
  anonymous: boolean = true,
) {
  if (quality === 0) {
    quality = 2147483647;
  }

  let res: any;
  async function normal() {
    res = await apiClient.get(
      "/song/enhance/player/url?ids=[" + id + "]&br=" + quality,
    );
  }
  async function vip() {
    res = await apiClient.get(
      `/song/enhance/player/url?ids=[${id}]&br=` + quality,
      {
        headers: {
          flag: cookie,
        },
      },
    );
  }

  if (cookie === "") {
    await normal();
  } else {
    if (quality === 2147483647) {
      await vip();
    } else {
      if (anonymous) {
        await normal();
        if (res.data.data[0].url === null) {
          await vip();
        }
      } else {
        await vip();
      }
    }
  }

  return res.data.data[0].url;
}

function lyric(id: string) {
  return "http://music.163.com/api/song/lyric?os=pc&id=" + id + "&lv=-1&tv=1";
}

async function playlist(id: string, limit: number, offset: number) {
  try {
    const res = await apiClient.get(
      "/v6/playlist/detail/?id=" + id + "&limit=" + limit + "&offset=" + offset,
    );
    return res.data;
  } catch (err: any) {
    console.error("API Error Response:", err.response.data);
    throw err;
  }
}

export default {
  async search(value: string, limit: number, offset: number) {
    let ids: Array<string> = [];

    const single = value.match(/music\.163\.com\/#\/song\?id=(\d+)/);
    const isPlaylist = value.match(/music\.163\.com\/#\/playlist\?id=(\d+)/);

    if (single) {
      ids = [single[1]];
    } else if (isPlaylist) {
      const res = await playlist(isPlaylist[1], limit, offset);
      ids = res.playlist.trackIds.map((track: any) => track.id);
      console.log(ids);
    } else {
      const res: any = await search(value, limit, offset);
      ids = res.result.songs.map((song: any) => song.id);
    }

    const songs: Array<Song> = [];

    await Promise.all(
      ids.map(async (id: string) => {
        const value: any = await detail(id);
        const song = {
          id: value.songs[0].id,
          name: value.songs[0].name,
          artist: value.songs[0].artists
            .map((item: any) => item.name)
            .join("/"),
          album: value.songs[0].album.name,
          cover: value.songs[0].album.picUrl,
          publishTime: format(
            new Date(value.songs[0].album.publishTime),
            "yyyy-MM-dd HH:mm:ss",
          ),
        };
        songs.push(song);
      }),
    );

    return songs;
  },

  async download(
    song: Song,
    cookie?: string,
    quality?: number,
    anonymous?: boolean,
  ) {
    song.url = await url(song.id, cookie, quality, anonymous);
    song.lyrics = lyric(song.id);
    return song;
  },
};
