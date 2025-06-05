function checkfilename(name: string, maxlength = 100) {
  const invalidregex = /[\\/:*?"<>|]/g;
  let safename = name.replace(invalidregex, "-");

  if (safename.length > maxlength) {
    safename = `${safename.slice(0, maxlength - 3)}...`;
  }

  return safename;
}

export default {
  download: async (song: Song, savelyric: boolean = false) => {
    const name = encodeURIComponent(checkfilename(song.name));
    const artist = encodeURIComponent(checkfilename(song.artist));
    const album = encodeURIComponent(checkfilename(song.album));
    const lyrics = song.lyrics ? song.lyrics : "";
    const publishtime = song.publishtime ? song.publishtime : "";

    let args
      = ` -s "${song.url}"`
        + ` -f "${name} - ${artist}"`
        + ` -u "${song.url}"`
        + ` -c "${song.cover}"`
        + ` -l "${lyrics || ""}"`
        + ` -i ${song.id}`
        + ` -t "${name}"`
        + ` -ar "${artist}"`
        + ` -al "${album}"`
        + ` -p "${publishtime}"`;

    if (savelyric) {
      args += " -sl";
    }

    const res = (window as any).electron.invoke("download", args);
    return res;
  },

  open(path: string) {
    (window as any).electron.invoke("open", path);
  },
};
