import type { Song } from "../types/song";

function checkFileName(name: string) {
  const invalidRegex = /[\\/:*?<>|]/g;
  return name.replace(invalidRegex, "-");
}

export const electron = {
  download: async (song: Song) => {
    const name = encodeURIComponent(checkFileName(song.name));
    const artist = encodeURIComponent(checkFileName(song.artist));
    const album = encodeURIComponent(checkFileName(song.album));
    const lyrics = song.lyrics ? song.lyrics : "";
    const publishTime = song.publishTime ? song.publishTime : "";

    // prettier-ignore
    const args = 
        ' -s ' + song.url  
      + ' -f "' + name + " - " + artist + '"'
      + ' -u ' + song.url
      + ' -c ' + song.cover
      + ' -l ' + (lyrics ? `"${lyrics}"` : "")  
      + ' -i ' + song.id
      + ' -t "' + name + '"'
      + ' -ar "' + artist + '"'
      + ' -al "' + album + '"'
      + ' -p "' + publishTime + '"';

    // @ts-ignore
    const res = window.electron.invoke("download", args);
    return res;
  },

  open(path: string) {
    // @ts-ignore
    window.electron.invoke("open", path);
  },
};
