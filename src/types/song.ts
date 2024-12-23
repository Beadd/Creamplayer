export interface Song {
  id: string;
  name: string;
  artist: string;
  album: string;
  cover: string;
  publishTime: string;
  url?: string;
  lyrics?: string;
  state?: string;
  path?: string;
}
