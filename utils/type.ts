export interface typeSong {
  id: string;
  name: string;
  cover: string;
}

export interface typeDetail {
  id: string;
  name: string;
  artist: string;
  album: string;
  cover: string;
  publishtime: string;
  url?: string;
  lyrics?: string;
  state?: string;
  path?: string;
}
