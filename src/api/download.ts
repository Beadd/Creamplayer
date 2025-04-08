import type { Song } from "../types/song";

function checkFileName(name: string, maxLength = 100) {
  const invalidRegex = /[\\/:*?"<>|]/g;
  let safeName = name.replace(invalidRegex, "-");

  if (safeName.length > maxLength) {
    safeName = safeName.slice(0, maxLength - 3) + "...";
  }

  return safeName;
}

export const electron = {
  // @saveLyric: Save lyrics to a separate file
  download: async (song: Song, saveLyric: boolean = false) => {
    const name = encodeURIComponent(checkFileName(song.name));
    const artist = encodeURIComponent(checkFileName(song.artist));
    const album = encodeURIComponent(checkFileName(song.album));
    const lyrics = song.lyrics ? song.lyrics : "";
    const publishTime = song.publishTime ? song.publishTime : "";

    // prettier-ignore
    let args = 
        ' -s "' + song.url + '" '  
      + ' -f "' + name + " - " + artist + '"'
      + ' -u "' + song.url + '" '  
      + ' -c "' + song.cover + '"'
      + ' -l "' + (lyrics ? lyrics : "") + '" '
      + ' -i ' + song.id
      + ' -t "' + name + '"'
      + ' -ar "' + artist + '"'
      + ' -al "' + album + '"'
      + ' -p "' + publishTime + '"';

    if (saveLyric) {
      args += " -sl";
    }

    const res = (window as any).electron.invoke("download", args);
    return res;
  },

  open(path: string) {
    (window as any).electron.invoke("open", path);
  },
};
